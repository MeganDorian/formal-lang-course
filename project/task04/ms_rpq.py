import networkx as net
from pyformlang.finite_automaton import State, EpsilonNFA
from scipy import sparse
from scipy.sparse import dok_matrix, vstack

from project.task02.finite_automaton import create_nfa, from_regex_to_dfa
from project.task03.ap_rpq import get_boolean_matrixes


def transform_front(front: dok_matrix, second_states_size: int) -> dok_matrix:
    """
    Shifts current front to the triangular form with ones at the main diagonal
    :param front: current front
    :param second_states_size: count of states in the second graph
    :return: transformed dok_matrix front
    """
    transformed = dok_matrix(front.shape, dtype=bool)
    for Ix, Iy in zip(*front.nonzero()):
        if Iy < second_states_size:
            row_right = front[[Ix], second_states_size:]
            if row_right.nnz > 0:
                front_shifted = Ix - (Ix % second_states_size)
                transformed[front_shifted + Iy, Iy] = True
                transformed[[front_shifted + Iy], second_states_size:] += row_right
    return transformed


def direct_sum(first: dict, second: dict) -> dict:
    """
    Makes the dict of direct sums of two matrices:
    second   None
    None    first
    for common symbols
    :param first: dict of boolean matrix of first graph
    :param second: dict of boolean matrix of second graph
    :return: dictionary of boolean dok_matrix which represents direct sums of two boolean matrices
    """
    direct_sums = dict()
    for symbol in first:
        if symbol in second:
            direct_sums[symbol] = sparse.bmat(
                [[second[symbol], None], [None, first[symbol]]]
            )
    return direct_sums


def create_front_for_each(first_states: list, second_states: list) -> dok_matrix:
    """
    Creates front for each start state from first graph (separated)
    :param first_states: info about first graph states: 1 - all states, 2 - all start states
    :param second_states: info about second graph states: 1 - all states, 2 - all start states
    :return: dok_matrix, current front
    """
    result = None
    for state_to_create in first_states[1]:
        front = dok_matrix(
            (len(second_states[0]), len(first_states[0]) + len(second_states[0])),
            dtype=bool,
        )
        front_right = dok_matrix((1, len(first_states[0])), dtype=bool)
        front_right[0, first_states[1][state_to_create]] = True
        for state in second_states[1]:
            index = second_states[0][state]
            front[index, index] = True
            front[[index], len(second_states[0]) :] = front_right
        if result is None:
            result = front
        else:
            result = vstack([result, front])
    return result


def create_front_for_all(first_states: list, second_states: list) -> dok_matrix:
    """
    Creates front for all states (not separated)
    :param first_states: info about first graph states: 1 - all states, 2 - all start states
    :param second_states: info about second graph states: 1 - all states, 2 - all start states
    :return: dok_matrix, current front
    """
    front = dok_matrix(
        (len(second_states[0]), len(first_states[0]) + len(second_states[0])),
        dtype=bool,
    )
    front_right = dok_matrix((1, len(first_states[0])), dtype=bool)
    for state_number in first_states[1]:
        front_right[0, first_states[1][state_number]] = True
    for state in second_states[1]:
        index = second_states[0][state]
        front[index, index] = True
        front[[index], len(second_states[0]) :] = front_right
    return front


def get_set_of_reachable(
    visited_result: dok_matrix,
    first_states_info: list,
    second_states_info: list,
    find_for_each: bool,
) -> set:
    """
    Builds in one answer set of reachable states from visited states
    :param visited_result: matrix of last front from bfs
    :param first_states_info: info about first graph states: 1 - all states, 2 - all start states, 3 - all final states
    :param second_states_info: info about second graph states: 1 - all states, 2 - all start states, 3 - all final states
    :param find_for_each: flag which shows do we need to make front for each state or not
    :return: set: if find_for_each - pairs (start_state, reachable_state), else - just set of reachable states
    """
    result = set()
    second_states_count = len(second_states_info[0])
    first_all_states_keys = list(first_states_info[0].keys())
    first_all_states_values = list(first_states_info[0].values())
    second_all_states_keys = list(second_states_info[0].keys())
    second_all_states_values = list(second_states_info[0].values())

    for x, y in zip(*visited_result.nonzero()):
        if y >= second_states_count:
            index_first = y - second_states_count
            index_second = x % second_states_count
            value_in_first = first_all_states_keys[first_all_states_values[index_first]]
            value_in_second = second_all_states_keys[
                second_all_states_values[index_second]
            ]
            if (
                value_in_first in first_states_info[2].keys()
                and value_in_second in second_states_info[2].keys()
            ):
                if find_for_each:
                    value = State(x // second_states_count), State(index_first)
                else:
                    value = State(index_first)
                result.add(value)

    return result


def bfs(
    first_boolean: dict,
    second_boolean: dict,
    first_states_info: list,
    second_states_info: list,
    find_for_each: bool,
) -> dok_matrix:
    """
    Inner bfs from outer global function in which calculates direct sums, first front and in cycle doing bfs
    while front is changing
    :param first_boolean:
    :param second_boolean:
    :param first_states_info:
    :param second_states_info:
    :param find_for_each:
    :return: final front, all marked visited states
    """
    direct_sums = direct_sum(first_boolean, second_boolean)

    if find_for_each:
        front = create_front_for_each(first_states_info, second_states_info)
    else:
        front = create_front_for_all(first_states_info, second_states_info)

    visited = dok_matrix(front.shape, dtype=bool)
    next_visited = visited.nnz
    changes = True
    while changes:
        for k, v in direct_sums.items():
            if front is None:
                next_front = visited.dot(v)
            else:
                next_front = front.dot(v)
            visited += transform_front(next_front, len(second_states_info[0]))
        changes = visited.nnz != next_visited
        next_visited = visited.nnz
        front = None
    return visited


def bfs_rpq(
    first: EpsilonNFA,
    second: EpsilonNFA,
    find_for_each: bool,
) -> set:
    """
    Finds all reachable states from list of start states for two graphs (graph and regular expression)
    :param first: first graph
    :param second: second graph (regular expression)
    :param find_for_each: flag which shows do we need to make front for each state or not
    :return: set of reachable states
    """
    first_boolean = get_boolean_matrixes(first)
    second_boolean = get_boolean_matrixes(second)

    first_states = {state: idx for idx, state in enumerate(first.states)}
    first_start_states = {State(state): state.value for state in first.start_states}
    first_final_states = {State(state): state.value for state in first.final_states}

    second_states = {state: idx for idx, state in enumerate(second.states)}
    second_start_states = {State(state): state.value for state in second.start_states}
    second_final_states = {State(state): state.value for state in second.final_states}

    last_visited = bfs(
        first_boolean,
        second_boolean,
        [first_states, first_start_states],
        [second_states, second_start_states],
        find_for_each,
    )

    return get_set_of_reachable(
        last_visited,
        [first_states, first_start_states, first_final_states],
        [second_states, second_start_states, second_final_states],
        find_for_each,
    )


def ms_rpq(
    graph: net.Graph,
    start_states: list,
    final_states: list,
    regex: str,
    find_for_each: bool,
):
    fa = create_nfa(graph, start_states, final_states)
    regex_fa = from_regex_to_dfa(regex)

    return bfs_rpq(fa, regex_fa, find_for_each)
