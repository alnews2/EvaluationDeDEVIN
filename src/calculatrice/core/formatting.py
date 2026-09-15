"""Conversion des nombres décimaux en texte destiné à l'afficheur."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, localcontext

from calculatrice.core.errors import OverflowLimitError

#: Nombre de chiffres significatifs affichés.
DISPLAY_PRECISION = 12


def format_number(value: Decimal) -> str:
    """Formate ``value`` pour l'afficheur.

    Les entiers sont affichés sans séparateur décimal, les zéros de fin sont
    supprimés, et la notation scientifique n'est employée que lorsque la
    notation positionnelle dépasserait la largeur utile de l'afficheur.

    Args:
        value: Valeur à formater.

    Returns:
        La représentation textuelle de ``value``.

    Raises:
        OverflowLimitError: Si ``value`` n'est pas un nombre fini.
    """
    if not value.is_finite():
        raise OverflowLimitError

    with localcontext() as context:
        context.prec = DISPLAY_PRECISION
        try:
            rounded = +value
        except InvalidOperation as exc:  # pragma: no cover - garde-fou défensif
            raise OverflowLimitError from exc

    if rounded == 0:
        return "0"

    normalized = rounded.normalize()
    exponent = normalized.adjusted()
    if exponent >= DISPLAY_PRECISION or exponent <= -DISPLAY_PRECISION:
        return _to_scientific(normalized)
    return f"{normalized:f}"


def _to_scientific(value: Decimal) -> str:
    """Rend ``value`` en notation scientifique compacte (``1.5e+20``)."""
    mantissa, _, exponent = f"{value:e}".partition("e")
    mantissa = mantissa.rstrip("0").rstrip(".") if "." in mantissa else mantissa
    return f"{mantissa}e{exponent}"
