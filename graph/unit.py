from data_io.tft import TFTSetBlob, COLOR_MAP
import networkx as nx
import itertools


def get_unit_node_graph(set_blob: TFTSetBlob, costs=None):

    if not costs:
        costs = list(range(1, 6))

    graph = nx.Graph()
    for champ in set_blob.get_base_unit_data():
        if champ['cost'] not in costs:
            continue
        graph.add_node(
            champ['name'],
            cost=champ['cost'],
            label=champ['name'],
            color=COLOR_MAP[champ['cost']],
            traits=champ['traits']
        )

    trait_map = nx.get_node_attributes(graph, 'traits')
    for node_1, node_2 in itertools.combinations(graph.nodes, 2):
        shared_traits = set(trait_map[node_1]) & set(trait_map[node_2])
        if shared_traits:
            trait_string = ', '.join(shared_traits)
            graph.add_edge(node_1, node_2, label=trait_string)

    return graph
