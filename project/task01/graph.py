from collections import namedtuple

import networkx.drawing.nx_pydot
from cfpq_data import *
from networkx import MultiDiGraph
from networkx.drawing import nx_pydot

Graph = namedtuple("Graph", "nodes edges labels")


def load_graph(name: str) -> MultiDiGraph:
    """
    Downloads graph from cfpq_data by name
    :param name: name of graph to download
    :return: MultiGraph
    """
    path = cfpq_data.download(name)
    return cfpq_data.graph_from_csv(path)


def get_graph_info(graph):
    """
    Returns representation of graph info: count of nodes, count of edges, list of labels
    :param graph:
    :return: NamedTuple Graph
    """
    V = graph.number_of_nodes()  # count of node
    E = graph.number_of_edges()  # count of edges
    L = set(cfpq_data.get_sorted_labels(graph))  # label
    return Graph(V, E, L)


def load_graph_and_get_info(name: str):
    """
    Downloads graph by name and return information about it
    :param name: name of graph to download
    :return: NamedTuple Graph
    """
    graph = load_graph(name)
    return get_graph_info(graph)


def load_graph_from_file(filename: str) -> MultiDiGraph:
    return nx_pydot.read_dot(filename)


def save_to_dot_graph(graph, filename="dot_graph"):
    """
    Saves graph to the file with name filename
    :param graph: graph to save
    :param filename: name of file to save the graph
    """
    if not filename.endswith(".dot"):
        filename = filename + ".dot"
    pydot_graph = networkx.drawing.nx_pydot.to_pydot(graph)
    with open(filename, "w"):
        pydot_graph.write(filename)


def create_labeled_two_cycles_graph(
    first_circle_vertex_count, second_circle_vertex_count, labels
) -> MultiDiGraph:
    """
    Generates labeled two cycles graph using cfpq_data.labeled_two_cycles_graph() method
    :param first_circle_vertex_count: number of nodes in the first cycle
    :param second_circle_vertex_count: number of nodes in the second cycle
    :param labels: list of labels
    :return: MultiDiGraph
    """
    if first_circle_vertex_count == 0 and second_circle_vertex_count == 0:
        return networkx.empty_graph()
    else:
        return cfpq_data.labeled_two_cycles_graph(
            first_circle_vertex_count, second_circle_vertex_count, labels=labels
        )


def create_and_save_to_dot_labeled_two_cycles_graph(
    first_circle_vertex_count, second_circle_vertex_count, labels, filename: str
) -> MultiDiGraph:
    """
    Generates labeled two cycles graph and saves it to the file
    :param first_circle_vertex_count: number of nodes in the first cycle
    :param second_circle_vertex_count: number of nodes in the second cycle
    :param labels: list of labels
    :param filename: name of file to save the graph
    :return:
    """
    graph = create_labeled_two_cycles_graph(
        first_circle_vertex_count, second_circle_vertex_count, labels=labels
    )
    save_to_dot_graph(graph, filename)
    return graph
