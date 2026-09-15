"""Tests de l'automate de la calculatrice."""

from __future__ import annotations

from decimal import Decimal

import pytest

from calculatrice.core.engine import MAX_INPUT_DIGITS, CalculatorEngine
from calculatrice.core.errors import OverflowLimitError
from calculatrice.core.operations import Operator

_OPERATORS = {
    "+": Operator.ADD,
    "-": Operator.SUBTRACT,
    "*": Operator.MULTIPLY,
    "/": Operator.DIVIDE,
}


def press(engine: CalculatorEngine, sequence: str) -> str:
    """Joue une séquence de touches et retourne l'afficheur.

    Les caractères reconnus sont les chiffres, ``.``, les opérateurs
    ``+-*/``, ``=`` (égale), ``c`` (remise à zéro), ``e`` (effacer la saisie),
    ``<`` (correction) et ``~`` (changement de signe).
    """
    for key in sequence:
        if key.isdigit():
            engine.press_digit(key)
        elif key == ".":
            engine.press_decimal_separator()
        elif key in _OPERATORS:
            engine.press_operator(_OPERATORS[key])
        elif key == "=":
            engine.press_equals()
        elif key == "c":
            engine.clear()
        elif key == "e":
            engine.clear_entry()
        elif key == "<":
            engine.backspace()
        elif key == "~":
            engine.toggle_sign()
        else:  # pragma: no cover - erreur de test
            raise AssertionError(f"Touche inconnue : {key!r}")
    return engine.display


@pytest.mark.parametrize(
    ("sequence", "expected"),
    [
        ("2+3=", "5"),
        ("9-4=", "5"),
        ("6*7=", "42"),
        ("8/2=", "4"),
        ("1/8=", "0.125"),
        (".1+.2=", "0.3"),
        ("2+3*4=", "20"),  # évaluation de gauche à droite
        ("5*2-3=", "7"),
        ("100/4/5=", "5"),
    ],
)
def test_nominal_sequences(engine: CalculatorEngine, sequence: str, expected: str) -> None:
    assert press(engine, sequence) == expected


def test_initial_state(engine: CalculatorEngine) -> None:
    assert engine.display == "0"
    assert engine.has_error is False
    assert engine.pending_operator is None
    assert engine.value == Decimal(0)


def test_digits_replace_the_previous_result(engine: CalculatorEngine) -> None:
    press(engine, "2+3=")
    assert press(engine, "7") == "7"


def test_operator_chains_on_the_previous_result(engine: CalculatorEngine) -> None:
    press(engine, "2+3=")
    assert press(engine, "*2=") == "10"


def test_pending_operator_is_exposed(engine: CalculatorEngine) -> None:
    press(engine, "2+")
    assert engine.pending_operator is Operator.ADD
    press(engine, "3=")
    assert engine.pending_operator is None


def test_operator_can_be_corrected_before_the_second_operand(engine: CalculatorEngine) -> None:
    assert press(engine, "8+-2=") == "6"


def test_equals_repeats_the_last_operation(engine: CalculatorEngine) -> None:
    assert press(engine, "2+3=") == "5"
    assert press(engine, "=") == "8"
    assert press(engine, "==") == "14"


def test_equals_without_pending_operation_is_inert(engine: CalculatorEngine) -> None:
    assert press(engine, "5=") == "5"


def test_leading_zero_is_replaced(engine: CalculatorEngine) -> None:
    assert press(engine, "007") == "7"


def test_single_decimal_separator(engine: CalculatorEngine) -> None:
    assert press(engine, "1.2.3") == "1.23"


def test_decimal_separator_starts_a_new_entry(engine: CalculatorEngine) -> None:
    assert press(engine, ".5") == "0.5"


def test_decimal_separator_after_a_result_starts_a_new_entry(engine: CalculatorEngine) -> None:
    press(engine, "2+3=")
    assert press(engine, ".5") == "0.5"


def test_input_length_is_capped(engine: CalculatorEngine) -> None:
    assert press(engine, "1" * (MAX_INPUT_DIGITS + 5)) == "1" * MAX_INPUT_DIGITS


def test_backspace(engine: CalculatorEngine) -> None:
    assert press(engine, "123<") == "12"
    assert press(engine, "<<") == "0"


def test_backspace_on_a_negative_entry_returns_to_zero(engine: CalculatorEngine) -> None:
    assert press(engine, "5~<") == "0"


def test_backspace_does_not_alter_a_result(engine: CalculatorEngine) -> None:
    press(engine, "2+3=")
    assert press(engine, "<") == "5"


def test_toggle_sign(engine: CalculatorEngine) -> None:
    assert press(engine, "5~") == "-5"
    assert press(engine, "~") == "5"


def test_toggle_sign_is_inert_on_zero(engine: CalculatorEngine) -> None:
    assert press(engine, "~") == "0"
    assert press(engine, ".~") == "0."


def test_negative_operand(engine: CalculatorEngine) -> None:
    assert press(engine, "3~*4=") == "-12"


def test_clear_entry_keeps_the_pending_operation(engine: CalculatorEngine) -> None:
    press(engine, "7+9")
    assert press(engine, "e") == "0"
    assert press(engine, "1=") == "8"


def test_clear_resets_everything(engine: CalculatorEngine) -> None:
    press(engine, "7+9")
    assert press(engine, "c") == "0"
    assert engine.pending_operator is None
    assert press(engine, "3=") == "3"


class TestErrors:
    """Comportement de l'automate en situation d'erreur."""

    def test_division_by_zero_shows_a_message(self, engine: CalculatorEngine) -> None:
        assert press(engine, "8/0=") == "Division par zéro"
        assert engine.has_error is True

    def test_division_by_zero_while_chaining(self, engine: CalculatorEngine) -> None:
        assert press(engine, "8/0+") == "Division par zéro"

    def test_any_calculation_error_is_surfaced(
        self, engine: CalculatorEngine, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def raise_overflow(*_args: object) -> Decimal:
            raise OverflowLimitError

        monkeypatch.setattr("calculatrice.core.engine.apply", raise_overflow)
        assert press(engine, "2*3=") == "Résultat hors limites"
        assert engine.has_error is True

    @pytest.mark.parametrize("keys", ["5", ".", "~", "<", "+", "="])
    def test_keys_are_ignored_until_the_error_is_acknowledged(
        self, engine: CalculatorEngine, keys: str
    ) -> None:
        press(engine, "8/0=")
        assert press(engine, keys) == "Division par zéro"

    @pytest.mark.parametrize("reset_key", ["c", "e"])
    def test_error_is_acknowledged_by_clear_keys(
        self, engine: CalculatorEngine, reset_key: str
    ) -> None:
        press(engine, "8/0=")
        assert press(engine, reset_key) == "0"
        assert engine.has_error is False
        assert press(engine, "2+2=") == "4"


def test_press_digit_rejects_invalid_input(engine: CalculatorEngine) -> None:
    with pytest.raises(ValueError, match="Chiffre invalide"):
        engine.press_digit("x")
