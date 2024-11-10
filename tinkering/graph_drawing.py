from graph.trait import get_trait_node_graph
from matplotlib import pyplot as plt
import networkx as nx

#my_g = single_trait_graph(12, 'Multistriker')
my_g = get_trait_node_graph(12, costs=[2, 3, 4, 5])

#positions = nx.spiral_layout(my_g)
#positions = nx.spring_layout(my_g)
positions = nx.bfs_layout(my_g, 'Witchcraft')


edge_labels = {(x[0], x[1],): x[2] for x in my_g.edges.data('label')}
nx.draw_networkx(
    my_g,
    pos=positions,
    with_labels=True,
    edge_color=nx.get_edge_attributes(my_g,'color').values(),
    width=3.0
)
nx.draw_networkx_edge_labels(my_g, positions, edge_labels=edge_labels)
plt.show()
