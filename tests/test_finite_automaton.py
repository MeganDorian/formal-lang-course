import pytest
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, Symbol, State

from project.task01.graph import (
    load_graph,
    create_labeled_two_cycles_graph,
    get_graph_info,
)
from project.task02.finite_automaton import from_regex_to_dfa, create_nfa


@pytest.mark.parametrize(
    "regex, accepts",
    [
        ("a* b*", ["a", "aa", "bb"]),
        ("a | b", ["a", "b"]),
        ("d* | (x | y)*", ["dd", "xx", "y"]),
    ],
)
def test_from_regex_to_dfa_accepts(regex, accepts):
    dfa = from_regex_to_dfa(regex)
    assert dfa.is_deterministic()

    for word in accepts:
        assert dfa.accepts(word)


def test_from_regex_to_dfa_equal():
    actual = from_regex_to_dfa("aa(a|b)*")

    expected = DeterministicFiniteAutomaton()

    symbol_aa = Symbol("aa")
    symbol_a = Symbol("a")
    symbol_b = Symbol("b")

    state_0 = State(0)
    state_1 = State(1)

    expected.add_start_state(state_0)
    expected.add_final_state(state_1)

    expected.add_transitions(
        [
            (state_0, symbol_aa, state_1),
            (state_1, symbol_a, state_1),
            (state_1, symbol_b, state_1),
        ]
    )

    assert expected.is_equivalent_to(actual)


@pytest.mark.parametrize("graph_name", ["pr", "skos", "wc"])
def test_create_nfa_from_downloaded(graph_name):
    downloaded_graph = load_graph(graph_name)
    nfa = create_nfa(downloaded_graph)
    assert nfa.start_states == set(downloaded_graph.nodes)
    assert nfa.final_states == set(downloaded_graph.nodes)
    assert nfa.symbols == get_graph_info(downloaded_graph).labels


@pytest.mark.parametrize(
    "first_cycle_count, second_cycle_count, labels, start, final",
    [
        (1, 3, ["c", "d"], {0, 1}, {4}),
        (3, 2, ["ac", "d"], {1}, {2, 3, 4}),
        (2, 5, ["d", "b"], None, None),
    ],
)
def test_create_nfa_from_generated_two_cycled(
    first_cycle_count, second_cycle_count, labels, start, final
):
    generated = create_labeled_two_cycles_graph(
        first_cycle_count, second_cycle_count, labels
    )
    nfa = create_nfa(generated, start, final)
    assert nfa.start_states == start if start is not None else generated.nodes
    assert nfa.final_states == final if final is not None else generated.nodes
    assert nfa.symbols == set(labels)
