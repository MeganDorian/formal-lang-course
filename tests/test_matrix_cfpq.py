import pytest

from project.task01.graph import create_labeled_two_cycles_graph
from project.task06.wcnf import load_cfg
from project.task08_09.cfpq import matrix


@pytest.mark.parametrize(
    "graph, cfg, start, final, variable, result",
    [
        (
            "tests/hellings/graph",
            """
            A -> a | epsilon
            B -> b C
            S -> C | A S1
            S1 -> S B
            C -> a
            """,
            None,
            None,
            "S",
            {(0, 1), (1, 2), (2, 0)},
        ),
        (
            create_labeled_two_cycles_graph(3, 2, ["a", "b"]),
            load_cfg("tests/hellings/cfg"),
            {0},
            {1, 2},
            "A",
            {(0, 1)},
        ),
        (
            create_labeled_two_cycles_graph(3, 2, ["a", "b"]),
            "tests/hellings/cfg",
            {0},
            {1, 2},
            "A",
            {(0, 1)},
        ),
    ],
)
def test_matrix(graph, cfg, start, final, variable, result):
    assert matrix(graph, cfg, start, final, variable) == result
