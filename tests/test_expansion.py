import pytest

from eml_lab.expansion import ExpansionError, expand_witness, expr_stats, rpn_for, unresolved_dependencies


@pytest.mark.parametrize("name", ["ln", "sub", "minus", "add", "mul", "div"])
def test_expansion_produces_eml_ast(name):
    expr = expand_witness(name)
    stats = expr_stats(expr)
    assert stats.nodes > 0
    assert stats.leaves > 0
    assert stats.depth > 0
    assert rpn_for(name)
    assert unresolved_dependencies(name) == ()


def test_ln_rpn_is_known_core_witness():
    assert rpn_for("ln") == "11xE1EE"


def test_unknown_expansion_reports_readable_error():
    with pytest.raises(ExpansionError, match="no local expansion rule"):
        expand_witness("arcsin")

