import mpmath as mp
import pytest

from eml_lab.arcosh_branch_diagnostics import (
    ARCOSH_BELOW_NEGATIVE_SAMPLES,
    ARCOSH_INTERIOR_CUT_SAMPLES,
    ARCOSH_SAFE_REAL_SAMPLES,
    ARCCOS_ISOLATION_SAMPLES,
    SIDE_EPSILONS,
    diagnose_arcosh_domain,
    direct_named_arccos_witness,
    isolate_arccos,
    side_of_cut_arcosh,
)
from eml_lab.witnesses import get_witness


def test_arcosh_safe_real_domain_still_matches_principal():
    for backend in ["mpmath_principal", "mpmath_lower"]:
        rows = diagnose_arcosh_domain("ordinary-real", backend)
        assert len(rows) == len(ARCOSH_SAFE_REAL_SAMPLES)
        assert all(row.classification == "exact-match" for row in rows)


def test_arcosh_interior_cut_exposes_nonprincipal_dependency_sheet():
    lower_rows = diagnose_arcosh_domain("interior-cut", "mpmath_lower")
    negative_rows = [row for row in lower_rows if mp.re(mp.mpc(row.sample)) < 0]
    nonnegative_rows = [row for row in lower_rows if mp.re(mp.mpc(row.sample)) >= 0]
    assert negative_rows
    assert all(row.classification == "wrong-square-root-sheet" for row in negative_rows)
    assert all(row.classification == "exact-match" for row in nonnegative_rows)

    principal_rows = diagnose_arcosh_domain("interior-cut", "mpmath_principal")
    assert any(row.classification == "wrong-square-root-sheet" for row in principal_rows)
    assert any(row.classification == "conjugation" for row in principal_rows)


def test_arcosh_below_negative_one_misses_log_sheet():
    for backend in ["mpmath_principal", "mpmath_lower"]:
        rows = diagnose_arcosh_domain("below-negative-cut", backend)
        assert len(rows) == len(ARCOSH_BELOW_NEGATIVE_SAMPLES)
        assert all(row.classification == "wrong-log-sheet" for row in rows)


def test_arcosh_side_of_cut_probes_exist():
    rows = side_of_cut_arcosh([mp.mpf("-0.5")], "mpmath_lower")
    assert len(rows) == 2 * len(SIDE_EPSILONS)
    assert {row.domain for row in rows} == {"side-of-cut"}
    assert all(row.classification for row in rows)


def test_direct_named_arccos_witness_passes():
    with mp.workdps(80):
        for sample in ARCCOS_ISOLATION_SAMPLES:
            got = direct_named_arccos_witness(sample)
            want = mp.acos(sample)
            assert mp.almosteq(got, want, rel_eps=mp.mpf("1e-40"), abs_eps=mp.mpf("1e-40"))


@pytest.mark.parametrize("mode", ["derived-arcosh-direct-cos", "full-dependency-chain"])
def test_arccos_isolation_fails_after_derived_arcosh_enters(mode):
    rows = isolate_arccos(mode, "mpmath_lower")
    negative_rows = [row for row in rows if mp.re(mp.mpc(row.sample)) < 0]
    positive_rows = [row for row in rows if mp.re(mp.mpc(row.sample)) >= 0]
    assert negative_rows
    assert all(row.classification == "acos-absolute-value-sheet" for row in negative_rows)
    assert all(row.classification == "exact-match" for row in positive_rows)


def test_iteration5_witness_metadata_exists():
    arcosh = get_witness("arcosh")
    for field in [
        "ordinary_real_domain_status",
        "internal_branch_cut_status",
        "interval_neg1_1_status",
        "below_negative_one_status",
        "safe_as_arccos_dependency",
        "outward_domain_status",
        "internal_compositional_status",
        "compositionally_unsafe_domains",
        "principal_arcosh_helper_source_status",
    ]:
        assert hasattr(arcosh, field)
        assert getattr(arcosh, field) not in {"", None}
    assert arcosh.used_in_arccos_internal_interval is True
    assert arcosh.principal_arcosh_helper_available is True

    for name in ["arccos", "arcsin", "artanh", "arctan"]:
        witness = get_witness(name)
        for field in [
            "root_blocker",
            "inherited_from",
            "branch_dependency",
            "repair_attempted",
            "repair_status",
            "source_justification",
            "source_chain_type",
            "named_function_reproduction_status",
            "dependency_chain_reproduction_status",
            "internal_helper_reproduction_status",
            "final_branch_verdict",
        ]:
            assert hasattr(witness, field)
            assert getattr(witness, field) not in {"", None}
