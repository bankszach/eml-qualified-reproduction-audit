from eml_lab.verification import check_unary_positive_real
from eml_lab.witnesses import get_witness


def test_positive_real_numeric_checks_for_core_unary_witnesses():
    for name in ["exp", "ln"]:
        result = check_unary_positive_real(get_witness(name))
        assert result.status == "passed", result
        assert result.samples > 0

