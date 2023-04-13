from project.task03.ap_rpq import get_boolean_matrixes
from project.task07.ecfg import ECFG


class RSM:
    """
    Recursive state machine class
    """

    def __init__(self):
        self.start_symbols = None
        self.productions = dict()
        self.matrixes = dict()

    def from_ecfg(self, ecfg: ECFG):
        self.start_symbols = ecfg.start_symbols
        self.productions = dict()
        for head, body in ecfg.production.items():
            self.productions[head] = body.to_epsilon_nfa()
            self.matrixes[head] = get_boolean_matrixes(self.productions[head])
        return self

    def minimize(self):
        for head, body in self.productions.items():
            self.productions[head] = body.minimize()
        return self
