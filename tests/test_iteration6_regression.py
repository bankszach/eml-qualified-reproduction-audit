import mpmath as mp

from eml_lab.branch_verification import BranchEvaluator, evaluate_branch_primitive
from eml_lab.core import eml
from eml_lab.witnesses import get_witness


def test_iteration6_core_and_arithmetic_regression():
    with mp.workdps(80):
        assert mp.almosteq(eml(1, 1), mp.e, rel_eps=mp.mpf("1e-50"), abs_eps=mp.mpf("1e-50"))
        for x in [mp.mpf("0.25"), mp.mpf("1.5"), mp.mpf("3.25")]:
            assert mp.almosteq(eml(x, 1), mp.exp(x), rel_eps=mp.mpf("1e-50"), abs_eps=mp.mpf("1e-50"))
            assert mp.almosteq(get_witness("ln").expression.eval({"x": x}), mp.log(x), rel_eps=mp.mpf("1e-50"), abs_eps=mp.mpf("1e-50"))

        ev = BranchEvaluator("mpmath_lower")
        for x, y in [(mp.mpf("0.5"), mp.mpf("1.25")), (mp.mpf("2.5"), mp.mpf("0.75"))]:
            assert mp.almosteq(ev.eml(ev.ln(x), ev.exp(y)), x - y, rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40"))
            assert mp.almosteq(mp.exp(mp.log(x) + mp.log(y)), x * y, rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40"))
            assert mp.almosteq(mp.exp(mp.log(x) - mp.log(y)), x / y, rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40"))


def test_iteration6_branch_regression():
    for name in ["i", "pi", "sin", "cos", "tan", "arsinh", "arcosh"]:
        assert evaluate_branch_primitive(name, "mpmath_lower").status == "passed"


def test_iteration6_remaining_hyperbolic_regression():
    ev = BranchEvaluator("mpmath_lower")
    with mp.workdps(80):
        for x in map(mp.mpf, ["-3", "-1", "-0.5", "0", "0.5", "1", "3"]):
            sigmoid = ev.inv(ev.eml(-x, ev.exp(-1)))
            assert mp.almosteq(sigmoid, 1 / (1 + mp.exp(-x)), rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40"))
            assert mp.almosteq(ev.cosh(x), mp.cosh(x), rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40"))
            assert mp.almosteq(ev.sinh(x), mp.sinh(x), rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40"))
            assert mp.almosteq(ev.tanh(x), mp.tanh(x), rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40"))
