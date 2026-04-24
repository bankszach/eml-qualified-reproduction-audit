"""Extended-domain diagnostics for the derived arcosh witness."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

import mpmath as mp

from eml_lab.branch_verification import Backend, BranchEvaluator
from eml_lab.unwinding import classify_branch_offset, detect_log_sheet_offset, detect_pi_offset, is_conjugate, is_sign_flip

ARCOSH_SAFE_REAL_SAMPLES = tuple(map(mp.mpf, ["1.1", "1.5", "2", "10"]))
ARCOSH_INTERIOR_CUT_SAMPLES = tuple(map(mp.mpf, ["-0.9", "-0.5", "-0.1", "0", "0.1", "0.5", "0.9"]))
ARCOSH_BELOW_NEGATIVE_SAMPLES = tuple(map(mp.mpf, ["-10", "-2", "-1.5", "-1.1"]))
ARCCOS_ISOLATION_SAMPLES = tuple(map(mp.mpf, ["-0.9", "-0.5", "-0.1", "0", "0.1", "0.5", "0.9"]))
SIDE_EPSILONS = tuple(map(mp.mpf, ["1e-6", "1e-12", "1e-30"]))

DomainName = Literal["ordinary-real", "interior-cut", "below-negative-cut", "side-of-cut"]
StageMode = Literal["direct-named", "derived-arcosh-direct-cos", "full-dependency-chain"]


@dataclass(frozen=True)
class ArcoshDiagnostic:
    backend: str
    domain: DomainName
    sample: str
    actual: str
    expected: str
    abs_error: str
    classification: str
    notes: str


@dataclass(frozen=True)
class ArccosIsolationRow:
    sample: str
    backend: str
    mode: StageMode
    first_arcosh: str
    cos_value: str
    final_value: str
    expected: str
    abs_error: str
    classification: str
    notes: str


def _samples_for_domain(domain: DomainName) -> tuple[mp.mpf, ...]:
    if domain == "ordinary-real":
        return ARCOSH_SAFE_REAL_SAMPLES
    if domain == "interior-cut":
        return ARCOSH_INTERIOR_CUT_SAMPLES
    if domain == "below-negative-cut":
        return ARCOSH_BELOW_NEGATIVE_SAMPLES
    raise ValueError(f"domain {domain!r} requires explicit side-of-cut samples")


def _classify_arcosh(sample: object, actual: object, expected: object) -> tuple[str, str]:
    z = mp.mpc(sample)
    base = classify_branch_offset(actual, expected, tol=mp.mpf("1e-30"))
    if base.classification == "match":
        return "exact-match", "matches principal acosh reference"
    if is_conjugate(actual, expected, tol=mp.mpf("1e-30")):
        return "conjugation", "opposite side of the same branch cut"
    if z.imag == 0 and z.real < -1:
        delta = mp.mpc(actual) - mp.mpc(expected)
        if mp.almosteq(delta, -mp.pi * mp.j, rel_eps=mp.mpf("1e-30"), abs_eps=mp.mpf("1e-30")):
            return "wrong-log-sheet", "derived witness misses the +i*pi principal acosh sheet below -1"
    if z.imag == 0 and -1 < z.real < 0:
        if mp.almosteq(abs(mp.im(actual)), mp.acos(abs(z.real)), rel_eps=mp.mpf("1e-30"), abs_eps=mp.mpf("1e-30")):
            return "wrong-square-root-sheet", "sqrt(x^2-1) factorization collapses to the acos(abs(x)) sheet"
    if z.imag == 0 and 0 < z.real < 1 and mp.im(actual) < 0 < mp.im(expected):
        return "branch-cut-side-mismatch", "LogLower selects the lower side on the interior cut"
    if base.classification == "log-sheet-offset":
        return "additive-2pi-i-offset", f"k={base.k}"
    if detect_pi_offset(actual, expected, tol=mp.mpf("1e-30")).classification == "pi-offset":
        return "additive-pi-offset", "real pi offset detected"
    if detect_log_sheet_offset(actual, expected, tol=mp.mpf("1e-30")).classification == "log-sheet-offset":
        return "additive-2pi-i-offset", "log sheet offset detected"
    return "unknown", base.residual


def derived_arcosh(x: object, backend: Backend = "mpmath_lower"):
    if backend == "numpy_principal":
        raise ValueError("numpy_principal is not implemented for arcosh branch diagnostics")
    return BranchEvaluator(backend).arcosh(x)


def diagnose_arcosh_sample(sample: object, backend: Backend, domain: DomainName) -> ArcoshDiagnostic:
    with mp.workdps(90):
        actual = derived_arcosh(sample, backend)
        expected = mp.acosh(sample)
        classification, notes = _classify_arcosh(sample, actual, expected)
        return ArcoshDiagnostic(
            backend=backend,
            domain=domain,
            sample=mp.nstr(sample, 18),
            actual=mp.nstr(actual, 18),
            expected=mp.nstr(expected, 18),
            abs_error=mp.nstr(abs(actual - expected), 18),
            classification=classification,
            notes=notes,
        )


def diagnose_arcosh_domain(domain: DomainName, backend: Backend = "mpmath_lower") -> list[ArcoshDiagnostic]:
    return [diagnose_arcosh_sample(sample, backend, domain) for sample in _samples_for_domain(domain)]


def side_of_cut_arcosh(samples: Iterable[object], backend: Backend = "mpmath_lower") -> list[ArcoshDiagnostic]:
    rows: list[ArcoshDiagnostic] = []
    for sample in samples:
        for eps in SIDE_EPSILONS:
            rows.append(diagnose_arcosh_sample(mp.mpc(sample, eps), backend, "side-of-cut"))
            rows.append(diagnose_arcosh_sample(mp.mpc(sample, -eps), backend, "side-of-cut"))
    return rows


def direct_named_arccos_witness(x: object):
    return mp.acosh(mp.cos(mp.acosh(x)))


def isolate_arccos_sample(sample: object, mode: StageMode, backend: Backend = "mpmath_lower") -> ArccosIsolationRow:
    with mp.workdps(90):
        if mode == "direct-named":
            first = mp.acosh(sample)
            cos_value = mp.cos(first)
            final = mp.acosh(cos_value)
        elif mode == "derived-arcosh-direct-cos":
            evaluator = BranchEvaluator(backend)
            first = evaluator.arcosh(sample)
            cos_value = mp.cos(first)
            final = evaluator.arcosh(cos_value)
        elif mode == "full-dependency-chain":
            evaluator = BranchEvaluator(backend)
            first = evaluator.arcosh(sample)
            cos_value = evaluator.cos(first)
            final = evaluator.arcosh(cos_value)
        else:
            raise ValueError(mode)
        expected = mp.acos(sample)
        base = classify_branch_offset(final, expected, tol=mp.mpf("1e-30"))
        if base.classification == "match":
            classification = "exact-match"
            notes = "matches principal acos reference"
        elif is_sign_flip(final, expected, tol=mp.mpf("1e-30")):
            classification = "sign-flip"
            notes = "final result is the opposite sign"
        elif mp.mpc(sample).imag == 0 and mp.mpc(sample).real < 0 and mp.almosteq(mp.re(final), mp.acos(abs(mp.re(sample))), rel_eps=mp.mpf("1e-30"), abs_eps=mp.mpf("1e-30")):
            classification = "acos-absolute-value-sheet"
            notes = "final result follows acos(abs(x))"
        else:
            classification = base.classification
            notes = base.residual
        return ArccosIsolationRow(
            sample=mp.nstr(sample, 18),
            backend=backend if mode != "direct-named" else "mpmath-direct",
            mode=mode,
            first_arcosh=mp.nstr(first, 18),
            cos_value=mp.nstr(cos_value, 18),
            final_value=mp.nstr(final, 18),
            expected=mp.nstr(expected, 18),
            abs_error=mp.nstr(abs(final - expected), 18),
            classification=classification,
            notes=notes,
        )


def isolate_arccos(mode: StageMode, backend: Backend = "mpmath_lower") -> list[ArccosIsolationRow]:
    return [isolate_arccos_sample(sample, mode, backend) for sample in ARCCOS_ISOLATION_SAMPLES]
