from pyformlang.cfg import CFG


def load_cfg(filename: str) -> CFG:
    """
    Opens the file with saved cfg
    :param filename: name of file
    :return: CFG object
    """
    with open(filename, "r") as f:
        f_str = f.read()

    return CFG.from_text(f_str)


def write_cfg(filename: str, cfg: CFG):
    """
    Writes the cfg to the given file
    :param filename: name of file
    :param cfg: to write
    """
    with open(filename, "w") as f:
        f.write(cfg.to_text())


def make_weak_ncf(cfg: CFG) -> CFG:
    """
    From CFG creates Weak Chomsky Normal Form:

    1. eliminates long productions
    2. removes useless symbols
    3. eliminates chained productions
    4. creates cfg with remaining productions

    :param cfg: to create from
    :return: cfg in weak normal form
    """
    cfg = cfg.eliminate_unit_productions().remove_useless_symbols()
    productions = cfg._decompose_productions(
        cfg._get_productions_with_only_single_terminals()
    )
    return CFG(start_symbol=cfg.start_symbol, productions=set(productions))
