"""Fixtures partagées par la suite de tests."""

from __future__ import annotations

import os

import pytest
from pytestqt.qtbot import QtBot

from calculatrice.core.engine import CalculatorEngine
from calculatrice.ui.main_window import MainWindow

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture
def engine() -> CalculatorEngine:
    """Automate neuf, sans interface."""
    return CalculatorEngine()


@pytest.fixture
def window(qtbot: QtBot) -> MainWindow:
    """Fenêtre principale enregistrée auprès de ``qtbot``."""
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    return main_window
