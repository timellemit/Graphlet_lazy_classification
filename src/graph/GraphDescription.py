from GraphDescriptionElement import GraphDescriptionElement,\
    networkx_graph_init
from graph.GraphDescriptionElement import graphlet_descs
from time import time
from matplotlib import pyplot as plt
"""
multiple graphs in one element
"""

class GraphDescription:
    def __init__(self, graphs, build_graphlets=False,

                 min_nodes=1, max_nodes=100000):
        """
        Initializes an instance of a childDescription class
        with a given container.
        """
        self.build_graphlets = build_graphlets
        if type(graphs) in [list, set, tuple]:
            self.value = [GraphDescriptionElement(elem, build_graphlets,
                        min_nodes, max_nodes) for elem in list(graphs)]
            # stores the raw list or set 
            self.raw_value = graphs
        else:
            raise Exception("A container of description elements is required")
        
    def intersect(self, other, use_graphlets=False, 
                  min_nodes=1, max_nodes=10000, verbose=False):
        if use_graphlets and not self.build_graphlets:
            Warning("Graphlets were not built")
            use_graphlets = False
        init_time = time()
        intersection = []
        if len(self.value) == len(other.value):
            for i in xrange(len(self.value)):
#                 print self.value[i], other.value[i]
                intersection.extend(self.value[i].
                                    meet(other.value[i], use_graphlets,
                                          min_nodes, max_nodes))
#             print "intersection ", intersection
            if verbose:
                print "Intersect time in sec: ", round(time() - init_time, 2)
            return GraphDescription([graph_elem.graph for graph_elem in intersection])
        return GraphDescription([])
    
    def is_sub_description(self, other, use_graphlets=False,
                           min_nodes=1, max_nodes=10000, verbose=True):
        """ Indicates whether one description is 
        subsumed by another. """
        if use_graphlets and not self.build_graphlets:
            Warning("Graphlets were not built")
            use_graphlets = False
        for graph_ind in xrange(len(self.value)):
            for other_graph_ind in xrange(len(other.value)):
                if not self.value[graph_ind].\
                    is_subgraph(other.value[other_graph_ind], 
                                use_graphlets,
                                min_nodes, max_nodes):
                    return False
        return True

    def __str__(self):
        s = "<"
        for elem in self.value:
            s += elem.__str__() + ", "
        s = s.rstrip(", ") + ">"
        return s
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.value)
    
    def draw(self, ax=None, num_x_subplots=1, num_y_subplots=1, nodesize=1000):
        _, axarr = plt.subplots(num_x_subplots, num_y_subplots)

        for i in xrange(num_x_subplots):
            for j in xrange(num_y_subplots):
                try:
                    self.value[i*num_y_subplots +j].draw(ax=axarr[i,j], show=False, nodesize=nodesize)
                    axarr[i,j].set_title('Graphlet '+ str(i*num_y_subplots +j+1))
                except IndexError:
                    pass
                
        plt.show()
    
def graphlet_descriptions(desc_set, training_set,
                          use_own_graphlets=False, 
                          graphlets=None,
                          min_nodes=3, max_nodes=3,
                          verbose=False):
    return graphlet_descs([elem for description in desc_set
                           for elem in description.value],
                          [elem for description in training_set
                           for elem in description.value],
                          use_own_graphlets=use_own_graphlets,
                          graphlets=graphlets,
                          min_nodes=min_nodes, 
                          max_nodes=max_nodes,
                          verbose=verbose
                          ) 
            
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
    map(lambda vertices: GraphDescription([networkx_graph_init(
                    vertices, molecule_structure)], build_graphlets=True,
                    min_nodes=3, max_nodes=3), molecule_vertices)
    print mol9.intersect(mol1, min_nodes=3, max_nodes=3, use_graphlets=True)#.\
#     is_sub_description(mol6, min_nodes=3, max_nodes=3)
    mol9.intersect(mol1, min_nodes=3, max_nodes=3, use_graphlets=True).draw(num_x_subplots=2, num_y_subplots=2)