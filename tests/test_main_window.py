"""Tests de l'interface graphique, pilotée comme un utilisateur (clics et clavier)."""

from __future__ import annotations

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton
from pytestqt.qtbot import QtBot

from calculatrice.ui.main_window import KEY_SPECS, MainWindow

pytestmark = pytest.mark.gui

_BUTTON_BY_CHARACTER = {
    "+": "button_add",
    "-": "button_subtract",
    "*": "button_multiply",
    "/": "button_divide",
    "=": "button_equals",
    ".": "button_decimal",
    "c": "button_clear",
    "e": "button_clear_entry",
    "<": "button_backspace",
    "~": "button_sign",
}


def display_of(window: MainWindow) -> str:
    """Retourne le texte affiché par la fenêtre."""
    label = window.findChild(QLabel, "display")
    assert label is not None
    return label.text()


def click(qtbot: QtBot, window: MainWindow, sequence: str) -> str:
    """Clique la séquence de touches ``sequence`` et retourne l'afficheur."""
    for character in sequence:
        name = f"button_{character}" if character.isdigit() else _BUTTON_BY_CHARACTER[character]
        qtbot.mouseClick(window.button(name), Qt.MouseButton.LeftButton)
    return display_of(window)


def test_window_exposes_every_declared_key(window: MainWindow) -> None:
    for spec in KEY_SPECS:
        button = window.findChild(QPushButton, spec.name)
        assert button is not None, spec.name
        assert button.text() == spec.label
        assert button.accessibleName()


def test_initial_display(window: MainWindow) -> None:
    assert display_of(window) == "0"
    assert window.windowTitle() == "Calculatrice"


@pytest.mark.parametrize(
    ("sequence", "expected"),
    [
        ("2+3=", "5"),
        ("9-4=", "5"),
        ("6*7=", "42"),
        ("8/2=", "4"),
        (".1+.2=", "0.3"),
        ("5~*3=", "-15"),
        ("12<=", "1"),
    ],
)
def test_calculations_by_clicking(
    qtbot: QtBot, window: MainWindow, sequence: str, expected: str
) -> None:
    assert click(qtbot, window, sequence) == expected


def test_clear_keys_by_clicking(qtbot: QtBot, window: MainWindow) -> None:
    assert click(qtbot, window, "7+8") == "8"
    assert click(qtbot, window, "e") == "0"
    assert click(qtbot, window, "2=") == "9"
    assert click(qtbot, window, "c") == "0"


@pytest.mark.parametrize(
    ("keys", "expected"),
    [
        ([Qt.Key.Key_3, Qt.Key.Key_Plus, Qt.Key.Key_4, Qt.Key.Key_Return], "7"),
        ([Qt.Key.Key_8, Qt.Key.Key_Slash, Qt.Key.Key_2, Qt.Key.Key_Equal], "4"),
        ([Qt.Key.Key_5, Qt.Key.Key_Asterisk, Qt.Key.Key_6, Qt.Key.Key_Enter], "30"),
        ([Qt.Key.Key_9, Qt.Key.Key_Minus, Qt.Key.Key_1, Qt.Key.Key_Return], "8"),
        ([Qt.Key.Key_1, Qt.Key.Key_Comma, Qt.Key.Key_5], "1.5"),
        ([Qt.Key.Key_1, Qt.Key.Key_Period, Qt.Key.Key_5], "1.5"),
        ([Qt.Key.Key_7, Qt.Key.Key_Backspace], "0"),
        ([Qt.Key.Key_7, Qt.Key.Key_F9], "-7"),
        ([Qt.Key.Key_7, Qt.Key.Key_Escape], "0"),
        ([Qt.Key.Key_7, Qt.Key.Key_Delete], "0"),
    ],
)
def test_keyboard_shortcuts(
    qtbot: QtBot, window: MainWindow, keys: list[Qt.Key], expected: str
) -> None:
    for key in keys:
        qtbot.keyClick(window, key)
    qtbot.waitUntil(lambda: display_of(window) == expected, timeout=1000)


def test_unbound_key_is_ignored(qtbot: QtBot, window: MainWindow) -> None:
    qtbot.keyClick(window, Qt.Key.Key_5)
    qtbot.keyClick(window, Qt.Key.Key_A)
    assert display_of(window) == "5"


def test_division_by_zero_is_shown_and_styled(qtbot: QtBot, window: MainWindow) -> None:
    label = window.findChild(QLabel, "display")
    assert label is not None
    assert click(qtbot, window, "8/0=") == "Division par zéro"
    assert label.property("state") == "error"

    assert click(qtbot, window, "c") == "0"
    assert label.property("state") == "normal"


def test_window_reflects_an_externally_driven_view_model(qtbot: QtBot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.view_model.input_digit("9")
    assert display_of(window) == "9"
