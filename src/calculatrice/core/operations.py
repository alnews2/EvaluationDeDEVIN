"""Les quatre opérations arithmétiques, en arithmétique décimale exacte."""

from __future__ import annotations

import operator as builtin_operator
from collections.abc import Callable
from decimal import Decimal, DivisionByZero, InvalidOperation, Overflow, localcontext
from enum import Enum

from calculatrice.core.errors import DivisionByZeroError, OverflowLimitError

#: Nombre de chiffres significatifs conservés pendant les calculs.
CALCULATION_PRECISION = 28


class Operator(Enum):
    """Opérateur binaire supporté par la calculatrice.

    La valeur de chaque membre est le symbole affiché dans l'interface.
    """

    ADD = "+"
    SUBTRACT = "−"
    MULTIPLY = "×"
    DIVIDE = "÷"

    @property
    def symbol(self) -> str:
        """Symbole destiné à l'affichage."""
        return self.value


#: Implémentation de chaque opérateur.
_IMPLEMENTATIONS: dict[Operator, Callable[[Decimal, Decimal], Decimal]] = {
    Operator.ADD: builtin_operator.add,
    Operator.SUBTRACT: builtin_operator.sub,
    Operator.MULTIPLY: builtin_operator.mul,
    Operator.DIVIDE: builtin_operator.truediv,
}


def apply(operator: Operator, left: Decimal, right: Decimal) -> Decimal:
    """Applique ``operator`` à ``left`` et ``right``.

    Args:
        operator: Opération à effectuer.
        left: Opérande de gauche.
        right: Opérande de droite.

    Returns:
        Le résultat, arrondi à :data:`CALCULATION_PRECISION` chiffres significatifs.

    Raises:
        DivisionByZeroError: Si ``operator`` est une division et ``right`` vaut zéro.
        OverflowLimitError: Si le résultat dépasse les capacités de l'afficheur.
    """
    if operator is Operator.DIVIDE and right == 0:
        raise DivisionByZeroError

    with localcontext() as context:
        context.prec = CALCULATION_PRECISION
        try:
            return _IMPLEMENTATIONS[operator](left, right)
        except DivisionByZero as exc:  # pragma: no cover - garde-fou défensif
            raise DivisionByZeroError from exc
        except (Overflow, InvalidOperation) as exc:
            raise OverflowLimitError from exc
