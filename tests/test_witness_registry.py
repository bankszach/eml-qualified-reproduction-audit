from eml_lab.table1 import TABLE1_PRIMITIVES
from eml_lab.witnesses import WITNESSES, table1_witnesses


ALLOWED_STATUSES = {
    "verified",
    "reproduced-numerically",
    "partially-reproduced",
    "blocked-by-source-gap",
    "blocked-by-branch-semantics",
    "failed",
    "not-yet-tested",
}


def test_registry_has_first_milestone_witnesses():
    assert {"e", "exp", "ln"}.issubset(WITNESSES)


def test_registry_has_every_table1_primitive():
    assert len(TABLE1_PRIMITIVES) == 36
    assert {item.canonical_name for item in TABLE1_PRIMITIVES} == set(table1_witnesses())


def test_registry_uses_controlled_statuses():
    for witness in WITNESSES.values():
        assert witness.symbolic_status in ALLOWED_STATUSES
        assert witness.numeric_status in ALLOWED_STATUSES
        assert witness.edge_case_status in ALLOWED_STATUSES
        assert witness.final_status in ALLOWED_STATUSES


def test_first_pure_eml_rpn_values_are_present():
    assert WITNESSES["e"].rpn == "11E"
    assert WITNESSES["exp"].rpn == "x1E"
    assert WITNESSES["ln"].rpn == "11xE1EE"


def test_branch_sensitive_status_fields_are_controlled():
    for name in ["i", "pi", "cos", "sin", "tan", "arsinh", "arcosh", "arccos", "arcsin", "artanh", "arctan"]:
        witness = WITNESSES[name]
        assert witness.principal_log_status in ALLOWED_STATUSES
        assert witness.loglower_status in ALLOWED_STATUSES
        assert witness.numpy_principal_status in ALLOWED_STATUSES
