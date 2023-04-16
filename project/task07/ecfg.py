from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex

from project.task06.wcnf import load_cfg


class ECFG:
    def __init__(self):
        self.variables = None
        self.start_symbols = None
        self.terminals = None
        self.production = None

    def from_cfg(self, cfg: CFG):
        """
        From CFG builds extended CFG
        :param cfg: CFG to process
        """
        self.production = dict()

        for production in cfg.productions:
            head = production.head
            body = ""
            if len(production.body) == 0:
                body = "$"
            else:
                body = body.join(" " + pr_body.value for pr_body in production.body)
            body = Regex(body)
            self.production[head] = (
                (self.production.get(head).union(body))
                if head in self.production
                else body
            )

        self.start_symbols = (
            Variable("S") if cfg.start_symbol is None else cfg.start_symbol
        )
        self.variables = set(cfg.variables)
        self.variables.add(self.start_symbols)
        self.terminals = cfg.terminals
        return self

    def from_file(self, filename: str):
        """
        From filename builds cfg and then builds extended CFG
        :param filename: name of file to read cfg from
        """
        cfg = load_cfg(filename)
        return self.from_cfg(cfg)

    def from_string(self, string: str):
        return self.from_cfg(CFG.from_text(string))
