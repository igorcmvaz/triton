import pytest

from netuno.core.report_service import normalize_report_type


@pytest.mark.parametrize(
    ("alias", "canonical"),
    [
        ("executive", "economic"),
        ("economic", "economic"),
        ("esg", "environmental"),
        ("lca", "environmental"),
        ("scientific", "research"),
    ],
)
def test_report_aliases_are_shared(alias, canonical):
    assert normalize_report_type(alias) == canonical


def test_invalid_report_type_is_rejected():
    with pytest.raises(ValueError):
        normalize_report_type("inventado")
