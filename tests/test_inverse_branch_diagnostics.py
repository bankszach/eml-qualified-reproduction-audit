import mpmath as mp
import pytest

from eml_lab.inverse_branch_diagnostics import (
    ARCSIN_ARCCOS_ARTANH_SAMPLES,
    ARCTAN_SAMPLES,
    BLOCKED_INVERSE_PRIMITIVES,
    SIDE_EPSILONS,
    diagnose_real_samples,
    side_of_cut_probes,
    summarize_classifications,
)
from eml_lab.witnesses import get_witness


def test_deterministic_sample_sets_are_fixed():
    assert tuple(map(str, ARCSIN_ARCCOS_ARTANH_SAMPLES)) == ("-0.9", "-0.5", "-0.1", "-1.0e-12", "0.0", "1.0e-12", "0.1", "0.5", "0.9")
    assert tuple(map(str, ARCTAN_SAMPLES)) == ("-10.0", "-2.0", "-1.0", "-0.5", "-1.0e-12", "0.0", "1.0e-12", "0.5", "1.0", "2.0", "10.0")
    assert tuple(map(str, SIDE_EPSILONS)) == ("1.0e-6", "1.0e-12", "1.0e-30")


def test_arccos_negative_samples_are_square_root_sheet_flip():
    rows = diagnose_real_samples("arccos", "mpmath_lower")
    negative_rows = [row for row in rows if mp.re(mp.mpc(row.sample)) < 0]
    assert negative_rows
    assert all(row.classification == "square-root-sheet-flip/composed-branch-cut" for row in negative_rows)
    assert all(row.square_root_sheet_flip for row in negative_rows)


@pytest.mark.parametrize("name", ["arcsin", "artanh", "arctan"])
def test_dependent_inverse_functions_sign_flip_on_negative_reals(name):
    rows = diagnose_real_samples(name, "mpmath_lower")
    negative_rows = [row for row in rows if mp.re(mp.mpc(row.sample)) < 0]
    assert negative_rows
    assert all(row.classification == "sign-flip" for row in negative_rows)
    assert all(row.sign_flip for row in negative_rows)


@pytest.mark.parametrize("name", BLOCKED_INVERSE_PRIMITIVES)
def test_positive_real_samples_match_principal_reference(name):
    rows = diagnose_real_samples(name, "mpmath_lower")
    positive_rows = [row for row in rows if mp.re(mp.mpc(row.sample)) > 0]
    assert positive_rows
    assert all(row.classification == "match" for row in positive_rows)


def test_side_of_cut_probes_do_not_silently_skip():
    rows = side_of_cut_probes("arccos", [mp.mpf("-0.5")], "mpmath_lower")
    assert len(rows) == 2 * len(SIDE_EPSILONS)
    assert {row.side for row in rows} == {"upper", "lower"}
    assert all(row.sample for row in rows)


def test_four_blockers_have_iteration4_metadata():
    required = [
        "requires_signed_zero_or_side_of_cut",
        "requires_square_root_branch_control",
        "requires_mathematica_branch_rules",
        "failure_region",
        "observed_failure_mode",
        "unwinding_offset_observed",
        "author_reference_status",
        "python_reproduction_status",
        "unsafe_real_domain",
        "branch_sheet_notes",
    ]
    for name in BLOCKED_INVERSE_PRIMITIVES:
        witness = get_witness(name)
        for field in required:
            assert hasattr(witness, field)
            assert getattr(witness, field) not in {"", None}


def test_summary_counts_classifications():
    assert summarize_classifications("arccos", "mpmath_lower")["square-root-sheet-flip/composed-branch-cut"] == 4
    assert summarize_classifications("arcsin", "mpmath_lower")["sign-flip"] == 4
