from pyformlang.cfg import Variable, CFG, Terminal
from scipy.sparse import dok_matrix

from project.task01.graph import load_graph_from_file
from project.task06.wcnf import make_weak_ncf, load_cfg


class Matrix:
    def __init__(self, graph, cfg):
        if isinstance(graph, str):
            self.graph = load_graph_from_file(graph)
        else:
            self.graph = graph
        if isinstance(cfg, str):
            try:
                cfg = load_cfg(cfg)
            except OSError:
                cfg = CFG.from_text(cfg)
        else:
            cfg = cfg
        self.cfg = make_weak_ncf(cfg)
        self.n = len(self.graph.nodes)
        self.e = self.graph.edges(data=True)
        self.epsilons = [pr.head for pr in self.cfg.productions if not pr.body]
        self.variables = list()
        self.terminals = list()
        for pr in self.cfg.productions:
            if pr.body and isinstance(pr.body[0], Variable):
                self.variables.append(pr)
            if pr.body and isinstance(pr.body[0], Terminal):
                self.terminals.append(pr)

    def matrix_algorithm(self):
        T = {
            var: dok_matrix((self.n, self.n), dtype=bool) for var in self.cfg.variables
        }
        for i, j, x in self.e:
            for pr in self.terminals:
                if pr.body[0] == Terminal(x["label"]):
                    T[pr.head][int(i), int(j)] = True

        for i in range(self.n):
            for eps in self.epsilons:
                T[eps][i, i] = True

        T = self.transitive_closure(T)
        result = {(var, u, v) for var, m in T.items() for u, v in zip(*m.nonzero())}
        return result

    def transitive_closure(self, T):
        isChanging = True
        isChanged = False
        while isChanging:
            for p in self.variables:
                start = T[p.head].getnnz()
                T[p.head] += T[p.body[0]].dot(T[p.body[1]])
                next = T[p.head].getnnz()
                isChanged = next != start
            isChanging = False or isChanged
        return T
