"""Verification helpers for witness expressions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import mpmath as mp
import sympy as sp

from eml_lab.ast import Expr
from eml_lab.domains import POSITIVE_REAL_SAMPLES
from eml_lab.witnesses import Witness


@dataclass(frozen=True)
class CheckResult:
    primitive: str
    backend: str
    status: str
    samples: int
    max_abs_error: str
    notes: str = ""


def almost_equal(a: object, b: object, *, tol: mp.mpf | None = None) -> bool:
    tol = tol or mp.mpf("1e-40")
    return abs(a - b) <= tol * max(1, abs(a), abs(b))


def check_unary_positive_real(
    witness: Witness,
    samples: Iterable[float] = POSITIVE_REAL_SAMPLES,
    *,
    dps: int = 80,
) -> CheckResult:
    if witness.expression is None or witness.reference is None:
        return CheckResult(witness.primitive, "mpmath", "skipped", 0, "nan", "missing expression/reference")

    with mp.workdps(dps):
        max_err = mp.mpf("0")
        count = 0
        for sample in samples:
            got = witness.expression.eval({"x": mp.mpf(sample)}, backend="mpmath")
            expected = witness.reference(mp.mpf(sample))
            err = abs(got - expected)
            max_err = max(max_err, err)
            count += 1
            if not almost_equal(got, expected):
                return CheckResult(witness.primitive, "mpmath", "failed", count, mp.nstr(max_err), f"sample={sample}")

    return CheckResult(witness.primitive, "mpmath", "passed", count, mp.nstr(max_err))


def sympy_simplifies_to(expr: Expr, expected: object, *, assumptions: str = "") -> bool:
    x = sp.symbols("x", positive=True) if assumptions == "positive-real" else sp.symbols("x")
    got = expr.eval({"x": x}, backend="sympy")
    return sp.simplify(got - expected) == 0
