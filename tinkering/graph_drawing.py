from graph.trait import get_trait_node_graph
from graph.unit import get_unit_node_graph
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


#one_costs = get_trait_node_graph(13, costs=[1])
#anchor_positions = nx.circular_layout(one_costs)
initial_graph = get_unit_node_graph(13, costs=[4, 5])

#target_nodes = ['Darius', 'Violet', 'Camille', 'Urgot', 'Gangplank', 'Ambessa', 'Vi', 'Jayce', 'Sevika']
#target_nodes = ['Morgana', 'Cassiopeia', 'Heimerdinger'] # Blue Buff
#target_nodes = ['Draven', 'Zeri'] # Rageblade

#['Lux', 'Zyra', 'Powder', 'Vex']
#['Renata Glasc', 'Ziggs', 'Nami', 'Twisted Fate']
#['Dr. Mundo', 'Elise', 'Garen', 'Illaoi']
#target_nodes = ['Elise', 'Illaoi']


#one_step_nodes = [x[1] for x in initial_graph.edges if x[0] in target_nodes]
#print(one_step_nodes)
#one_step_nodes.extend([x[0] for x in initial_graph.edges if x[1] in target_nodes])
#target_nodes.extend(one_step_nodes)

#trait_graph = nx.subgraph(initial_graph, set(target_nodes))
#nx.edge_subgraph()


#my_g = nx.compose(one_costs, two_costs)

#final_layout = nx.spring_layout(my_g, pos=anchor_positions, fixed=one_costs.nodes)
draw_trait_web(initial_graph, nx.spring_layout(initial_graph, k=.1))






