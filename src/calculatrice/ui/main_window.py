"""Fenêtre principale de la calculatrice.

La fenêtre est purement déclarative : elle décrit un clavier, branche chaque
touche sur la vue-modèle, et se contente de refléter l'état publié.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QKeyEvent
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from calculatrice.core.operations import Operator
from calculatrice.ui.styles import STYLE_SHEET
from calculatrice.ui.view_model import CalculatorViewModel


@dataclass(frozen=True)
class KeySpec:
    """Description déclarative d'une touche du clavier."""

    name: str
    label: str
    row: int
    column: int
    action: Callable[[CalculatorViewModel], None]
    role: str = "digit"
    shortcuts: tuple[int, ...] = field(default_factory=tuple)
    accessible_name: str = ""


def _digit_key(digit: str, row: int, column: int) -> KeySpec:
    """Construit la touche du chiffre ``digit``."""
    return KeySpec(
        name=f"button_{digit}",
        label=digit,
        row=row,
        column=column,
        action=lambda view_model, digit=digit: view_model.input_digit(digit),  # type: ignore[misc]
        role="digit",
        shortcuts=(getattr(Qt.Key, f"Key_{digit}"),),
        accessible_name=f"Chiffre {digit}",
    )


def _operator_key(
    operator: Operator, name: str, row: int, column: int, shortcuts: tuple[int, ...]
) -> KeySpec:
    """Construit la touche de l'opération ``operator``."""
    return KeySpec(
        name=name,
        label=operator.symbol,
        row=row,
        column=column,
        action=lambda view_model, operator=operator: view_model.apply_operator(operator),  # type: ignore[misc]
        role="operator",
        shortcuts=shortcuts,
        accessible_name=f"Opération {operator.name.lower()}",
    )


#: Disposition complète du clavier, lue par :class:`MainWindow`.
KEY_SPECS: tuple[KeySpec, ...] = (
    KeySpec(
        name="button_clear",
        label="C",
        row=0,
        column=0,
        action=lambda view_model: view_model.clear(),
        role="command",
        shortcuts=(Qt.Key.Key_Escape,),
        accessible_name="Tout effacer",
    ),
    KeySpec(
        name="button_clear_entry",
        label="CE",
        row=0,
        column=1,
        action=lambda view_model: view_model.clear_entry(),
        role="command",
        shortcuts=(Qt.Key.Key_Delete,),
        accessible_name="Effacer la saisie",
    ),
    KeySpec(
        name="button_backspace",
        label="⌫",
        row=0,
        column=2,
        action=lambda view_model: view_model.backspace(),
        role="command",
        shortcuts=(Qt.Key.Key_Backspace,),
        accessible_name="Correction",
    ),
    _operator_key(Operator.DIVIDE, "button_divide", 0, 3, (Qt.Key.Key_Slash,)),
    _digit_key("7", 1, 0),
    _digit_key("8", 1, 1),
    _digit_key("9", 1, 2),
    _operator_key(Operator.MULTIPLY, "button_multiply", 1, 3, (Qt.Key.Key_Asterisk,)),
    _digit_key("4", 2, 0),
    _digit_key("5", 2, 1),
    _digit_key("6", 2, 2),
    _operator_key(Operator.SUBTRACT, "button_subtract", 2, 3, (Qt.Key.Key_Minus,)),
    _digit_key("1", 3, 0),
    _digit_key("2", 3, 1),
    _digit_key("3", 3, 2),
    _operator_key(Operator.ADD, "button_add", 3, 3, (Qt.Key.Key_Plus,)),
    KeySpec(
        name="button_sign",
        label="±",
        row=4,
        column=0,
        action=lambda view_model: view_model.toggle_sign(),
        role="command",
        shortcuts=(Qt.Key.Key_F9,),
        accessible_name="Changer de signe",
    ),
    _digit_key("0", 4, 1),
    KeySpec(
        name="button_decimal",
        label=",",
        row=4,
        column=2,
        action=lambda view_model: view_model.input_decimal_separator(),
        role="digit",
        shortcuts=(Qt.Key.Key_Comma, Qt.Key.Key_Period),
        accessible_name="Séparateur décimal",
    ),
    KeySpec(
        name="button_equals",
        label="=",
        row=4,
        column=3,
        action=lambda view_model: view_model.compute(),
        role="equals",
        shortcuts=(Qt.Key.Key_Equal, Qt.Key.Key_Return, Qt.Key.Key_Enter),
        accessible_name="Égale",
    ),
)


class MainWindow(QMainWindow):
    """Fenêtre principale : un afficheur et un clavier de seize touches."""

    def __init__(self, view_model: CalculatorViewModel | None = None) -> None:
        """Initialise la fenêtre.

        Args:
            view_model: Vue-modèle à piloter. Une instance neuve par défaut.
        """
        super().__init__()
        self._view_model = (
            view_model if view_model is not None else CalculatorViewModel(parent=self)
        )
        self._buttons: dict[str, QPushButton] = {}
        self._shortcuts: dict[int, QPushButton] = {}

        self.setWindowTitle("Calculatrice")
        self.setObjectName("main_window")
        self.setStyleSheet(STYLE_SHEET)
        self.setCentralWidget(self._build_central_widget())
        self.setMinimumSize(320, 420)

        self._view_model.display_changed.connect(self._on_display_changed)
        self._view_model.error_state_changed.connect(self._on_error_state_changed)
        self._on_display_changed(self._view_model.display)

    @property
    def view_model(self) -> CalculatorViewModel:
        """Vue-modèle pilotée par la fenêtre."""
        return self._view_model

    def button(self, name: str) -> QPushButton:
        """Retourne la touche nommée ``name``.

        Args:
            name: Nom d'objet de la touche, par exemple ``"button_add"``.

        Returns:
            Le bouton correspondant.

        Raises:
            KeyError: Si aucune touche ne porte ce nom.
        """
        return self._buttons[name]

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802 - API Qt
        """Redirige les raccourcis clavier vers la touche correspondante."""
        button = self._shortcuts.get(event.key())
        if button is None:
            super().keyPressEvent(event)
            return
        button.click()
        event.accept()

    def _build_central_widget(self) -> QWidget:
        """Construit l'afficheur et le clavier."""
        central = QWidget(self)
        central.setObjectName("central_widget")
        layout = QVBoxLayout(central)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self._display = QLabel("0", central)
        self._display.setObjectName("display")
        self._display.setAccessibleName("Afficheur")
        self._display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._display.setFont(QFont(self._display.font().family(), 28, QFont.Weight.DemiBold))
        self._display.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self._display)

        keypad = QWidget(central)
        keypad.setObjectName("keypad")
        grid = QGridLayout(keypad)
        grid.setSpacing(8)
        for spec in KEY_SPECS:
            grid.addWidget(self._build_button(spec, keypad), spec.row, spec.column)
        layout.addWidget(keypad, stretch=1)
        return central

    def _build_button(self, spec: KeySpec, parent: QWidget) -> QPushButton:
        """Construit la touche décrite par ``spec``."""
        button = QPushButton(spec.label, parent)
        button.setObjectName(spec.name)
        button.setProperty("role", spec.role)
        button.setAccessibleName(spec.accessible_name or spec.label)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        button.setMinimumSize(56, 48)
        button.clicked.connect(lambda *, spec=spec: spec.action(self._view_model))
        self._buttons[spec.name] = button
        for shortcut in spec.shortcuts:
            self._shortcuts[shortcut] = button
        return button

    def _on_display_changed(self, text: str) -> None:
        """Met à jour l'afficheur."""
        self._display.setText(text)

    def _on_error_state_changed(self, has_error: bool) -> None:
        """Applique le style d'erreur à l'afficheur."""
        self._display.setProperty("state", "error" if has_error else "normal")
        style = self._display.style()
        style.unpolish(self._display)
        style.polish(self._display)
