"""Erreurs métier de la calculatrice.

Chaque erreur porte un message déjà rédigé pour l'utilisateur final : la couche
graphique se contente de l'afficher, elle n'a aucune décision à prendre.
"""


class CalculationError(Exception):
    """Erreur de calcul destinée à être affichée telle quelle."""

    def __init__(self, message: str) -> None:
        """Initialise l'erreur avec le message présenté à l'utilisateur."""
        super().__init__(message)
        self.message = message


class DivisionByZeroError(CalculationError):
    """Division par zéro."""

    def __init__(self) -> None:
        """Initialise l'erreur avec le message standard de division par zéro."""
        super().__init__("Division par zéro")


class OverflowLimitError(CalculationError):
    """Résultat hors des limites représentables par l'afficheur."""

    def __init__(self) -> None:
        """Initialise l'erreur avec le message standard de dépassement."""
        super().__init__("Résultat hors limites")
