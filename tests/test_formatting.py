"""Tests du formatage de l'afficheur."""

from __future__ import annotations

from decimal import Decimal

import pytest

from calculatrice.core.errors import OverflowLimitError
from calculatrice.core.formatting import format_number


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("0", "0"),
        ("-0", "0"),
        ("42", "42"),
        ("-42", "-42"),
        ("2.50", "2.5"),
        ("0.125", "0.125"),
        ("1000", "1000"),
        ("1E+3", "1000"),
        ("0.3333333333333333", "0.333333333333"),
        ("123456789012", "123456789012"),
    ],
)
def test_format_number(value: str, expected: str) -> None:
    assert format_number(Decimal(value)) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("1E+12", "1e+12"),
        ("1.5E+20", "1.5e+20"),
        ("-2E+15", "-2e+15"),
        ("1E-13", "1e-13"),
    ],
)
def test_large_and_small_values_use_scientific_notation(value: str, expected: str) -> None:
    assert format_number(Decimal(value)) == expected


@pytest.mark.parametrize("value", ["Infinity", "-Infinity", "NaN"])
def test_non_finite_values_are_rejected(value: str) -> None:
    with pytest.raises(OverflowLimitError):
        format_number(Decimal(value))
