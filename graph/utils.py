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


def links_subgraph_by_nodes(base_graph, target_nodes):

    edges_to_keep = set()
    for edge in base_graph.edges:
        if edge[0] in target_nodes and edge[1] not in target_nodes:
            edges_to_keep.add(edge)
        elif edge[1] in target_nodes and edge[0] not in target_nodes:
            edges_to_keep.add(edge)
        elif edge[0] in target_nodes and edge[1] in target_nodes:
            edges_to_keep.add(edge)
        else:
            continue

    first_round_subgraph = nx.edge_subgraph(base_graph, edges=edges_to_keep)
    return first_round_subgraph


def links_subgraph_by_edges(base_graph, target_edges):

    target_nodes = set()
    for edge in target_edges:
        target_nodes.add(edge[0])
        target_nodes.add(edge[1])

    first_round_subgraph = links_subgraph_by_nodes(base_graph, target_nodes)
    nodes_to_keep = set()
    node_list = sorted(first_round_subgraph.degree, key=lambda x: x[1], reverse=True)
    for item in node_list:
        if item[0] not in target_nodes:
            nodes_to_keep.add(item[0])
        if len(nodes_to_keep) == 3:
            break
    nodes_to_keep.update(target_nodes)
    return nx.induced_subgraph(first_round_subgraph, nodes_to_keep)


def get_edges_by_attribute(graph, attribute, target: str | Iterable[str]):
    if isinstance(target, str):
        values = [target]
    else:
        values = target
    return [x for x in graph.edges.data() if x[2].get(attribute) in values]
