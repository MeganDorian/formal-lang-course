import pytest

from project.task01.graph import create_labeled_two_cycles_graph
from project.task03.regular_queries import all_pairs_rpq


@pytest.mark.parametrize(
    "first_cycle_count, second_cycle_count, start_states, final_states, labels, regex, expected",
    [
        (5, 2, [0], [6, 4], ["a", "b"], "a*|b", {(0, 6), (0, 4)}),
        (3, 4, [1], [2, 4], ["a", "b"], "a", {(1, 2)}),
        (0, 0, None, None, [], "a*", set()),
        (
            3,
            2,
            None,
            None,
            ["a", "b"],
            "a*|b*",
            {
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (0, 4),
                (0, 5),
                (1, 0),
                (1, 1),
                (1, 2),
                (1, 3),
                (2, 0),
                (2, 1),
                (2, 2),
                (2, 3),
                (3, 0),
                (3, 1),
                (3, 2),
                (3, 3),
                (4, 0),
                (4, 4),
                (4, 5),
                (5, 0),
                (5, 4),
                (5, 5),
            },
        ),
        (0, 0, None, None, [], "", set()),
        (2, 1, [1, 2], None, ["a", "b"], "x*", set()),
    ],
)
def test_ap_rpq(
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
    result = all_pairs_rpq(graph, start_states, final_states, regex)
    assert expected == result
