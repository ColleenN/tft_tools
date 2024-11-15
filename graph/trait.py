import networkx as nx

from data_io.tft import get_base_data, get_unique_traits, COLOR_MAP


def get_trait_node_graph(set_num, show_unique_traits=False, costs=list(range(1, 6))):
    edge_list = []
    for champ in get_base_data(set_num):
        if champ['cost'] not in costs:
            continue
        edge_attrs = {
            'cost': champ['cost'],
            'label': champ['name'],
            'color': COLOR_MAP[champ['cost']]
        }
        if len(champ['traits']) > 1:
            edge_list.append((champ['traits'][0], champ['traits'][1], edge_attrs,))
        if len(champ['traits']) == 3:
            edge_list.append((champ['traits'][0], champ['traits'][2], edge_attrs,))
            edge_list.append((champ['traits'][1], champ['traits'][2], edge_attrs,))

    graph = nx.MultiGraph(edge_list)

    if not show_unique_traits:
        graph.remove_nodes_from(get_unique_traits(set_num))

    return graph


def single_trait(base_graph, trait_name):
    included_nodes = list(base_graph[trait_name].keys())
    included_nodes.append(trait_name)
    return base_graph.subgraph(included_nodes)
