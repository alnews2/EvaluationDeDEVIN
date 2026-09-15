"""Tests des quatre opérations."""

from __future__ import annotations

from decimal import Decimal

import pytest

from calculatrice.core.errors import DivisionByZeroError, OverflowLimitError
from calculatrice.core.operations import Operator, apply


@pytest.mark.parametrize(
    ("operator", "left", "right", "expected"),
    [
        (Operator.ADD, "1", "2", "3"),
        (Operator.ADD, "0.1", "0.2", "0.3"),
        (Operator.ADD, "-5", "5", "0"),
        (Operator.SUBTRACT, "10", "4", "6"),
        (Operator.SUBTRACT, "4", "10", "-6"),
        (Operator.MULTIPLY, "7", "6", "42"),
        (Operator.MULTIPLY, "2.5", "4", "10.0"),
        (Operator.MULTIPLY, "0", "12345", "0"),
        (Operator.DIVIDE, "9", "3", "3"),
        (Operator.DIVIDE, "1", "8", "0.125"),
        (Operator.DIVIDE, "-6", "4", "-1.5"),
    ],
)
def test_apply_returns_exact_decimal_result(
    operator: Operator, left: str, right: str, expected: str
) -> None:
    assert apply(operator, Decimal(left), Decimal(right)) == Decimal(expected)


def test_decimal_arithmetic_avoids_binary_float_artifacts() -> None:
    assert str(apply(Operator.ADD, Decimal("0.1"), Decimal("0.2"))) == "0.3"
    assert 0.1 + 0.2 != 0.3  # le même calcul en virgule flottante binaire échoue


def test_division_by_zero_is_rejected() -> None:
    with pytest.raises(DivisionByZeroError, match="Division par zéro"):
        apply(Operator.DIVIDE, Decimal(1), Decimal(0))


def test_overflow_is_reported_as_business_error() -> None:
    huge = Decimal("1e500000")
    with pytest.raises(OverflowLimitError):
        apply(Operator.MULTIPLY, huge, huge)


@pytest.mark.parametrize(
    ("operator", "symbol"),
    [
        (Operator.ADD, "+"),
        (Operator.SUBTRACT, "−"),
        (Operator.MULTIPLY, "×"),
        (Operator.DIVIDE, "÷"),
    ],
)
def test_operator_symbols(operator: Operator, symbol: str) -> None:
    assert operator.symbol == symbol
