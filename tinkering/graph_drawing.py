from typing import Iterable

from graph.unit import get_unit_node_graph
from graph.trait import get_trait_node_graph
from data_io.tft import TFTSetBlob
import networkx as nx

from graph.utils import draw_trait_web, common_neighbors_subgraph


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


current_set_blob = TFTSetBlob(13)
current_set_blob.offline = True
from pprint import pprint
initial_graph = get_trait_node_graph(current_set_blob)
initial = {'Black Rose'}
one_step = nx.neighbors(initial_graph, 'Black Rose')
other_edges = initial_graph.edges(one_step, data='cost')
pprint(other_edges)
edges_to_keep = {(e[0], e[1]) for e in other_edges if e[2] > 3}
edges_to_keep.update(initial_graph.edges(initial))


pprint(edges_to_keep)
trait_graph = nx.edge_subgraph(initial_graph, edges_to_keep)

#edges = get_edges_by_attribute(initial_graph, 'label', {'Silco', 'Heimerdinger', 'Zoe'})
#'Visionary', 'Academy', 'Chem-Baron', 'Dominator', 'Sorcerer', 'Rebel', 'Black Rose'
#trait_graph = common_neighbors_subgraph(initial_graph, {'Visionary', 'Dominator', 'Sorcerer'})
#trait_graph = nx.subgraph(
#    initial_graph, {'Visionary', 'Academy', 'Chem-Baron', 'Dominator', 'Sorcerer', 'Rebel', 'Black Rose'})
#get_edges_by_attribute(initial_graph, 'label', {'Dr. Mundo', 'Illaoi', 'Garen'})


#final_layout = nx.spring_layout(initial_graph, pos=anchor_positions, fixed=one_costs.nodes)

draw_trait_web(trait_graph, nx.spring_layout(trait_graph))








# unique_trait_names = {x[0] for x in current_set_blob.get_unique_traits()}
#
# for unit in current_set_blob.get_base_unit_data():
#     non_uniques = set(unit['traits']) - unique_trait_names
#
#     if len(non_uniques) == 3 and unit['cost'] in [1, 2, 3]:
#         target_nodes.append(unit['name'])