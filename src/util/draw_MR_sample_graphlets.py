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
                        min_nodes=3, max_nodes=3, ptc=True) 

pos_mol_names, neg_mol_names = ["TR206","TR245","TR267", "TR331"], [ "TR068", "TR126", "TR165", "TR276"]

#molecules.positive_cxt.table[0].value[0].draw()
for i in xrange(len(pos_mol_names)):
#     print molecules.positive_cxt.table[i].value[0].graph.edge
    print "{0}: {1} graphlets".format(pos_mol_names[i], str(len(molecules.positive_cxt.table[i].value[0].all_k_graphlets(3))))
#     for j in xrange(len(molecules.positive_cxt.table[i].value[0].all_k_graphlets(4))):
# #         print molecules.positive_cxt.table[i].value[0].all_k_graphlets(4)[j].graph.edge
#         molecules.positive_cxt.table[i].value[0].all_k_graphlets(4)[j].draw()
    GraphDescription(graphs=[elem.graph for elem
                              in molecules.positive_cxt.table[i].value[0].all_k_graphlets(3)]).\
    draw(num_x_subplots=2, num_y_subplots=3, nodesize=1500)
    for gr in molecules.positive_cxt.table[i].value[0].all_k_graphlets(3):
        print gr.print_3_chain()

for i in xrange(len(neg_mol_names)):
    print "{0}: {1} graphlets".format(neg_mol_names[i], str(len(molecules.negative_cxt.table[i].value[0].all_k_graphlets(3))))

    GraphDescription(graphs=[elem.graph for elem in molecules.negative_cxt.table[i].value[0].all_k_graphlets(3)]).\
    draw(num_x_subplots=4, num_y_subplots=3, nodesize=1500)
    for gr in molecules.negative_cxt.table[i].value[0].all_k_graphlets(3):
        print gr.print_3_chain()