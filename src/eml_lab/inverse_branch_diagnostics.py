"""Branch-sheet diagnostics for inverse-function witnesses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

import mpmath as mp

from eml_lab.branch_verification import Backend, BranchEvaluator
from eml_lab.unwinding import classify_branch_offset, detect_half_pi_offset, detect_log_sheet_offset, detect_pi_offset, is_conjugate, is_sign_flip

BlockedPrimitive = Literal["arccos", "arcsin", "artanh", "arctan"]
Side = Literal["real", "upper", "lower"]

BLOCKED_INVERSE_PRIMITIVES: tuple[BlockedPrimitive, ...] = ("arccos", "arcsin", "artanh", "arctan")
ARCSIN_ARCCOS_ARTANH_SAMPLES = tuple(map(mp.mpf, ["-0.9", "-0.5", "-0.1", "-1e-12", "0", "1e-12", "0.1", "0.5", "0.9"]))
ARCTAN_SAMPLES = tuple(map(mp.mpf, ["-10", "-2", "-1", "-0.5", "-1e-12", "0", "1e-12", "0.5", "1", "2", "10"]))
SIDE_EPSILONS = tuple(map(mp.mpf, ["1e-6", "1e-12", "1e-30"]))


@dataclass(frozen=True)
class InverseBranchDiagnostic:
    primitive: str
    backend: Backend
    sample_domain: str
    sample: str
    side: Side
    eps: str
    actual: str
    expected: str
    abs_error: str
    sign_flip: bool
    conjugation: bool
    pi_offset: int | None
    half_pi_offset: int | None
    log_sheet_offset: int | None
    square_root_sheet_flip: bool
    classification: str
    branch_notes: str


def deterministic_samples(name: BlockedPrimitive) -> tuple[mp.mpf, ...]:
    if name == "arctan":
        return ARCTAN_SAMPLES
    return ARCSIN_ARCCOS_ARTANH_SAMPLES


def reference_value(name: BlockedPrimitive, z: object):
    refs = {
        "arccos": mp.acos,
        "arcsin": mp.asin,
        "artanh": mp.atanh,
        "arctan": mp.atan,
    }
    return refs[name](z)


def dependency_value(name: BlockedPrimitive, z: object, backend: Backend = "mpmath_lower"):
    if backend == "numpy_principal":
        raise ValueError("numpy_principal is not implemented for inverse branch diagnostics")
    evaluator = BranchEvaluator(backend)
    return getattr(evaluator, name)(z)


def _looks_like_square_root_sheet_flip(name: str, sample: object, actual: object, expected: object, classification: str) -> bool:
    if name != "arccos":
        return False
    z = mp.mpc(sample)
    if abs(z.imag) > mp.mpf("1e-40") or z.real >= 0:
        return False
    if classification == "match":
        return False
    return mp.almosteq(mp.re(actual), mp.acos(abs(z.real)), rel_eps=mp.mpf("1e-30"), abs_eps=mp.mpf("1e-30"))


def _classify(name: str, sample: object, actual: object, expected: object) -> tuple[str, str, bool]:
    base = classify_branch_offset(actual, expected)
    square_root_sheet_flip = _looks_like_square_root_sheet_flip(name, sample, actual, expected, base.classification)
    if square_root_sheet_flip:
        return "square-root-sheet-flip/composed-branch-cut", "arccos witness follows acos(abs(x)) on negative real samples", True
    if base.classification == "sign-flip":
        return "sign-flip", "dependency chain returns the odd-function sign from the wrong arccos sheet", False
    if base.classification == "match":
        return "match", "matches DLMF/principal real-domain reference", False
    if base.classification in {"pi-offset", "half-pi-offset", "log-sheet-offset", "conjugation"}:
        return base.classification, f"offset detected: {base}", False
    return "unclassified-branch-offset", base.residual, False


def diagnose_sample(name: BlockedPrimitive, sample: object, backend: Backend = "mpmath_lower", *, side: Side = "real", eps: object = 0) -> InverseBranchDiagnostic:
    with mp.workdps(90):
        got = dependency_value(name, sample, backend)
        want = reference_value(name, sample)
        classification, notes, square_root_sheet_flip = _classify(name, sample, got, want)
        pi_offset = detect_pi_offset(got, want).k
        half_pi_offset = detect_half_pi_offset(got, want).k
        log_sheet_offset = detect_log_sheet_offset(got, want).k
        return InverseBranchDiagnostic(
            primitive=name,
            backend=backend,
            sample_domain="real-domain calculator behavior" if side == "real" else "side-of-cut probe",
            sample=mp.nstr(sample, 18),
            side=side,
            eps=mp.nstr(eps, 8),
            actual=mp.nstr(got, 18),
            expected=mp.nstr(want, 18),
            abs_error=mp.nstr(abs(got - want), 18),
            sign_flip=is_sign_flip(got, want),
            conjugation=is_conjugate(got, want),
            pi_offset=pi_offset,
            half_pi_offset=half_pi_offset,
            log_sheet_offset=log_sheet_offset,
            square_root_sheet_flip=square_root_sheet_flip,
            classification=classification,
            branch_notes=notes,
        )


def diagnose_real_samples(name: BlockedPrimitive, backend: Backend = "mpmath_lower") -> list[InverseBranchDiagnostic]:
    return [diagnose_sample(name, sample, backend) for sample in deterministic_samples(name)]


def side_of_cut_probes(name: BlockedPrimitive, real_samples: Iterable[object] | None = None, backend: Backend = "mpmath_lower") -> list[InverseBranchDiagnostic]:
    samples = tuple(real_samples) if real_samples is not None else deterministic_samples(name)
    rows: list[InverseBranchDiagnostic] = []
    for sample in samples:
        for eps in SIDE_EPSILONS:
            rows.append(diagnose_sample(name, mp.mpc(sample, eps), backend, side="upper", eps=eps))
            rows.append(diagnose_sample(name, mp.mpc(sample, -eps), backend, side="lower", eps=eps))
    return rows


def summarize_classifications(name: BlockedPrimitive, backend: Backend = "mpmath_lower") -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in diagnose_real_samples(name, backend):
        counts[row.classification] = counts.get(row.classification, 0) + 1
    return counts
