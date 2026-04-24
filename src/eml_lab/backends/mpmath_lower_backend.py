"""mpmath backend with the author Mathematica LogLower convention."""

from __future__ import annotations

from typing import Any

import mpmath as mp


def _is_negative_real(z: Any) -> bool:
    c = mp.mpc(z)
    return c.imag == 0 and c.real < 0


def exp(x: Any) -> Any:
    return mp.exp(x)


def log(x: Any) -> Any:
    if _is_negative_real(x):
        return mp.log(-mp.mpc(x)) - mp.j * mp.pi
    return mp.log(x)


def eml(x: Any, y: Any) -> Any:
    return exp(x) - log(y)
