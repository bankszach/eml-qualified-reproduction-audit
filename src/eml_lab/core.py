"""Core EML operator implementations."""

from __future__ import annotations

from typing import Any, Literal

BackendName = Literal["mpmath", "mpmath_lower", "numpy", "sympy"]


class EMLDomainError(ValueError):
    """Raised when a backend reports invalid EML domain behavior."""


def eml(x: Any, y: Any, backend: BackendName = "mpmath", *, strict: bool = True) -> Any:
    """Evaluate eml(x, y) = exp(x) - log(y) with an explicit backend."""

    if backend == "mpmath":
        from eml_lab.backends.mpmath_backend import eml as backend_eml
    elif backend == "mpmath_lower":
        from eml_lab.backends.mpmath_lower_backend import eml as backend_eml
    elif backend == "numpy":
        from eml_lab.backends.numpy_backend import eml as backend_eml
    elif backend == "sympy":
        from eml_lab.backends.sympy_backend import eml as backend_eml
    else:
        raise ValueError(f"unknown EML backend: {backend!r}")

    try:
        value = backend_eml(x, y)
    except Exception as exc:  # pragma: no cover - backend-specific detail
        if strict:
            raise EMLDomainError(f"{backend} failed to evaluate eml({x!r}, {y!r})") from exc
        return exc

    if strict and backend == "numpy":
        from eml_lab.backends.numpy_backend import has_invalid_numeric_state

        if has_invalid_numeric_state(value):
            raise EMLDomainError(f"numpy produced invalid numeric state for eml({x!r}, {y!r})")

    return value


def mpmath_eml(x: Any, y: Any) -> Any:
    """Explicit mpmath implementation."""

    from eml_lab.backends.mpmath_backend import eml as backend_eml

    return backend_eml(x, y)


def numpy_eml(x: Any, y: Any) -> Any:
    """Explicit NumPy implementation."""

    from eml_lab.backends.numpy_backend import eml as backend_eml

    return backend_eml(x, y)
