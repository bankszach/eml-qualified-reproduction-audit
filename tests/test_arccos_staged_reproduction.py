from collections import Counter

import mpmath as mp

from eml_lab.arccos_staged_reproduction import ARCCOS_STAGE_SAMPLES, arcsin_internal_helper, arctan_internal_helper, artanh_internal_helper, diagnose_all_variants


def test_arccos_stage_sample_set_is_iteration6_set():
    assert tuple(map(str, ARCCOS_STAGE_SAMPLES)) == ("-0.9", "-0.5", "-0.1", "-1.0e-12", "0.0", "1.0e-12", "0.1", "0.5", "0.9")


def test_named_and_internal_helper_arccos_variants_pass():
    results = diagnose_all_variants("mpmath_lower")
    for variant in ["named", "internal-helper", "internal-first-derived-final"]:
        rows = results[variant]
        assert Counter(row.classification for row in rows) == {"exact-match": len(ARCCOS_STAGE_SAMPLES)}


def test_fully_derived_arccos_variant_still_fails_on_negative_interior_samples():
    results = diagnose_all_variants("mpmath_lower")["derived"]
    negative = [row for row in results if mp.re(mp.mpc(row.sample)) < 0]
    nonnegative = [row for row in results if mp.re(mp.mpc(row.sample)) >= 0]
    assert Counter(row.classification for row in negative) == {"acos-absolute-value-sheet": 4}
    assert all(row.classification == "exact-match" for row in nonnegative)


def test_internal_final_alone_is_not_enough():
    results = diagnose_all_variants("mpmath_lower")["derived-first-internal-final"]
    negative = [row for row in results if mp.re(mp.mpc(row.sample)) < 0]
    assert all(row.classification == "acos-absolute-value-sheet" for row in negative)


def test_inherited_blockers_pass_only_in_diagnostic_helper_chain():
    with mp.workdps(80):
        for sample in ARCCOS_STAGE_SAMPLES:
            assert mp.almosteq(arcsin_internal_helper(sample), mp.asin(sample), rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40"))
            assert mp.almosteq(artanh_internal_helper(sample), mp.atanh(sample), rel_eps=mp.mpf("1e-35"), abs_eps=mp.mpf("1e-35"))
        for sample in map(mp.mpf, ["-10", "-2", "-1", "-0.5", "-1e-12", "0", "1e-12", "0.5", "1", "2", "10"]):
            assert mp.almosteq(arctan_internal_helper(sample), mp.atan(sample), rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40"))
