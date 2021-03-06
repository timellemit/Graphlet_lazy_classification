import networkx as nx
from itertools import combinations
from matplotlib import pyplot as plt
from time import time

class GraphDescriptionElement(nx.Graph):
    def __init__(self, graph, build_graphlets=False, 
                 min_nodes=3, max_nodes=3, verbose=False):
        self.graph = graph
        self.build_graphlets = build_graphlets
        if self.build_graphlets:
            self.min_nodes, self.max_nodes = min_nodes, max_nodes
            self.graphlets = self.all_graphlets(min_nodes, max_nodes)
            if verbose:
                print "Graphlets", self.graphlets
            
            
    def is_connected(self):
        return nx.is_connected(self.graph)
    
    def is_isomorphic(self, other):
        def node_match(n1,n2):
            return n1['label'] == n2['label']
        def edge_match(e1,e2):  
            return e1['type'] == e2['type']
        return nx.is_isomorphic(self.graph, other.graph, 
                                    node_match=node_match, 
                                    edge_match = edge_match)
    
    def is_subgraph(self, other, use_graphlets=False,
                    min_nodes=3, max_nodes=3):
        meet  = self.meet(other, use_graphlets, min_nodes, max_nodes)
#         print "is_subgraph", meet
        if len(meet) == 1:
            return meet[0].is_isomorphic(self)  
        else:
            return False  
    
    def all_k_graphlets(self, k_nodes):
        graphlets = []
        for node_subset in combinations(self.graph.nodes(), k_nodes):
#             print node_subset
            subgraph = GraphDescriptionElement(self.graph.subgraph(node_subset))
            if subgraph.is_connected():
                if subgraph.unique_graphlet(graphlets):
                    graphlets.append(subgraph)
        return graphlets
    
    def all_graphlets(self, min_nodes, max_nodes):
        all_graphlets = []
        for n_nodes in xrange(max_nodes, min_nodes - 1, -1):  
            all_graphlets.extend(self.all_k_graphlets(n_nodes))  
        return  all_graphlets  
                                     
    def graphlet_iter(self, k_nodes, build_graphlets=True,verbose=False):
        for node_subset in combinations(self.graph.nodes(), k_nodes):
#             print node_subset
            subgraph = GraphDescriptionElement(self.graph.subgraph(node_subset),
                                               build_graphlets,
                                               verbose=verbose,
                                               min_nodes=k_nodes, max_nodes=k_nodes)
            if subgraph.is_connected():
                yield subgraph
    
    def unique_graphlet(self, graphlets):             
            for graphlet in graphlets:
#                 print self.graph.node
#                 print graphlet.graph.node
                if isomorphic(self.graph, graphlet.graph):
                    return False
            return True
        
    def meet(self, other, use_graphlets=False, 
             min_nodes=3, max_nodes=3, 
             verbose=False):
        init_time = time()
        meet = []
        for n_nodes in xrange(min(len(self.graph), len(other.graph), 
                                  max_nodes), min_nodes - 1, -1):
            if use_graphlets:
                for gr1 in self.graphlets:
                    for gr2 in other.graphlets:
                        if gr1.is_isomorphic(gr2):
                            if gr1.unique_graphlet(meet):
                                    meet.append(gr1)
        
            else:
                for gr1 in self.graphlet_iter(n_nodes):
                    for gr2 in other.graphlet_iter(n_nodes):
                        if gr1.is_isomorphic(gr2):
                            if gr1.unique_graphlet(meet):
                                    meet.append(gr1)
        if verbose:
            print "meet time in sec: ", round(time() - init_time, 2)
        if meet:
            return meet
        return []
    
    def print_3_chain(self):
        edge_type_dic = {1:'-', 2:"="}
        if len(self.graph.node) == 0: # empty graph
            return ""
        else: # non-empty graph, initialize with the first atom label
            prev_from_id = self.graph.edges()[0][0]
            prev_to_id = prev_from_id
            s = self.graph.node[prev_from_id]["label"]
            
        for edge in self.graph.edges(data=True): # like [(0,1,{'type':1}),(1,2,{'type':2})]
            node_to_id, node_from_id, edge_type = edge[0], edge[1], edge[2]['type']
            if node_from_id == prev_from_id:
                s = self.graph.node[node_to_id]["label"] + edge_type_dic[edge_type] + s
                
            elif node_to_id == prev_from_id:
                s = self.graph.node[node_from_id]["label"] + edge_type_dic[edge_type] + s
                prev_from_id = node_from_id
            elif node_from_id == prev_to_id:
                s +=  edge_type_dic[edge_type] + self.graph.node[node_to_id]["label"]
            elif node_to_id == prev_to_id:
                s +=  edge_type_dic[edge_type] + self.graph.node[node_from_id]["label"]
            else: # impossible for 3-node chains
                pass
            prev_from_id, prev_to_id = node_from_id, node_to_id
        return s

    def __str__(self):
#         labels_coding = {'a': 'CH3', 'b': 'OH', 'c':'C', 'd': 'NH2','e': 'Cl'}
        s = ""
#         print self.graph
        for i in self.graph.nodes():
            s += str(i) + self.graph.node[i]["label"] +"-"
#             s += labels_coding[self.graph.node[i]["label"]] +"-"
        s = s.rstrip("-")
        return s
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.graph)
    
    def draw(self, ax=None, show=True, nodesize=1000):
        col = {'a' : 1, 'b': 0.75, 'c': 0.8, 'd': 0.67, 'e': 0.77, 
               'Br' : 'darkgreen', 'C': 'yellow', 'Cl': 'magenta', 'H': 'red', 'N': 'cyan',
               'O' : 'coral', 'Na':'crimson'}
        colors = [col.get(self.graph.node[node]['label']) for node in self.graph.nodes()]
        labels = {}
        for i in self.graph.nodes():
            labels[i] = self.graph.node[i]['label']
        edge_styles = [('solid' if edge_type == 1 else "dashed") for edge_type in [edge[2]['type'] for edge in self.graph.edges(data=True)]]    
        nx.draw_networkx(self.graph, node_size=nodesize, 
                node_color = colors, labels = labels, ax=ax, style=edge_styles)
        if show:
            plt.show()
    
def networkx_graph_init(node_labels, edges):
    """
    Initializes an instance of a networkx.Graph class
    with node_labels and edges.
    :type node_labels: list
    :param node_labels: a list of node labels as strings 
    :type edges: list
    :param edges: a list of tuples (x,y, edge_dic) where x and y
    are node indexes, edge_dic is a dictionary of edge properties.
    ###############################################################
    # Example:
    node_labels = ['a', 'c', 'b', 'c', 'd', 'd']
    edges_dict = [(0, 1, {'type' : 1}), (1, 2, {'type' : 1}), 
                  (1, 3, {'type' : 2}), (3, 4, {'type' : 1}), 
                  (5, 3, {'type' : 1})]
    graph1 = networkx_graph_init(node_labels, edges_dict)
    ###############################################################
    """ 
    graph = nx.Graph()
    graph.add_nodes_from(range(len(node_labels)))
    graph.add_edges_from(edges)
    for i in xrange(len(node_labels)):
        graph.node[i]['label'] = node_labels[i]
    return graph       

def graphlet_descs(desc_set, training_set, 
                   use_own_graphlets=True,
                   graphlets=None,
                   min_nodes=3, max_nodes=3,
                   verbose=False):
        def node_match(n1,n2):
            return n1['label'] == n2['label']
        def edge_match(e1,e2):
            return e1['type'] == e2['type']
         
        init_time = time()                     
        desc_vectors = []
#         print "train_descs", graphlets
        for n_nodes in xrange(max_nodes, min_nodes - 1, -1):
            for elem in desc_set: 
                new_desc = []
                for graphlet_ind in xrange(len(graphlets)):
                    for example_subgraph in elem.graphlet_iter(n_nodes):
                     
                        is_isomorphic_to_some_graphlet = False
                        if example_subgraph.is_isomorphic(graphlets[graphlet_ind]):
                            is_isomorphic_to_some_graphlet = True
                            break
                    new_desc.append(int(is_isomorphic_to_some_graphlet))
                desc_vectors.append(new_desc)
        if verbose:
            print "graphlet_descs time: ", round(time() - init_time, 2)
        return graphlets, desc_vectors
                
def isomorphic(nx_graph1, nx_graph2):
        def node_match(n1,n2):
            return n1['label'] == n2['label']
        def edge_match(e1,e2):  
            return e1['type'] == e2['type']
        return nx.is_isomorphic(nx_graph1, nx_graph2, 
                                    node_match=node_match, 
                                    edge_match = edge_match)
                 
if __name__ == "__main__":
    molecule_structure = [(0, 2, {'type' : 1}), (1, 2, {'type' : 1}), 
                                    (2, 3, {'type' : 2}), (3, 4, {'type' : 1}), 
                                    (5, 3, {'type' : 1})]
    molecule_vertices = [['a', 'b', 'c', 'c', 'd', 'd'],
                         ['a', 'b', 'c', 'c', 'b', 'd'],
                         ['a', 'b', 'c', 'c', 'a', 'e'],
                         ['a', 'e', 'c', 'c', 'b', 'e'],
                         ['a', 'd', 'c', 'c', 'd', 'd'],
                         ['a', 'e', 'c', 'c', 'b', 'd'],
                         ['b', 'd', 'c', 'c', 'd', 'e'],
                         ['a', 'b', 'c', 'c', 'd', 'e'], 
                         ['a', 'd', 'c', 'c', 'b', 'e']]
    mol1, mol2, mol3, mol4, mol5, mol6, mol7, mol8, mol9 = \
    map(lambda vertices: GraphDescriptionElement(networkx_graph_init(
                    vertices, molecule_structure), build_graphlets=False),
                    molecule_vertices)
    train_set = [mol1, mol2, mol3, mol4, mol5, mol6, mol7]
#     train_set = [mol1, mol2, mol3]
    test_set = [mol8, mol9]
#     print mol1.meet(mol9, min_nodes=3, max_nodes=3, verbose=True)[0].\
#     is_subgraph(mol6, min_nodes=3, max_nodes=3)
#     for gr in mol5.graphlet_iter(3):
#         print gr.node
#     graphlets, train_descs =  graphlet_descs(train_set, train_set,
#                                              use_own_graphlets=False,
#                                              verbose=True)
#     print train_descs
#     print graphlet_descs(desc_set=test_set, 
#                          training_set=train_set, 
#                          graphlets=graphlets,min_nodes=3,
#                          max_nodes=3)[1]

    mol1.draw()
    print mol1
#     for gr in mol1.graphlet_iter(4):
#         print gr.graph.edge
#         gr.draw()
    plt.show()