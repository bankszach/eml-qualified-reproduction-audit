"""SymPy backend for symbolic sanity checks."""

from __future__ import annotations

from typing import Any

import sympy as sp


def exp(x: Any) -> Any:
    return sp.exp(x)


def log(x: Any) -> Any:
    return sp.log(x)


def eml(x: Any, y: Any) -> Any:
    return exp(x) - log(y)

