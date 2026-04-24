import mpmath as mp
import sympy as sp

from eml_lab.ast import EML, ONE, Var, parse_rpn
from eml_lab.core import eml
from eml_lab.verification import check_unary_positive_real, sympy_simplifies_to
from eml_lab.witnesses import get_witness


def test_e_identity_mpmath():
    with mp.workdps(80):
        assert mp.almosteq(eml(1, 1), mp.e)


def test_exp_identity_mpmath():
    witness = get_witness("exp")
    result = check_unary_positive_real(witness)
    assert result.status == "passed"


def test_ln_identity_mpmath_positive_reals():
    witness = get_witness("ln")
    result = check_unary_positive_real(witness)
    assert result.status == "passed"


def test_exp_identity_sympy():
    x = sp.symbols("x")
    assert sympy_simplifies_to(get_witness("exp").expression, sp.exp(x))


def test_ln_identity_sympy_positive_real():
    x = sp.symbols("x", positive=True)
    assert sympy_simplifies_to(get_witness("ln").expression, sp.log(x), assumptions="positive-real")


def test_rpn_ln_example_round_trips():
    expr = EML(ONE, EML(EML(ONE, Var("x")), ONE))
    assert expr.to_rpn() == "11xE1EE"
    assert parse_rpn("11xE1EE") == expr

