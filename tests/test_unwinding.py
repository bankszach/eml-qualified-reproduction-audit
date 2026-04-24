import mpmath as mp

from eml_lab.unwinding import classify_branch_offset, detect_half_pi_offset, detect_log_sheet_offset, detect_pi_offset, is_conjugate, is_sign_flip


def test_detects_log_sheet_offsets():
    expected = mp.mpc("1.25", "-0.5")
    actual = expected + 2 * mp.pi * mp.j * 3
    result = detect_log_sheet_offset(actual, expected)
    assert result.classification == "log-sheet-offset"
    assert result.k == 3


def test_detects_pi_offsets():
    result = detect_pi_offset(mp.pi * 2, 0)
    assert result.classification == "pi-offset"
    assert result.k == 2


def test_detects_half_pi_offsets():
    result = detect_half_pi_offset(mp.pi / 2, 0)
    assert result.classification == "half-pi-offset"
    assert result.k == 1


def test_detects_sign_flip_and_conjugation():
    assert is_sign_flip(mp.mpf("0.5"), mp.mpf("-0.5"))
    assert is_conjugate(mp.mpc(1, -2), mp.mpc(1, 2))
    assert classify_branch_offset(mp.mpf("0.5"), mp.mpf("-0.5")).classification == "sign-flip"
