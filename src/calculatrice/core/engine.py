"""Automate de la calculatrice : saisie, opérations en attente, erreurs.

Cette classe ne dépend d'aucune bibliothèque graphique : elle est intégralement
testable sans interface, et constitue la référence du comportement attendu.
"""

from __future__ import annotations

from decimal import Decimal

from calculatrice.core.errors import CalculationError
from calculatrice.core.formatting import format_number
from calculatrice.core.operations import Operator, apply

#: Nombre maximal de chiffres saisissables.
MAX_INPUT_DIGITS = 15

_DIGITS = frozenset("0123456789")


class CalculatorEngine:
    """Automate d'une calculatrice à quatre opérations.

    L'automate conserve trois éléments : la saisie courante, un accumulateur
    (le résultat partiel) et l'opération en attente. En cas d'erreur, toutes
    les touches sont ignorées sauf :meth:`clear` et :meth:`clear_entry`.
    """

    _entry: str
    _accumulator: Decimal | None
    _pending: Operator | None
    _entry_is_stale: bool
    _error: str | None
    _repeat_operator: Operator | None
    _repeat_operand: Decimal | None

    def __init__(self) -> None:
        """Crée un automate remis à zéro."""
        self.clear()

    # ------------------------------------------------------------------
    # Lecture de l'état
    # ------------------------------------------------------------------
    @property
    def display(self) -> str:
        """Texte à afficher : la saisie courante, ou le message d'erreur."""
        return self._error if self._error is not None else self._entry

    @property
    def has_error(self) -> bool:
        """Vrai tant que l'erreur courante n'a pas été acquittée."""
        return self._error is not None

    @property
    def pending_operator(self) -> Operator | None:
        """Opération en attente d'un second opérande, le cas échéant."""
        return self._pending

    @property
    def value(self) -> Decimal:
        """Valeur numérique de la saisie courante."""
        return Decimal(self._entry)

    # ------------------------------------------------------------------
    # Saisie
    # ------------------------------------------------------------------
    def press_digit(self, digit: str) -> None:
        """Saisit un chiffre.

        Args:
            digit: Un caractère de ``"0"`` à ``"9"``.

        Raises:
            ValueError: Si ``digit`` n'est pas un chiffre unique.
        """
        if digit not in _DIGITS:
            raise ValueError(f"Chiffre invalide : {digit!r}")
        if self._error is not None:
            return
        if self._entry_is_stale:
            self._entry = digit
            self._entry_is_stale = False
            return
        if self._count_digits(self._entry) >= MAX_INPUT_DIGITS:
            return
        self._entry = digit if self._entry == "0" else self._entry + digit

    def press_decimal_separator(self) -> None:
        """Saisit le séparateur décimal, sans jamais en produire deux."""
        if self._error is not None:
            return
        if self._entry_is_stale:
            self._entry = "0."
            self._entry_is_stale = False
        elif "." not in self._entry:
            self._entry += "."

    def toggle_sign(self) -> None:
        """Inverse le signe de la saisie courante."""
        if self._error is not None or self._entry in {"0", "0."}:
            return
        self._entry = self._entry[1:] if self._entry.startswith("-") else "-" + self._entry

    def backspace(self) -> None:
        """Efface le dernier caractère saisi."""
        if self._error is not None or self._entry_is_stale:
            return
        truncated = self._entry[:-1]
        self._entry = "0" if truncated in {"", "-"} else truncated

    # ------------------------------------------------------------------
    # Opérations
    # ------------------------------------------------------------------
    def press_operator(self, operator: Operator) -> None:
        """Enregistre ``operator``, en repliant l'opération déjà en attente."""
        if self._error is not None:
            return
        if self._pending is not None and not self._entry_is_stale:
            if not self._fold_pending(self.value):
                return
        elif self._pending is None:
            self._accumulator = self.value
        self._pending = operator
        self._entry_is_stale = True
        self._repeat_operator = None
        self._repeat_operand = None

    def press_equals(self) -> None:
        """Termine le calcul, ou répète la dernière opération."""
        if self._error is not None:
            return
        if self._pending is not None:
            self._repeat_operator = self._pending
            self._repeat_operand = self.value
            operand = self.value
        elif self._repeat_operator is not None and self._repeat_operand is not None:
            self._accumulator = self.value
            self._pending = self._repeat_operator
            operand = self._repeat_operand
        else:
            self._entry_is_stale = True
            return
        folded = self._fold_pending(operand)
        self._pending = None
        if folded:
            self._entry_is_stale = True

    # ------------------------------------------------------------------
    # Remise à zéro
    # ------------------------------------------------------------------
    def clear_entry(self) -> None:
        """Efface la saisie courante (touche ``CE``) et acquitte l'erreur."""
        self._entry = "0"
        self._entry_is_stale = True
        self._error = None

    def clear(self) -> None:
        """Remet l'automate à son état initial (touche ``C``)."""
        self._entry = "0"
        self._accumulator = None
        self._pending = None
        self._entry_is_stale = True
        self._error = None
        self._repeat_operator = None
        self._repeat_operand = None

    # ------------------------------------------------------------------
    # Interne
    # ------------------------------------------------------------------
    def _fold_pending(self, operand: Decimal) -> bool:
        """Applique l'opération en attente à ``operand``.

        Args:
            operand: Second opérande de l'opération en attente.

        Returns:
            ``True`` si le calcul a abouti, ``False`` s'il a échoué (l'erreur
            est alors déjà publiée dans :attr:`display`).
        """
        pending = self._pending
        if pending is None:  # pragma: no cover - invariant interne
            return True
        left = self._accumulator if self._accumulator is not None else Decimal(0)
        try:
            result = apply(pending, left, operand)
            self._entry = format_number(result)
        except CalculationError as exc:
            self._fail(exc.message)
            return False
        self._accumulator = Decimal(self._entry)
        return True

    def _fail(self, message: str) -> None:
        """Bascule l'automate en état d'erreur."""
        self._error = message
        self._entry = "0"
        self._entry_is_stale = True
        self._accumulator = None
        self._pending = None
        self._repeat_operator = None
        self._repeat_operand = None

    @staticmethod
    def _count_digits(entry: str) -> int:
        """Compte les chiffres significatifs présents dans ``entry``."""
        return sum(1 for character in entry if character in _DIGITS)
