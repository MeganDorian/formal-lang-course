import networkx as net
from pyformlang.finite_automaton import EpsilonNFA
from scipy.sparse import dok_matrix, kron

from project.task02.finite_automaton import create_nfa, from_regex_to_dfa


def get_transitive_closure(matrix: dok_matrix):
    """
    Builds matrix transitive closure for the matrix
    :param matrix: matrix to close
    :return: transitively closed matrix
    """

    start_vertex = 0
    next_vertex = matrix.getnnz()
    while start_vertex != next_vertex:
        matrix += matrix.dot(matrix)
        start_vertex = next_vertex
        next_vertex = matrix.getnnz()

    return matrix


def get_boolean_matrixes(graph: EpsilonNFA) -> dict:
    """
    Creates dictionary of boolean matrixes from the graph.
    For each state in graph creates dok_matrix with the size (graph.states x graph.states) .
    For example for transition [0, 'a', 1] in the matrix_a on the row 0 and column 1 will be True
    :param graph: finite automaton
    :return: dictionary of boolean matrixes
    """

    count_of_states = len(graph.states)
    states = {state: idx for idx, state in enumerate(graph.states)}
    result = dict()
    for source, label, dest in graph:
        if label not in result:
            result[label] = dok_matrix((count_of_states, count_of_states), dtype=bool)
        result[label][states[source], states[dest]] = True
    return result


def kron_multiplication(first, second) -> dok_matrix:
    """
    Kron multiplication for two dok matrixes
    :param first: first matrix
    :param second: second matrix
    :return: dok matrix which represents kron multiplication
    """

    return kron(first, second, format="dok")


def get_intersect_of_two_finite_automaton(
    first: EpsilonNFA, second: EpsilonNFA
) -> dok_matrix:
    """
    Gets an transitive intersection of two FA.
    Firstly get boolean matrixes of first and second graph.
    Secondly get kron multiplication for common symbols
    Then sums all multiplied matrixes
    Then transitive closes summed matrix
    :param first: first finite automaton
    :param second: second finite automaton
    :return: transitively closed boolean dok_matrix of intersection of two graphs
    """
    first_boolean = get_boolean_matrixes(first)
    second_boolean = get_boolean_matrixes(second)

    b_t = dict()
    for first_b_symb, first_b_matrix in first_boolean.items():
        if first_b_symb in second_boolean:
            b_t[first_b_symb] = kron_multiplication(
                first_b_matrix, second_boolean[first_b_symb]
            )

    matrix_size = len(first.states) * len(second.states)
    sum_boolean = dok_matrix((matrix_size, matrix_size), dtype=bool)
    for key, item in b_t.items():
        sum_boolean += item

    transitive = get_transitive_closure(sum_boolean)
    return transitive


def all_pairs_rpq(graph: net.Graph, start_states: list, final_states: list, regex: str):
    fa = create_nfa(graph, start_states, final_states)
    regex_fa = from_regex_to_dfa(regex)

    intersection = get_intersect_of_two_finite_automaton(fa, regex_fa)
    decart = [(a, b) for a in fa.states for b in regex_fa.states]
    result = set()
    for x, y in zip(*intersection.nonzero()):
        a, b = decart[x]
        c, d = decart[y]
        if (
            a in fa.start_states
            and b in regex_fa.start_states
            and c in fa.final_states
            and d in regex_fa.final_states
        ):
            result.add((a, c))
    return result
