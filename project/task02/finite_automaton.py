import networkx as net
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, EpsilonNFA, State
from pyformlang.regular_expression import Regex

from project.task01.graph import get_graph_info


def from_regex_to_dfa(regex_str: str) -> DeterministicFiniteAutomaton:
    """
    Builds DFA from regex
    :param regex_str: regex with format https://pyformlang.readthedocs.io/en/latest/usage.html#regular-expression`
    :return: DeterministicFiniteAutomaton
    """
    regex = Regex(regex_str)
    dfa = regex.to_epsilon_nfa().minimize()
    return dfa


def create_nfa(graph: net.Graph, start_states=None, final_states=None) -> EpsilonNFA:
    """
    Builds NFA from another graph
    :param graph: any type of graph from networkx.Graph
    :param start_states: set of start_states. If None, all states marks as start ones
    :param final_states: set of final_states. If None, all states marks as final ones
    :return: EpsilonNFA
    """
    nfa = EpsilonNFA()
    nfa = nfa.from_networkx(graph)

    graph_info = get_graph_info(graph)
    states = [State(n) for n in range(graph_info.nodes)]

    if start_states is None:
        start_states = states

    if final_states is None:
        final_states = states

    for s_state in start_states:
        nfa.add_start_state(s_state)

    for f_state in final_states:
        nfa.add_final_state(f_state)

    return nfa
