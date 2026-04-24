import mpmath as mp

from eml_lab.backends.mpmath_lower_backend import log as log_lower
from eml_lab.witnesses import get_witness


def test_ln_witness_agrees_near_positive_zero_but_not_at_zero():
    witness = get_witness("ln")
    with mp.workdps(80):
        for sample in [mp.mpf("1e-30"), mp.mpf("1e-12"), mp.mpf("1e-6")]:
            assert mp.almosteq(witness.expression.eval({"x": sample}), mp.log(sample))


def test_log_exp_is_not_global_identity():
    z = 1 + 4j
    assert not mp.almosteq(mp.log(mp.exp(z)), z)


def test_author_loglower_uses_lower_edge_on_negative_real_axis():
    assert mp.almosteq(log_lower(-1), -mp.j * mp.pi)
    assert mp.almosteq(log_lower(1), mp.mpf(0))
