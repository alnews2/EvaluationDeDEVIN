"""Tests de la vue-modèle (signaux Qt)."""

from __future__ import annotations

from pytestqt.qtbot import QtBot

from calculatrice.core.operations import Operator
from calculatrice.ui.view_model import CalculatorViewModel


def test_display_changed_is_emitted_on_input(qtbot: QtBot) -> None:
    view_model = CalculatorViewModel()
    with qtbot.waitSignal(view_model.display_changed, timeout=1000) as blocker:
        view_model.input_digit("7")
    assert blocker.args == ["7"]
    assert view_model.display == "7"


def test_display_changed_is_not_emitted_without_change(qtbot: QtBot) -> None:
    view_model = CalculatorViewModel()
    with qtbot.assertNotEmitted(view_model.display_changed):
        view_model.input_digit("0")


def test_full_calculation_through_the_view_model(qtbot: QtBot) -> None:
    view_model = CalculatorViewModel()
    view_model.input_digit("1")
    view_model.input_digit("2")
    view_model.apply_operator(Operator.DIVIDE)
    view_model.input_digit("8")
    with qtbot.waitSignal(view_model.display_changed, timeout=1000) as blocker:
        view_model.compute()
    assert blocker.args == ["1.5"]


def test_error_state_changes_are_published(qtbot: QtBot) -> None:
    view_model = CalculatorViewModel()
    view_model.input_digit("5")
    view_model.apply_operator(Operator.DIVIDE)
    view_model.input_digit("0")
    with qtbot.waitSignal(view_model.error_state_changed, timeout=1000) as raised:
        view_model.compute()
    assert raised.args == [True]
    assert view_model.has_error is True

    with qtbot.waitSignal(view_model.error_state_changed, timeout=1000) as cleared:
        view_model.clear()
    assert cleared.args == [False]
    assert view_model.has_error is False


def test_editing_helpers(qtbot: QtBot) -> None:
    view_model = CalculatorViewModel()
    view_model.input_digit("4")
    view_model.input_decimal_separator()
    view_model.input_digit("2")
    assert view_model.display == "4.2"
    view_model.backspace()
    assert view_model.display == "4."
    view_model.toggle_sign()
    assert view_model.display == "-4."
    view_model.clear_entry()
    assert view_model.display == "0"
