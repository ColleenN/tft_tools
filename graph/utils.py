import networkx as nx
from matplotlib import pyplot as plt
from typing import Iterable


def draw_trait_web(trait_graph, layout):
    edge_labels = {(x[0], x[1],): x[2] for x in trait_graph.edges.data('label')}

    plt.figure(1, figsize=(20, 10))
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    nx.draw_networkx(
        trait_graph,
        pos=layout,
        with_labels=True,
        node_color=nx.get_node_attributes(trait_graph, 'color').values(),
        edge_color=nx.get_edge_attributes(trait_graph, 'color', default='#BBBBBB').values(),
        width=3.0
    )
    nx.draw_networkx_edge_labels(trait_graph, layout, edge_labels=edge_labels)
    plt.show()


def shortest_path_subgraph(graph, target_nodes: Iterable[str]):

    node_set = set(target_nodes)
    included_nodes = set()

    for src_node in node_set:
        for dst_node in node_set:
            if src_node == dst_node:
                continue
            included_nodes.update(set(nx.shortest_path(graph, source=src_node, target=dst_node)))

    return nx.subgraph(graph, included_nodes)


def common_neighbors_subgraph(graph, target_nodes: Iterable[str]):
    node_set = set(target_nodes)
    included_nodes = set()

    for src_node in node_set:
        for dst_node in node_set:
            if src_node == dst_node:
                continue
            included_nodes.update(set(nx.common_neighbors(graph, src_node, dst_node)))

    return nx.subgraph(graph, (included_nodes | node_set))
