"""Diagnostics for branch-sheet offsets.

These helpers classify observed differences. They do not repair witness
outputs and should not be used as pass criteria.
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp


@dataclass(frozen=True)
class OffsetClassification:
    classification: str
    k: int | None = None
    residual: str = ""


def _near_zero(z: object, tol: mp.mpf) -> bool:
    return abs(mp.mpc(z)) <= tol


def _nearest_integer(value: object) -> int:
    return int(mp.floor(mp.re(value) + mp.mpf("0.5"))) if mp.re(value) >= 0 else int(mp.ceil(mp.re(value) - mp.mpf("0.5")))


def detect_log_sheet_offset(actual: object, expected: object, *, tol: mp.mpf | str = "1e-35") -> OffsetClassification:
    """Detect whether actual - expected is approximately 2*pi*i*k."""

    tol = mp.mpf(tol)
    delta = mp.mpc(actual) - mp.mpc(expected)
    scaled = delta / (2 * mp.pi * mp.j)
    k = _nearest_integer(scaled)
    residual = delta - 2 * mp.pi * mp.j * k
    if _near_zero(residual, tol):
        return OffsetClassification("log-sheet-offset", k, mp.nstr(residual, 12))
    return OffsetClassification("no-log-sheet-offset", None, mp.nstr(residual, 12))


def detect_pi_offset(actual: object, expected: object, *, tol: mp.mpf | str = "1e-35") -> OffsetClassification:
    """Detect whether actual - expected is approximately pi*k."""

    tol = mp.mpf(tol)
    delta = mp.mpc(actual) - mp.mpc(expected)
    scaled = delta / mp.pi
    if abs(mp.im(scaled)) > tol:
        return OffsetClassification("no-pi-offset", None, mp.nstr(delta, 12))
    k = _nearest_integer(mp.re(scaled))
    residual = delta - mp.pi * k
    if _near_zero(residual, tol):
        return OffsetClassification("pi-offset", k, mp.nstr(residual, 12))
    return OffsetClassification("no-pi-offset", None, mp.nstr(residual, 12))


def detect_half_pi_offset(actual: object, expected: object, *, tol: mp.mpf | str = "1e-35") -> OffsetClassification:
    """Detect whether actual - expected is approximately (pi/2)*k."""

    tol = mp.mpf(tol)
    delta = mp.mpc(actual) - mp.mpc(expected)
    scaled = delta / (mp.pi / 2)
    if abs(mp.im(scaled)) > tol:
        return OffsetClassification("no-half-pi-offset", None, mp.nstr(delta, 12))
    k = _nearest_integer(mp.re(scaled))
    residual = delta - (mp.pi / 2) * k
    if _near_zero(residual, tol):
        return OffsetClassification("half-pi-offset", k, mp.nstr(residual, 12))
    return OffsetClassification("no-half-pi-offset", None, mp.nstr(residual, 12))


def is_sign_flip(actual: object, expected: object, *, tol: mp.mpf | str = "1e-35") -> bool:
    return _near_zero(mp.mpc(actual) + mp.mpc(expected), mp.mpf(tol))


def is_conjugate(actual: object, expected: object, *, tol: mp.mpf | str = "1e-35") -> bool:
    return _near_zero(mp.mpc(actual) - mp.conj(mp.mpc(expected)), mp.mpf(tol))


def classify_branch_offset(actual: object, expected: object, *, tol: mp.mpf | str = "1e-35") -> OffsetClassification:
    """Classify the smallest common branch offset pattern."""

    tol = mp.mpf(tol)
    actual_z = mp.mpc(actual)
    expected_z = mp.mpc(expected)
    if _near_zero(actual_z - expected_z, tol):
        return OffsetClassification("match", 0, "0")
    if is_sign_flip(actual_z, expected_z, tol=tol):
        return OffsetClassification("sign-flip", None, mp.nstr(actual_z + expected_z, 12))
    if is_conjugate(actual_z, expected_z, tol=tol):
        return OffsetClassification("conjugation", None, mp.nstr(actual_z - mp.conj(expected_z), 12))

    for detector in (detect_pi_offset, detect_half_pi_offset, detect_log_sheet_offset):
        result = detector(actual_z, expected_z, tol=tol)
        if not result.classification.startswith("no-"):
            return result

    return OffsetClassification("unclassified-offset", None, mp.nstr(actual_z - expected_z, 12))
