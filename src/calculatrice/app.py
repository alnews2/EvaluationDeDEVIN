"""Point d'entrée de l'application."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from calculatrice import __version__
from calculatrice.ui.main_window import MainWindow


def main(argv: list[str] | None = None) -> int:
    """Lance l'application graphique.

    Args:
        argv: Arguments de la ligne de commande. ``sys.argv`` par défaut.

    Returns:
        Le code de sortie de la boucle d'évènements Qt.
    """
    arguments = list(sys.argv if argv is None else argv)
    existing = QApplication.instance()
    application = existing if isinstance(existing, QApplication) else QApplication(arguments)
    application.setApplicationName("Calculatrice")
    application.setApplicationVersion(__version__)
    application.setOrganizationName("EvaluationDeDEVIN")

    window = MainWindow()
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
