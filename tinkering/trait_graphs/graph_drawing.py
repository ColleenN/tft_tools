from graph.trait import get_trait_node_graph
from data_io.tft import TFTSetBlob
import networkx as nx

from graph.utils import draw_trait_web

current_set_blob = TFTSetBlob(17)
initial_graph = get_trait_node_graph(current_set_blob)

draw_trait_web(initial_graph, nx.spring_layout(initial_graph))

