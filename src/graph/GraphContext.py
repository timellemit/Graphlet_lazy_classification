from GraphDescription import GraphDescription
from GraphDescriptionElement import networkx_graph_init
import csv, glob


class GraphContext:
    
    def __init__(self, data_file_address, build_graphlets=False, 
                 min_nodes=1, max_nodes=100000, ptc=False):
        self.obj_num, self.attr_num = 0, 0
        self.obj_names = []
        self.table = []
        self.parsePTCData(input_address=data_file_address, 
                          build_graphlets=build_graphlets, 
                 min_nodes=min_nodes, max_nodes=max_nodes) \
        if ptc else self.parseData(data_file_address=data_file_address, 
                          build_graphlets=build_graphlets, 
                 min_nodes=min_nodes, max_nodes=max_nodes)
        
        
    def parseData(self, data_file_address, build_graphlets=False, 
                 min_nodes=1, max_nodes=100000):
        edge_list = []
        data = csv.reader(open(data_file_address))
        self.obj_num = int(data.next()[0])
        for i in xrange(self.obj_num):  # @UnusedVariable
#             print i
            self.obj_names.append(data.next()[0])
            edge_num = int(data.next()[0])
            node_labels = [str(label) for label in data.next()]
            for j in xrange(edge_num):  # @UnusedVariable
                node_from, node_to, bond_type = [int(elem) for elem in data.next()]
                new_edge = (node_from, node_to, {'type' : bond_type})
                edge_list.append(new_edge)
            self.table.append(GraphDescription([
                networkx_graph_init(node_labels, edge_list)], 
                build_graphlets, min_nodes, max_nodes)) 
    
    def parsePTCData(self, input_address, build_graphlets=False, 
                 min_nodes=1, max_nodes=100000, verbose=False):
        """
        TODO: modify input_address + filename
        so that it works from here
        """
        self.table = []
        for filename in glob.glob(input_address + "*"):
            self.obj_num += 1
            node_labels, edges = [], []
            f = open(filename,'r')
            f.readline()
            f.readline()
            f.readline()
            [node_num, edge_num] = [int(val) for val in f.readline().split()[:2]]
#             if node_num < 35:
            self.obj_names.append(filename[len(input_address):] + "_" +
                                  str(node_num) +"x" + str(edge_num))
            for node_id in xrange(node_num):
                lb = f.readline().split()[3]
                node_labels.append(lb)
            for edge_id in xrange(edge_num):
                [edge_from_id, edge_to_id, edge_type] = \
                [int(val)-1 for val in f.readline().split()[:3]]
                edge_dic = {}
                edge_dic['type'] = edge_type
                edges.append((edge_from_id, edge_to_id, edge_dic))
            self.table.append(GraphDescription([
                networkx_graph_init(node_labels,edges)], 
                build_graphlets, min_nodes, max_nodes))  
            if verbose:
                print filename
                print "{} nodes, {} edges.".format(node_num, edge_num)
          
if __name__ == "__main__":
#     context = GraphContext("../../input/toy_molecules_positive.csv",
#                            build_graphlets=True, min_nodes=3, max_nodes=3)
#     print context.table[0].is_sub_description(context.table[1], min_nodes=3,
#                                               max_nodes=3, verbose=True)
#     context = GraphContext("../../input/PTC_sample/test/",
#                            build_graphlets=False, min_nodes=3, 
#                            max_nodes=3, ptc=True)
    context = GraphContext("/Users/yorko/Documents/workspace/JSM_python/input/PTC_training_set/",
                           build_graphlets=False, min_nodes=3, 
                           max_nodes=3, ptc=True)
    
    print context.obj_num, "molecules parsed."
    print context.obj_names[0]
#     print context.table[81].intersect(context.table[123], min_nodes=3,
#                                               max_nodes=3, verbose=True)
#     print context.table[0].intersect(context.table[4], use_graphlets=True, 
#                                      min_nodes=3, max_nodes=3, verbose=True)
#                                               max_nodes=3, verbose=True)
#     for graph in context.table[0].value[0].graphlet_iter(3):
#         print graph.node
#     print context.table[0]