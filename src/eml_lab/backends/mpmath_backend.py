"""mpmath backend using principal complex logarithm."""

from __future__ import annotations

from typing import Any

import mpmath as mp


def exp(x: Any) -> Any:
    return mp.exp(x)


def log(x: Any) -> Any:
    return mp.log(x)


def eml(x: Any, y: Any) -> Any:
    return exp(x) - log(y)

