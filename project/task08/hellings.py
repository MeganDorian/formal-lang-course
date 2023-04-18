from pyformlang.cfg import CFG, Variable, Terminal

from project.task01.graph import load_graph_from_file
from project.task06.wcnf import make_weak_ncf, load_cfg


class Helling:
    """
    Perform hellings algorithm
    1. Makes from cfg wcfg
    2. Creates list of epsilons, terminals and productions for further algorithm work
    3. Calculates r = {(Ni, v, v) | v ∈ V ∧ Ni → ε ∈ P} ∪ {(Ni, v, u) | (v, t, u) ∈ E ∧ Ni → t ∈ P}
    4. Stars querying context free path
    :param graph: any type of graph from networkx.Graph
    :param cfg: context free grammar representation
    """

    def __init__(self, graph, cfg: CFG):
        if isinstance(graph, str):
            self.graph = load_graph_from_file(graph)
        else:
            self.graph = graph
        if isinstance(cfg, str):
            try:
                self.cfg = load_cfg(cfg)
            except OSError:
                self.cfg = CFG.from_text(cfg)
        else:
            self.cfg = cfg
        wcfg = make_weak_ncf(self.cfg)
        epsilons = [pr.head for pr in wcfg.productions if not pr.body]
        self.variables = list()
        terminals = list()
        for pr in wcfg.productions:
            if pr.body and isinstance(pr.body[0], Variable):
                self.variables.append(pr)
            if pr.body and isinstance(pr.body[0], Terminal):
                terminals.append(pr)

        self.r = {(n, int(v), int(v)) for v in self.graph.nodes for n in epsilons} | {
            (n.head, int(v), int(u))
            for v, u, t in self.graph.edges.data("label")
            for n in terminals
            if n.body[0].value == t
        }
        self.m = self.r.copy()

    def hellings_algorithm(self):
        while len(self.m) != 0:
            ni, v, u = self.m.pop()
            res = set()
            for nj, v1, v2 in self.r:
                if v == v2:
                    for nk in self.variables:
                        if (
                            nj.value == nk.body[0].value
                            and ni.value == nk.body[1].value
                            and (nk.head, v1, u) not in self.r
                        ):
                            self.m.add((nk.head, v1, u))
                            res.add((nk.head, v1, u))
                if v1 == u:
                    for nk in self.variables:
                        if (
                            ni.value == nk.body[0].value
                            and nj.value == nk.body[1].value
                            and (nk.head, v, v2) not in self.r
                        ):
                            self.m.add((nk.head, v, v2))
                            res.add((nk.head, v, v2))
            self.r |= res
        return self.r
