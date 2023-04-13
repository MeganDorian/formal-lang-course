import pytest
from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

from project.task06.wcnf import load_cfg, make_weak_ncf
from project.task07.ecfg import ECFG


@pytest.mark.parametrize(
    "filename, productions",
    [
        (
            "tests/ecfg/ecfg",
            {
                Variable("S"): Regex("B | a*b | epsilon"),
                Variable("C"): Regex("S S"),
                Variable("B"): Regex("C"),
            },
        ),
        (
            "tests/ecfg/ecfg-2",
            {
                Variable("S"): Regex("S A"),
                Variable("A"): Regex("a | B"),
                Variable("B"): Regex("C | epsilon"),
                Variable("C"): Regex("c"),
            },
        ),
    ],
)
def test_from_cfg_to_ecfg_from_file(filename, productions):
    ecfg = ECFG().from_file(filename)
    assert len(productions) == len(ecfg.production)
    for head, body in ecfg.production.items():
        expected = productions[head]
        b = body.to_epsilon_nfa()
        d = expected.to_epsilon_nfa()
        assert b.is_equivalent_to(d)


@pytest.mark.parametrize(
    "filename",
    [
        "tests/cfg/cfg",
        "tests/cfg/cfg-2",
        "tests/cfg/cfg-3",
    ],
)
def test_from_cfg_to_ecfg_from_wcnf(filename):
    cfg = load_cfg(filename)
    weak = make_weak_ncf(cfg)
    ecfg = ECFG().from_cfg(weak)
    assert weak.start_symbol == ecfg.start_symbols
    assert weak.terminals == ecfg.terminals
    assert weak.variables == ecfg.variables


@pytest.mark.parametrize(
    "filename, productions",
    [
        (
            "tests/ecfg/ecfg",
            {
                Variable("S"): Regex("B | a*b | epsilon"),
                Variable("C"): Regex("S S"),
                Variable("B"): Regex("C"),
            },
        ),
        (
            "tests/ecfg/ecfg-2",
            {
                Variable("S"): Regex("S A"),
                Variable("A"): Regex("a | B"),
                Variable("B"): Regex("C | epsilon"),
                Variable("C"): Regex("c"),
            },
        ),
    ],
)
def test_from_cfg_to_ecfg_from_text(filename, productions):
    with open(filename, "r") as f:
        f_str = f.read()
    ecfg = ECFG().from_string(f_str)
    assert len(productions) == len(ecfg.production)
    for head, body in ecfg.production.items():
        expected = productions[head]
        b = body.to_epsilon_nfa()
        d = expected.to_epsilon_nfa()
        assert b.is_equivalent_to(d)
