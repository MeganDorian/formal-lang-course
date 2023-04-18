from pyformlang.cfg import Variable

from project.task08.hellings import Helling
from project.task09.matrix import Matrix


def prepare_init_data(start_states: list, final_states: list, variable: str, algorithm):
    variable = Variable(variable)
    if start_states is None:
        start_states = algorithm.graph.nodes
    start_states = [int(x) for x in start_states]

    if final_states is None:
        final_states = algorithm.graph.nodes
    final_states = [int(x) for x in final_states]

    return start_states, final_states, variable


def hellings(graph, cfg, start_states: list, final_states: list, variable: str):
    """
    Performs hellings algorithm for the graph with cfg
    Accepts graph as: MultiGraph, path to file with saved graph
    Accepts cfg as: CFG, path to file with saved cfg, text
    :param graph: any type of graph from networkx.Graph
    :param cfg: context free grammar representation
    :param start_states: set of start_states. If None, all states marks as start ones
    :param final_states: set of final_states. If None, all states marks as final ones
    :param variable: start variable
    """
    helling = Helling(graph, cfg)
    start_states, final_states, variable = prepare_init_data(
        start_states, final_states, variable, helling
    )
    result = helling.hellings_algorithm()

    r = set()
    for var, v, u in result:
        if v in start_states and u in final_states and var == variable:
            r.add((v, u))
    return r


def matrix(graph, cfg, start_states: list, final_states: list, variable: str):
    matrixes = Matrix(graph, cfg)
    start_states, final_states, variable = prepare_init_data(
        start_states, final_states, variable, matrixes
    )
    result = matrixes.matrix_algorithm()
    r = set()
    for var, v, u in result:
        if v in start_states and u in final_states and var == variable:
            r.add((v, u))
    return r
