from project.task01.graph import *


def test_graph_info():
    graph_name = "ls"
    graph = load_graph_and_get_info(graph_name)
    assert 1687 == graph.nodes
    assert 1453 == graph.edges
    assert {"d", "a"} == graph.labels


def test_create_and_save_to_dot_labeled_two_cycles_graph():
    filename = "test_create_labeled_two_cycles_graph.dot"
    expected = (
        "digraph  { 1; 2; 0; 3; 4; 5; 6; 1 -> 2  [key=0, label=a]; 2 -> 0  [key=0, label=a]; 0 -> 1  [key=0, "
        "label=a]; 0 -> 3  [key=0, label=c]; 3 -> 4  [key=0, label=c]; 4 -> 5  [key=0, label=c]; 5 -> 6  ["
        "key=0, label=c]; 6 -> 0  [key=0, label=c]; } "
    )
    create_and_save_to_dot_labeled_two_cycles_graph(2, 4, ["a", "c"], filename)
    with open(filename, "r") as f:
        assert expected == f.read().replace("\n", " ")
