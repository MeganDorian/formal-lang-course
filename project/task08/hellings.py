from pyformlang.cfg import CFG, Variable, Terminal

from project.task01.graph import load_graph_from_file
from project.task06.wcnf import make_weak_ncf, load_cfg


def context_free_path_querying(r, variables):
    m = r.copy()
    while len(m) != 0:
        ni, v, u = m.pop()
        res = set()
        for nj, v1, v2 in r:
            if v == v2:
                for nk in variables:
                    if (
                        nj.value == nk.body[0].value
                        and ni.value == nk.body[1].value
                        and (nk.head, v1, u) not in r
                    ):
                        m.add((nk.head, v1, u))
                        res.add((nk.head, v1, u))
            if v1 == u:
                for nk in variables:
                    if (
                        ni.value == nk.body[0].value
                        and nj.value == nk.body[1].value
                        and (nk.head, v, v2) not in r
                    ):
                        m.add((nk.head, v, v2))
                        res.add((nk.head, v, v2))
        r |= res
    return r


def hellings_algorithm(graph, cfg: CFG):
    """
    Perform hellings algorithm
    Accepts graph as: MultiGraph, path to file with saved graph
    Accepts cfg as: CFG, path to file with saved cfg, text
    1. Makes from cfg wcfg
    2. Creates list of epsilons, terminals and productions for further algorithm work
    3. Calculates r = {(Ni, v, v) | v ∈ V ∧ Ni → ε ∈ P} ∪ {(Ni, v, u) | (v, t, u) ∈ E ∧ Ni → t ∈ P}
    4. Stars querying context free path
    :param graph: any type of graph from networkx.Graph
    :param cfg: context free grammar representation
    """
    if isinstance(graph, str):
        graph = load_graph_from_file(graph)
    if isinstance(cfg, str):
        try:
            cfg = load_cfg(cfg)
        except OSError:
            cfg = CFG.from_text(cfg)
    wcfg = make_weak_ncf(cfg)
    epsilons = [pr.head for pr in wcfg.productions if not pr.body]
    variables = list()
    terminals = list()
    for pr in wcfg.productions:
        if pr.body and isinstance(pr.body[0], Variable):
            variables.append(pr)
        if pr.body and isinstance(pr.body[0], Terminal):
            terminals.append(pr)

    r = {(n, v, v) for v in graph.nodes for n in epsilons} | {
        (n.head, v, u)
        for v, u, t in graph.edges.data("label")
        for n in terminals
        if n.body[0].value == t
    }

    return context_free_path_querying(r, variables)


def get_reachable_by_hellings(
    graph, cfg, start_states: list, final_states: list, variable: str
):
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
    variable = Variable(variable)
    result = hellings_algorithm(graph, cfg)

    if start_states is None:
        start_states = graph.nodes

    if final_states is None:
        final_states = graph.nodes

    r = set()
    for var, v, u in result:
        if v in start_states and u in final_states and var == variable:
            r.add((int(v), int(u)))
    return r
