import mpmath as mp

from eml_lab.backends.mpmath_lower_backend import log as log_lower


def test_loglower_minus_one_is_lower_edge():
    assert mp.almosteq(mp.log(-1), mp.j * mp.pi)
    assert mp.almosteq(log_lower(-1), -mp.j * mp.pi)


def test_loglower_agrees_with_principal_away_from_negative_real_cut():
    for z in [1, 2 + 3j, -1 + 0.25j, -1 - 0.25j]:
        assert mp.almosteq(log_lower(z), mp.log(z))


def test_loglower_above_and_below_negative_axis():
    eps = mp.mpf("1e-30")
    above = log_lower(-1 + eps * mp.j)
    below = log_lower(-1 - eps * mp.j)
    assert above.imag > 0
    assert below.imag < 0
    assert mp.almosteq(above, mp.log(-1 + eps * mp.j))
    assert mp.almosteq(below, mp.log(-1 - eps * mp.j))


def test_loglower_zero_and_infinity_behavior_is_mpmath_extended():
    zero = log_lower(0)
    pos_inf = log_lower(mp.inf)
    neg_inf = log_lower(-mp.inf)
    assert mp.isinf(zero) and zero < 0
    assert mp.isinf(pos_inf) and pos_inf > 0
    assert mp.isinf(neg_inf.real) and neg_inf.imag < 0

