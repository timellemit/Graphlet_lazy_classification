import networkx as nx
from GraphDescriptionElement import GraphDescriptionElement

g = nx.Graph()
g.add_edge(1,2);g.add_edge(1,3)
g.add_edge(1,7);g.add_edge(2,4)
g.add_edge(3,4);g.add_edge(3,5)
g.add_edge(3,6);g.add_edge(4,5)
g.add_edge(5,6);g.add_edge(6,7)

# g = GraphDescriptionElement(g)
import itertools

target = nx.Graph()
target.add_edge(1,2)
target.add_edge(2,3)
# target = GraphDescriptionElement(target)

print g, target
for sub_nodes in itertools.combinations(g.nodes(),len(target.nodes())):
    subg = g.subgraph(sub_nodes)
    if nx.is_connected(subg):#Sand nx.is_isomorphic(subg, target):
        print subg.edges()