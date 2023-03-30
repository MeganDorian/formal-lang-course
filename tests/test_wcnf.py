import pytest

from project.task06.wcnf import load_cfg, make_weak_ncf, write_cfg


@pytest.mark.parametrize(
    "filename, expectedfile",
    [
        ("cfg/cfg", "cfg/cfg-result"),
        ("cfg/cfg-2", "cfg/cfg-result-2"),
        ("cfg/cfg-3", "cfg/cfg-result-3"),
    ],
)
def test_weak_normal_chomsky_form(filename, expectedfile):
    cfg = load_cfg(filename)
    weak = make_weak_ncf(cfg)
    expected = load_cfg(expectedfile)
    assert set(weak.productions) == expected.productions
