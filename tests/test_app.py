"""Tests du point d'entrée de l'application."""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QApplication

from calculatrice import __version__
from calculatrice.app import main


def test_main_configures_the_application_and_shows_the_window(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    created: dict[str, object] = {}

    def fake_exec(self: QApplication) -> int:
        created["application_name"] = self.applicationName()
        created["version"] = self.applicationVersion()
        created["visible_windows"] = [widget.isVisible() for widget in self.topLevelWidgets()]
        return 0

    monkeypatch.setattr(QApplication, "exec", fake_exec)
    assert main(["calculatrice"]) == 0
    assert created["application_name"] == "Calculatrice"
    assert created["version"] == __version__
    assert True in created["visible_windows"]  # type: ignore[operator]
