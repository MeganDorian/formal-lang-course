from project.task07.ecfg import ECFG


class RSM:
    def __init__(self):
        self.start_symbols = None
        self.productions = dict()

    def from_ecfg(self, ecfg: ECFG):
        self.start_symbols = ecfg.start_symbols
        self.productions = dict()
        for head, body in ecfg.production.items():
            self.productions[head] = body.to_epsilon_nfa()
        return self

    def minimize(self):
        for head, body in self.productions.items():
            self.productions[head] = body.minimize()
        return self
