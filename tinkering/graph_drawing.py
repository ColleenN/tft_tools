from graph.trait import get_trait_node_graph
from graph.unit import get_unit_node_graph
from data_io.tft import get_base_unit_data, get_unique_traits
from matplotlib import pyplot as plt
import networkx as nx


def draw_trait_web(trait_graph, layout):
    edge_labels = {(x[0], x[1],): x[2] for x in trait_graph.edges.data('label')}

    plt.figure(1, figsize=(20, 10))
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    nx.draw_networkx(
        trait_graph,
        pos=layout,
        with_labels=True,
        node_color=nx.get_node_attributes(trait_graph, 'color').values(),
        width=3.0
    )
    nx.draw_networkx_edge_labels(trait_graph, layout, edge_labels=edge_labels)
    plt.show()


def links_subgraph(base_graph, target_nodes):

    one_step_nodes = set()
    edges_to_keep = set()
    for edge in base_graph.edges:
        if edge[0] in target_nodes and edge[1] not in target_nodes:
            possible = edge[1]
            edges_to_keep.add(edge)
        elif edge[1] in target_nodes and edge[0] not in target_nodes:
            possible = edge[0]
            edges_to_keep.add(edge)
        else:
            continue

    first_round_subgraph = nx.edge_subgraph(base_graph, edges=edges_to_keep)


    return first_round_subgraph


target_nodes = []
unique_trait_names = {x[0] for x in get_unique_traits(13)}

for unit in get_base_unit_data(13):
    non_uniques = set(unit['traits']) - unique_trait_names

    if len(non_uniques) == 3 and unit['cost'] in [1, 2, 3]:
        target_nodes.append(unit['name'])


#trait_graph = nx.subgraph(initial_graph, set(target_nodes))
#nx.edge_subgraph()
#my_g = nx.compose(one_costs, two_costs)

initial_graph = get_unit_node_graph(13)
trait_graph = links_subgraph(initial_graph, {'Heimerdinger', 'Silco', 'Zoe'})
#final_layout = nx.spring_layout(initial_graph, pos=anchor_positions, fixed=one_costs.nodes)
draw_trait_web(trait_graph, nx.spring_layout(trait_graph))






