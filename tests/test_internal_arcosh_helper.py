import mpmath as mp

from eml_lab.arcosh_branch_diagnostics import ARCOSH_BELOW_NEGATIVE_SAMPLES, ARCOSH_INTERIOR_CUT_SAMPLES, ARCOSH_SAFE_REAL_SAMPLES, SIDE_EPSILONS
from eml_lab.branch_verification import BranchEvaluator
from eml_lab.internal_branches import principal_arcosh_internal
from eml_lab.witnesses import WITNESSES


def test_principal_arcosh_internal_matches_mpmath_acosh_on_iteration5_samples():
    samples = ARCOSH_SAFE_REAL_SAMPLES + ARCOSH_INTERIOR_CUT_SAMPLES + ARCOSH_BELOW_NEGATIVE_SAMPLES
    with mp.workdps(80):
        for sample in samples:
            assert mp.almosteq(principal_arcosh_internal(sample), mp.acosh(sample), rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40")), sample


def test_principal_arcosh_internal_matches_side_of_cut_probes():
    with mp.workdps(80):
        for real in [mp.mpf("-2"), mp.mpf("-0.5"), mp.mpf("0.5")]:
            for eps in SIDE_EPSILONS:
                for sign in [1, -1]:
                    sample = mp.mpc(real, sign * eps)
                    assert mp.almosteq(principal_arcosh_internal(sample), mp.acosh(sample), rel_eps=mp.mpf("1e-35"), abs_eps=mp.mpf("1e-35")), sample


def test_internal_helper_kept_separate_from_derived_witness():
    ev = BranchEvaluator("mpmath_lower")
    with mp.workdps(80):
        for sample in [mp.mpf("-0.5"), mp.mpf("-2")]:
            assert not mp.almosteq(ev.arcosh(sample), mp.acosh(sample), rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40"))
            assert mp.almosteq(principal_arcosh_internal(sample), mp.acosh(sample), rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40"))


def test_diagnostic_helper_is_not_recorded_as_verified_witness_path():
    arcosh = WITNESSES["arcosh"]
    arccos = WITNESSES["arccos"]

    assert arcosh.principal_arcosh_helper_available is True
    assert "diagnostic-only" in arcosh.principal_arcosh_helper_source_status
    assert "compositionally-unsafe" in arcosh.internal_compositional_status

    assert arccos.final_status == "partially-reproduced"
    assert arccos.dependency_chain_reproduction_status.startswith("fails")
    assert "diagnostic" in arccos.internal_helper_reproduction_status
    assert arccos.final_branch_verdict.startswith("diagnostic-only repair")
