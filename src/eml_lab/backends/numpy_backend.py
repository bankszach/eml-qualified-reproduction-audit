"""NumPy backend using complex dtype to expose principal-log behavior."""

from __future__ import annotations

from typing import Any

import numpy as np


def _array(value: Any) -> Any:
    return np.asarray(value, dtype=np.complex128)


def exp(x: Any) -> Any:
    return np.exp(_array(x))


def log(x: Any) -> Any:
    return np.log(_array(x))


def eml(x: Any, y: Any) -> Any:
    with np.errstate(all="ignore"):
        return exp(x) - log(y)


def has_invalid_numeric_state(value: Any) -> bool:
    arr = np.asarray(value)
    return bool(np.any(np.isnan(arr)))

