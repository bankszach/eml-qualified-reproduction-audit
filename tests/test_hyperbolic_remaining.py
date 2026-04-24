import mpmath as mp
import pytest

from eml_lab.branch_verification import BranchEvaluator
from eml_lab.witnesses import get_witness

REAL_SAMPLES = tuple(map(mp.mpf, ["-3", "-1", "-0.5", "0", "0.5", "1", "3"]))


def sigmoid_witness(ev: BranchEvaluator, x):
    return ev.inv(ev.eml(-x, ev.exp(-1)))


def dependency_value(name: str, ev: BranchEvaluator, x):
    if name == "sigmoid":
        return sigmoid_witness(ev, x)
    return getattr(ev, name)(x)


@pytest.mark.parametrize("name", ["sigmoid", "cosh", "sinh", "tanh"])
def test_remaining_hyperbolic_real_domain_dependency_chain(name):
    witness = get_witness(name)
    ev = BranchEvaluator("mpmath_lower")
    with mp.workdps(80):
        for x in REAL_SAMPLES:
            got = dependency_value(name, ev, x)
            want = witness.reference(x)
            assert mp.almosteq(got, want, rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40")), (name, x, got, want)


def test_remaining_hyperbolic_test_scope_is_documented():
    for name in ["sigmoid", "cosh", "sinh", "tanh"]:
        witness = get_witness(name)
        assert witness.dependency_witness
        assert witness.reference is not None
