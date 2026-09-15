"""Vue-modèle : adapte le cœur métier aux signaux attendus par l'interface.

C'est la seule couche qui connaisse à la fois :mod:`calculatrice.core` et Qt.
Elle n'implémente aucune règle de calcul : elle délègue et publie l'état.
"""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from calculatrice.core.engine import CalculatorEngine
from calculatrice.core.operations import Operator


class CalculatorViewModel(QObject):
    """Expose l'état de :class:`~calculatrice.core.engine.CalculatorEngine` via des signaux."""

    #: Émis à chaque changement du texte de l'afficheur.
    display_changed = Signal(str)
    #: Émis lorsque l'automate entre ou sort de l'état d'erreur.
    error_state_changed = Signal(bool)

    def __init__(
        self, engine: CalculatorEngine | None = None, parent: QObject | None = None
    ) -> None:
        """Initialise la vue-modèle.

        Args:
            engine: Automate à piloter. Un automate neuf est créé par défaut.
            parent: Parent Qt éventuel.
        """
        super().__init__(parent)
        self._engine = engine if engine is not None else CalculatorEngine()
        self._last_display = self._engine.display
        self._last_error_state = self._engine.has_error

    @property
    def display(self) -> str:
        """Texte courant de l'afficheur."""
        return self._engine.display

    @property
    def has_error(self) -> bool:
        """Vrai si l'automate est en état d'erreur."""
        return self._engine.has_error

    def input_digit(self, digit: str) -> None:
        """Saisit le chiffre ``digit``."""
        self._engine.press_digit(digit)
        self._publish()

    def input_decimal_separator(self) -> None:
        """Saisit le séparateur décimal."""
        self._engine.press_decimal_separator()
        self._publish()

    def toggle_sign(self) -> None:
        """Inverse le signe de la saisie courante."""
        self._engine.toggle_sign()
        self._publish()

    def backspace(self) -> None:
        """Efface le dernier caractère saisi."""
        self._engine.backspace()
        self._publish()

    def apply_operator(self, operator: Operator) -> None:
        """Enregistre l'opération ``operator``."""
        self._engine.press_operator(operator)
        self._publish()

    def compute(self) -> None:
        """Déclenche le calcul du résultat."""
        self._engine.press_equals()
        self._publish()

    def clear_entry(self) -> None:
        """Efface la saisie courante."""
        self._engine.clear_entry()
        self._publish()

    def clear(self) -> None:
        """Remet la calculatrice à zéro."""
        self._engine.clear()
        self._publish()

    def _publish(self) -> None:
        """Émet les signaux correspondant aux changements d'état."""
        display = self._engine.display
        if display != self._last_display:
            self._last_display = display
            self.display_changed.emit(display)
        error_state = self._engine.has_error
        if error_state != self._last_error_state:
            self._last_error_state = error_state
            self.error_state_changed.emit(error_state)
