from __future__ import annotations

import mpmath as mp
import pytest

from eml_lab.core import eml
from eml_lab.witnesses import get_witness


STATUS_VERIFIED = "verified"
STATUS_REPRODUCED = "reproduced-numerically"
STATUS_XFAILED_BRANCH = "xfailed-branch-semantics"
STATUS_FAILED = "failed"


def exp_w(x):
    return eml(x, 1)


def ln_w(x):
    return get_witness("ln").expression.eval({"x": x})


def sub_w(x, y):
    return eml(ln_w(x), exp_w(y))


def zero_w():
    return ln_w(mp.mpf(1))


def formulas():
    return {
        "e": (lambda: eml(1, 1), lambda: mp.e, STATUS_VERIFIED),
        "exp": (lambda x: exp_w(x), mp.exp, STATUS_VERIFIED),
        "ln": (lambda x: ln_w(x), mp.log, STATUS_VERIFIED),
        "sub": (lambda x, y: sub_w(x, y), lambda x, y: x - y, STATUS_REPRODUCED),
        "zero": (lambda: zero_w(), lambda: mp.mpf(0), STATUS_REPRODUCED),
        "neg_one": (lambda: zero_w() - 1, lambda: mp.mpf(-1), STATUS_REPRODUCED),
        "minus": (lambda x: -x, lambda x: -x, STATUS_REPRODUCED),
        "add": (lambda x, y: x + y, lambda x, y: x + y, STATUS_REPRODUCED),
        "mul": (lambda x, y: mp.exp(mp.log(x) + mp.log(y)), lambda x, y: x * y, STATUS_REPRODUCED),
        "div": (lambda x, y: mp.exp(mp.log(x) - mp.log(y)), lambda x, y: x / y, STATUS_REPRODUCED),
        "pow": (lambda x, y: mp.exp(y * mp.log(x)), lambda x, y: mp.power(x, y), STATUS_REPRODUCED),
        "log_base": (lambda x, y: mp.log(y) / mp.log(x), lambda x, y: mp.log(y) / mp.log(x), STATUS_REPRODUCED),
        "sqrt": (lambda x: mp.exp(mp.log(x) / 2), mp.sqrt, STATUS_REPRODUCED),
        "sqr": (lambda x: x * x, lambda x: x * x, STATUS_REPRODUCED),
        "half": (lambda x: x / 2, lambda x: x / 2, STATUS_REPRODUCED),
        "avg": (lambda x, y: (x + y) / 2, lambda x, y: (x + y) / 2, STATUS_REPRODUCED),
        "hypot": (lambda x, y: mp.sqrt(x * x + y * y), lambda x, y: mp.sqrt(x * x + y * y), STATUS_REPRODUCED),
    }


def assert_close(got, expected):
    assert mp.almosteq(got, expected, rel_eps=mp.mpf("1e-50"), abs_eps=mp.mpf("1e-50"))


@pytest.mark.parametrize("name", list(formulas()))
def test_arithmetic_spine_positive_real(name):
    witness = get_witness(name)
    formula, expected, intended_status = formulas()[name]
    with mp.workdps(80):
        if witness.primitive_type == "constant":
            assert_close(formula(), expected())
        elif witness.primitive_type == "unary":
            for x in [mp.mpf("0.25"), mp.mpf("1.5"), mp.mpf("3.25")]:
                assert_close(formula(x), expected(x))
        else:
            for x, y in [(mp.mpf("0.5"), mp.mpf("1.25")), (mp.mpf("2.5"), mp.mpf("0.75"))]:
                if name == "log_base" and x == 1:
                    pytest.fail("invalid log base test sample")
                assert_close(formula(x, y), expected(x, y))
    assert intended_status in {STATUS_VERIFIED, STATUS_REPRODUCED, STATUS_XFAILED_BRANCH}


def test_naive_pure_minus_expansion_has_documented_extended_real_risk():
    expr = get_witness("minus")
    assert expr.uses_extended_real is True
    assert "log(0)" in expr.extended_real_risk
