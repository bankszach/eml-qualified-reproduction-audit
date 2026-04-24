from eml_lab.branch_verification import BRANCH_SENSITIVE_PRIMITIVES, evaluate_branch_primitive
from eml_lab.witnesses import get_witness


PASS_UNDER_LOGLOWER = {"i", "pi", "cos", "sin", "tan", "arsinh", "arcosh"}
BLOCKED_UNDER_LOGLOWER = {"arccos", "arcsin", "artanh", "arctan"}


def test_branch_sensitive_witnesses_have_metadata():
    for name in BRANCH_SENSITIVE_PRIMITIVES:
        witness = get_witness(name)
        assert isinstance(witness.requires_loglower, bool)
        assert isinstance(witness.principal_log_expected_to_fail, bool)
        assert witness.branch_failure_mode
        assert witness.safe_real_domain
        assert witness.extended_real_required is False


def test_i_and_pi_constant_branch_verdicts():
    principal_i = evaluate_branch_primitive("i", "mpmath_principal")
    lower_i = evaluate_branch_primitive("i", "mpmath_lower")
    principal_pi = evaluate_branch_primitive("pi", "mpmath_principal")
    lower_pi = evaluate_branch_primitive("pi", "mpmath_lower")

    assert principal_i.status == "xfailed"
    assert lower_i.status == "passed"
    assert principal_pi.status == "passed"
    assert lower_pi.status == "passed"


def test_loglower_branch_sensitive_real_domain_results():
    for name in PASS_UNDER_LOGLOWER:
        result = evaluate_branch_primitive(name, "mpmath_lower")
        assert result.status == "passed", result
        assert "dependency-chain" in result.branch_notes or name in {"i", "pi"}


def test_principal_log_results_are_kept_separate():
    expected_fail = evaluate_branch_primitive("i", "mpmath_principal")
    assert expected_fail.status == "xfailed"

    for name in PASS_UNDER_LOGLOWER - {"i"}:
        result = evaluate_branch_primitive(name, "mpmath_principal")
        assert result.status == "passed", result


def test_inverse_trig_chain_remains_branch_blocked_on_negative_real_samples():
    for name in BLOCKED_UNDER_LOGLOWER:
        result = evaluate_branch_primitive(name, "mpmath_lower")
        assert result.status == "xfailed", result
        assert result.passed > 0
        assert result.failed > 0


def test_numpy_principal_is_only_practical_subset():
    for name in ["i", "pi", "cos", "sin", "tan"]:
        result = evaluate_branch_primitive(name, "numpy_principal")
        assert result.status == "passed", result

    not_implemented = evaluate_branch_primitive("arccos", "numpy_principal")
    assert not_implemented.status == "xfailed"
    assert "not implemented" in not_implemented.branch_notes
