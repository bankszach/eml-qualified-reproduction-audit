"""Branch-aware numerical checks for dependency-chain witnesses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

import mpmath as mp

Backend = Literal["mpmath_principal", "mpmath_lower", "numpy_principal"]


BRANCH_SENSITIVE_PRIMITIVES = (
    "i",
    "pi",
    "cos",
    "sin",
    "tan",
    "arsinh",
    "arcosh",
    "arccos",
    "arcsin",
    "artanh",
    "arctan",
)


@dataclass(frozen=True)
class BranchCheckResult:
    primitive: str
    backend: Backend
    sample_domain: str
    passed: int
    failed: int
    xfail_expected: bool
    max_abs_error: str
    branch_notes: str
    extended_real_notes: str = ""

    @property
    def status(self) -> str:
        if self.passed == 0 and self.failed == 0:
            return "not-run"
        if self.failed == 0:
            return "passed"
        return "xfailed" if self.xfail_expected else "failed"


class BranchEvaluator:
    """Evaluate author dependency-chain witnesses with a selected EML log branch."""

    def __init__(self, backend: Backend):
        if backend not in {"mpmath_principal", "mpmath_lower"}:
            raise ValueError(f"unsupported BranchEvaluator backend: {backend}")
        self.backend = backend

    def _log_for_eml(self, z):
        z = self._snap_near_negative_real(z)
        if self.backend == "mpmath_lower":
            from eml_lab.backends.mpmath_lower_backend import log

            return log(z)
        return mp.log(z)

    def _snap_near_negative_real(self, z):
        c = mp.mpc(z)
        if c.real < 0 and abs(c.imag) <= mp.mpf("1e-50") * max(1, abs(c.real)):
            return mp.mpc(c.real, 0)
        return z

    def eml(self, x, y):
        return mp.exp(x) - self._log_for_eml(y)

    def exp(self, x):
        return self.eml(x, 1)

    def ln(self, x):
        return self.eml(1, self.exp(self.eml(1, x)))

    # Below this point the functions are direct dependency-chain witnesses
    # using already-established operations, not pure expanded EML trees.
    def half(self, x):
        return x / 2

    def inv(self, x):
        return 1 / x

    def hypot(self, x, y):
        return mp.sqrt(x * x + y * y)

    def i(self):
        return self.exp(self.half(self.ln(-1)))

    def pi(self):
        return self.ln(-1) / self.i()

    def cosh(self, x):
        return (self.exp(x) + self.exp(-x)) / 2

    def sinh(self, x):
        return self.eml(x, self.exp(self.cosh(x)))

    def tanh(self, x):
        return self.sinh(x) / self.cosh(x)

    def cos(self, x):
        return self.cosh(x / self.i())

    def sin(self, x):
        return self.cos(x - self.pi() / 2)

    def tan(self, x):
        return self.sin(x) / self.cos(x)

    def arsinh(self, x):
        return self.ln(x + self.hypot(-1, x))

    def arcosh(self, x):
        return self.arsinh(self.hypot(self.i(), x))

    def arccos(self, x):
        return self.arcosh(self.cos(self.arcosh(x)))

    def arcsin(self, x):
        return self.pi() / 2 - self.arccos(x)

    def artanh(self, x):
        return self.arsinh(self.inv(self.tan(self.arccos(x))))

    def arctan(self, x):
        return self.arcsin(self.tanh(self.arsinh(x)))


def samples_for(name: str) -> tuple[str, tuple[mp.mpf, ...]]:
    if name in {"i", "pi"}:
        return "constant dependency-chain behavior", ()
    if name in {"sin", "cos"}:
        return "real-domain calculator behavior", tuple(map(mp.mpf, ["-1.25", "-0.5", "0", "0.75", "1.25"]))
    if name == "tan":
        return "real-domain calculator behavior away from tangent poles", tuple(map(mp.mpf, ["-1.2", "-0.4", "0.3", "1.0"]))
    if name == "arsinh":
        return "real-domain calculator behavior", tuple(map(mp.mpf, ["-2", "-0.5", "0", "1.3"]))
    if name == "arcosh":
        return "real-domain calculator behavior x > 1", tuple(map(mp.mpf, ["1.1", "2", "5"]))
    if name in {"arcsin", "arccos"}:
        return "real-domain calculator behavior inside (-1, 1)", tuple(map(mp.mpf, ["-0.75", "-0.25", "0.25", "0.75"]))
    if name == "artanh":
        return "real-domain calculator behavior inside (-1, 1)", tuple(map(mp.mpf, ["-0.75", "-0.2", "0.2", "0.75"]))
    if name == "arctan":
        return "real-domain calculator behavior", tuple(map(mp.mpf, ["-5", "-1", "0", "1", "5"]))
    raise KeyError(name)


def expected_function(name: str) -> Callable:
    mapping = {
        "i": lambda: mp.j,
        "pi": lambda: mp.pi,
        "cos": mp.cos,
        "sin": mp.sin,
        "tan": mp.tan,
        "arsinh": mp.asinh,
        "arcosh": mp.acosh,
        "arccos": mp.acos,
        "arcsin": mp.asin,
        "artanh": mp.atanh,
        "arctan": mp.atan,
    }
    return mapping[name]


def evaluate_branch_primitive(name: str, backend: Backend, *, dps: int = 80) -> BranchCheckResult:
    if backend == "numpy_principal":
        return _evaluate_numpy_principal(name)

    evaluator = BranchEvaluator(backend)
    sample_domain, samples = samples_for(name)
    expected = expected_function(name)
    max_error = mp.mpf("0")
    passed = 0
    failed = 0

    with mp.workdps(dps):
        if not samples:
            got = getattr(evaluator, name)()
            want = expected()
            err = abs(got - want)
            max_error = max(max_error, err)
            if mp.almosteq(got, want, rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40")):
                passed += 1
            else:
                failed += 1
        else:
            for sample in samples:
                got = getattr(evaluator, name)(sample)
                want = expected(sample)
                err = abs(got - want)
                max_error = max(max_error, err)
                if mp.almosteq(got, want, rel_eps=mp.mpf("1e-35"), abs_eps=mp.mpf("1e-35")):
                    passed += 1
                else:
                    failed += 1

    return BranchCheckResult(
        primitive=name,
        backend=backend,
        sample_domain=sample_domain,
        passed=passed,
        failed=failed,
        xfail_expected=expected_to_fail(name, backend),
        max_abs_error=mp.nstr(max_error, 12),
        branch_notes=branch_note_for(name, backend),
        extended_real_notes=extended_real_note_for(name),
    )


def principal_expected_to_fail(name: str) -> bool:
    return expected_to_fail(name, "mpmath_principal")


def expected_to_fail(name: str, backend: Backend) -> bool:
    if name in {"arccos", "arcsin", "artanh", "arctan"}:
        return True
    return backend == "mpmath_principal" and name == "i"


def branch_note_for(name: str, backend: Backend) -> str:
    if name == "i":
        return "principal log returns -i for the author i witness; LogLower returns +i"
    if name == "pi":
        return "pi is sign-stable when log(-1) and i are constructed consistently"
    if backend == "mpmath_lower":
        return "direct dependency-chain witness evaluated with LogLower inside EML"
    return "direct dependency-chain witness evaluated with ordinary principal log inside EML"


def extended_real_note_for(name: str) -> str:
    if name in {"i", "pi"}:
        return "direct branch test uses generated -1; fully inlined construction inherits neg_one/log(0) risk"
    return "not required for this direct dependency-chain branch test"


def _evaluate_numpy_principal(name: str) -> BranchCheckResult:
    try:
        import numpy as np
    except Exception as exc:  # pragma: no cover
        return BranchCheckResult(name, "numpy_principal", "numpy unavailable", 0, 1, True, "nan", str(exc))

    sample_domain, samples = samples_for(name)

    def log_eml(z):
        return eml(1, exp(eml(1, z)))

    def eml(a, b):
        return np.exp(np.asarray(a, dtype=np.complex128)) - np.log(np.asarray(b, dtype=np.complex128))

    def exp(z):
        return eml(z, 1)

    def half(z):
        return z / 2

    def i_const():
        return exp(half(log_eml(-1)))

    def pi_const():
        return log_eml(-1) / i_const()

    funcs = {
        "i": lambda: i_const(),
        "pi": lambda: pi_const(),
        "cos": lambda x: np.cosh(x / i_const()),
        "sin": lambda x: np.cosh((x - pi_const() / 2) / i_const()),
        "tan": lambda x: np.cosh((x - pi_const() / 2) / i_const()) / np.cosh(x / i_const()),
    }
    if name not in funcs:
        return BranchCheckResult(
            primitive=name,
            backend="numpy_principal",
            sample_domain=sample_domain,
            passed=0,
            failed=1,
            xfail_expected=True,
            max_abs_error="nan",
            branch_notes="numpy principal check not implemented for this dependency-chain witness",
        )

    expected = expected_function(name)
    max_error = 0.0
    passed = 0
    failed = 0
    if not samples:
        got = funcs[name]()
        want = complex(expected())
        err = abs(complex(got) - want)
        max_error = max(max_error, err)
        if err < 1e-10:
            passed += 1
        else:
            failed += 1
    else:
        for sample in samples:
            got = funcs[name](complex(sample))
            want = complex(expected(sample))
            err = abs(complex(got) - want)
            max_error = max(max_error, err)
            if err < 1e-10:
                passed += 1
            else:
                failed += 1
    return BranchCheckResult(
        primitive=name,
        backend="numpy_principal",
        sample_domain=sample_domain,
        passed=passed,
        failed=failed,
        xfail_expected=expected_to_fail(name, "numpy_principal"),
        max_abs_error=f"{max_error:.3g}",
        branch_notes=branch_note_for(name, "numpy_principal"),
        extended_real_notes=extended_real_note_for(name),
    )


def summarize_results(results: list[BranchCheckResult]) -> dict[str, int]:
    return {
        "passed": sum(result.failed == 0 for result in results),
        "failed": sum(result.failed > 0 and not result.xfail_expected for result in results),
        "xfailed": sum(result.failed > 0 and result.xfail_expected for result in results),
    }
