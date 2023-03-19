import cfpq_data
import pytest
from networkx import MultiDiGraph

from project.task01.graph import create_labeled_two_cycles_graph
from project.task04.ms_rpq import ms_rpq


@pytest.mark.parametrize(
    "first_cycle_count, second_cycle_count, start_states, final_states, labels, regex, expected",
    [
        (2, 4, [1, 3], [4], ["a", "b"], "a|b*", {(1, 4)}),
        (
            2,
            2,
            None,
            None,
            ["a", "b"],
            "a.b*",
            {(0, 1), (1, 2), (2, 0), (2, 3), (2, 4)},
        ),
        (3, 5, [0, 1], [2, 4], ["a", "b"], "a*|b*", {(0, 2), (0, 4), (1, 2)}),
        (2, 5, [4], [2], ["a", "b"], "(ab)*", set()),
    ],
)
def test_ms_pairs_rpq_for_each(
    first_cycle_count,
    second_cycle_count,
    start_states,
    final_states,
    labels,
    regex,
    expected,
):
    graph = create_labeled_two_cycles_graph(
        first_cycle_count, second_cycle_count, labels
    )
    actual = ms_rpq(graph, start_states, final_states, regex, True)
    assert expected == actual


@pytest.mark.parametrize(
    "first_cycle_count, second_cycle_count, start_states, final_states, labels, regex, expected",
    [
        (3, 3, [0, 2], [0, 5], ["a", "b"], "a*|b.", {0}),
        (4, 6, [0, 3, 5], [1, 2, 4, 7], ["a", "b"], "a.b*", {1, 4}),
        (2, 2, None, None, ["a", "b"], "a*b*", {0, 1, 2, 3, 4}),
        (2, 5, [0], [4], ["a", "b"], "(abc)*", set()),
    ],
)
def test_ms_pairs_rpq_for_all(
    first_cycle_count,
    second_cycle_count,
    start_states,
    final_states,
    labels,
    regex,
    expected,
):
    graph = create_labeled_two_cycles_graph(
        first_cycle_count, second_cycle_count, labels
    )
    actual = ms_rpq(graph, start_states, final_states, regex, False)
    assert expected == actual
