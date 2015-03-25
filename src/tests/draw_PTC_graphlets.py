import os
from graph.GraphClassify import GraphClassify
from graph.GraphDescription import GraphDescription

input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
labels_filename = os.path.join(input_address, "training_set_results.txt")
sample_adress = os.path.join(input_address, "PTC_sample_4x4x4")

pos_dir=os.path.join(sample_adress,"MR_positive")
neg_dir=os.path.join(sample_adress,"MR_negative")
test_dir=os.path.join(sample_adress,"MR_test")

molecules = GraphClassify(pos_cxt_file=pos_dir,
                          neg_cxt_file=neg_dir,
                        build_graphlets=True, 
                        min_nodes=4, max_nodes=4, ptc=True) 

print "TR206: {0} graphlets".format(str(len(molecules.positive_cxt.table[0].value[0].all_k_graphlets(4))))
GraphDescription(graphs=[elem.graph for elem in molecules.positive_cxt.table[0].value[0].all_k_graphlets(4)]).\
draw(num_x_subplots=4, num_y_subplots=4, nodesize=400)