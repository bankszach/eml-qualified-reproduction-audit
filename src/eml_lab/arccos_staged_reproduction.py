"""Staged reproduction variants for the arccos witness.

The internal-helper variants are diagnostic-only. They show how the named
principal ``ArcCosh`` identity behaves, but they are not source-justified
replacements for the derived EML ``arcosh`` witness.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import mpmath as mp

from eml_lab.branch_verification import Backend, BranchEvaluator
from eml_lab.internal_branches import principal_arcosh_internal
from eml_lab.unwinding import classify_branch_offset, is_conjugate, is_sign_flip

ARCCOS_STAGE_SAMPLES = tuple(map(mp.mpf, ["-0.9", "-0.5", "-0.1", "-1e-12", "0", "1e-12", "0.1", "0.5", "0.9"]))

ArccosVariant = Literal[
    "named",
    "derived",
    "internal-helper",
    "internal-first-derived-final",
    "derived-first-internal-final",
]


@dataclass(frozen=True)
class ArccosStageResult:
    variant: ArccosVariant
    backend: str
    sample: str
    actual: str
    expected: str
    abs_error: str
    classification: str
    source_status: str
    notes: str


def _derived_arcosh(z: object, backend: Backend):
    return BranchEvaluator(backend).arcosh(z)


def _derived_cos(z: object, backend: Backend):
    return BranchEvaluator(backend).cos(z)


def arccos_named(x: object):
    return mp.acosh(mp.cos(mp.acosh(x)))


def arccos_derived(x: object, backend: Backend = "mpmath_lower"):
    evaluator = BranchEvaluator(backend)
    return evaluator.arcosh(evaluator.cos(evaluator.arcosh(x)))


def arccos_internal_helper(x: object):
    return principal_arcosh_internal(mp.cos(principal_arcosh_internal(x)))


def arcsin_internal_helper(x: object):
    return mp.pi / 2 - arccos_internal_helper(x)


def artanh_internal_helper(x: object):
    return mp.asinh(1 / mp.tan(arccos_internal_helper(x)))


def arctan_internal_helper(x: object):
    return arcsin_internal_helper(mp.tanh(mp.asinh(x)))


def arccos_internal_first_derived_final(x: object, backend: Backend = "mpmath_lower"):
    first = principal_arcosh_internal(x)
    return _derived_arcosh(_derived_cos(first, backend), backend)


def arccos_derived_first_internal_final(x: object, backend: Backend = "mpmath_lower"):
    first = _derived_arcosh(x, backend)
    return principal_arcosh_internal(_derived_cos(first, backend))


def evaluate_variant(variant: ArccosVariant, x: object, backend: Backend = "mpmath_lower"):
    if variant == "named":
        return arccos_named(x), "source-named-function"
    if variant == "derived":
        return arccos_derived(x, backend), "full-dependency-chain"
    if variant == "internal-helper":
        return arccos_internal_helper(x), "diagnostic-only"
    if variant == "internal-first-derived-final":
        return arccos_internal_first_derived_final(x, backend), "diagnostic-only"
    if variant == "derived-first-internal-final":
        return arccos_derived_first_internal_final(x, backend), "diagnostic-only"
    raise ValueError(variant)


def _classify(sample: object, actual: object, expected: object) -> tuple[str, str]:
    base = classify_branch_offset(actual, expected, tol=mp.mpf("1e-30"))
    if base.classification == "match":
        return "exact-match", "matches principal acos reference"
    if is_sign_flip(actual, expected, tol=mp.mpf("1e-30")):
        return "sign-flip", "actual is the negative of expected"
    if is_conjugate(actual, expected, tol=mp.mpf("1e-30")):
        return "conjugation", "actual is conjugate of expected"
    z = mp.mpc(sample)
    if z.imag == 0 and z.real < 0 and mp.almosteq(mp.re(actual), mp.acos(abs(z.real)), rel_eps=mp.mpf("1e-30"), abs_eps=mp.mpf("1e-30")):
        return "acos-absolute-value-sheet", "actual follows acos(abs(x))"
    if base.classification in {"pi-offset", "half-pi-offset", "log-sheet-offset"}:
        return base.classification, f"k={base.k}"
    return "wrong-sheet", base.residual


def diagnose_variant(variant: ArccosVariant, x: object, backend: Backend = "mpmath_lower") -> ArccosStageResult:
    with mp.workdps(90):
        actual, source_status = evaluate_variant(variant, x, backend)
        expected = mp.acos(x)
        classification, notes = _classify(x, actual, expected)
        return ArccosStageResult(
            variant=variant,
            backend=backend if variant != "named" else "mpmath-direct",
            sample=mp.nstr(x, 18),
            actual=mp.nstr(actual, 18),
            expected=mp.nstr(expected, 18),
            abs_error=mp.nstr(abs(actual - expected), 18),
            classification=classification,
            source_status=source_status,
            notes=notes,
        )


def diagnose_all_variants(backend: Backend = "mpmath_lower") -> dict[ArccosVariant, list[ArccosStageResult]]:
    variants: tuple[ArccosVariant, ...] = (
        "named",
        "derived",
        "internal-helper",
        "internal-first-derived-final",
        "derived-first-internal-final",
    )
    return {variant: [diagnose_variant(variant, sample, backend) for sample in ARCCOS_STAGE_SAMPLES] for variant in variants}
