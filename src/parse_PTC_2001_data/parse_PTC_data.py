import glob
import networkx as nx

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

input_address = "C:\Users\User\Documents\eclipse_workspace\graphlet_lazy\input\PTC_training_set\original"
graphs = []
for filename in glob.glob(input_address + "*.sdf"):
    print filename
    node_labels, edges = [], []
    f = open(input_address + filename,'r')
    f.readline()
    f.readline()
    f.readline()
#     print f.readline().split()
    [node_num, edge_num] = [int(val) for val in f.readline().split()[:2]]
    print node_num, edge_num
    for node_id in xrange(node_num):
        node_labels.append(f.readline().split()[3])
    for edge_id in xrange(edge_num):
        [edge_from_id, edge_to_id, edge_type] = \
        [int(val) for val in f.readline().split()[:3]]
        edge_dic = {}
        edge_dic['type'] = edge_type
        edges.append((edge_from_id, edge_to_id, edge_dic))
    graphs.append(networkx_graph_init(node_labels,edges))

print graphs[0]