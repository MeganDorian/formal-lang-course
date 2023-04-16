import pytest

from project.task06.wcnf import load_cfg
from project.task07.ecfg import ECFG
from project.task07.rsm import RSM


@pytest.mark.parametrize(
    "filename, expectedfile",
    [
        ("tests/ecfg/ecfg", "tests/ecfg/ecfg-result"),
        ("tests/ecfg/ecfg-2", "tests/ecfg/ecfg-result-2"),
    ],
)
def test_from_ecfg(filename, expectedfile):
    ecfg = ECFG().from_cfg(load_cfg(filename))
    rsm = RSM().from_ecfg(ecfg)

    assert len(rsm.productions) == len(ecfg.production)
    for head, body in ecfg.production.items():
        head2 = rsm.productions[head]
        assert body.to_epsilon_nfa().is_equivalent_to(head2)
    assert ecfg.start_symbols == rsm.start_symbols


@pytest.mark.parametrize(
    "filename, expectedfile",
    [
        ("tests/ecfg/ecfg", "tests/ecfg/ecfg-result"),
        ("tests/ecfg/ecfg-2", "tests/ecfg/ecfg-result-2"),
    ],
)
def test_minimize(filename, expectedfile):
    actual_ecfg = ECFG().from_cfg(load_cfg(filename))
    expected_ecfg = ECFG().from_cfg(load_cfg(expectedfile))
    actual = RSM().from_ecfg(actual_ecfg).minimize()
    expected = RSM().from_ecfg(expected_ecfg)

    assert len(expected.productions) == len(actual.productions)
    for head, body in expected.productions.items():
        head2 = actual.productions[head]
        assert body.is_equivalent_to(head2)
