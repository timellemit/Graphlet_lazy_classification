from time import time
from graph.GraphClassify import GraphClassify
from parse_PTC_2001_data.parse_PTC_train_labels import select_labels
import numpy as np
import os

def test_lazy_classification(input_address, pos_dir, neg_dir, test_dir,
                             grouptype,
                             labels_filename="training_set_results.txt",
                             use_graphlets=True, min_nodes=3, max_nodes=3,
                             weighted=False,
                             parse_ptc=True, verbose=True):
    init_time = time()
    test_dir_address = os.path.join(input_address, test_dir)
    molecules = GraphClassify(pos_cxt_file=os.path.join(input_address,pos_dir),
                              neg_cxt_file=os.path.join(input_address,neg_dir),
                              build_graphlets=use_graphlets, 
                              min_nodes=min_nodes, max_nodes=max_nodes, ptc=parse_ptc) 
    predicted = molecules.lazy_classify(test_cxt_file=test_dir_address,
                                        use_graphlets=use_graphlets,
                                        min_nodes=min_nodes, max_nodes=max_nodes,
                                        weighted=weighted, 
                                        ptc=parse_ptc, verbose=verbose)
    expected = select_labels(
        test_address=test_dir_address, 
        label_file_address=os.path.join(input_address,labels_filename), 
        grouptype=grouptype)
    print "Classification time in sec: ", round(time() - init_time, 2) 
    return np.array(expected), np.array(predicted)

def accuracy_with_refusal(expected, predicted, verbose=True):
    no_refuse_indexes = (predicted != -1)
    accuracy_no_refuse = round(float(sum(expected[no_refuse_indexes] == 
                             predicted[no_refuse_indexes]))/
                                        sum(no_refuse_indexes),2)
    total_accuracy = round(float(sum(expected == predicted))/
                                        expected.shape[0],2)
    if verbose:
        print "Expected labels: ", expected
        print "Predicted labels: ", predicted
        print "Total accuracy: ", total_accuracy
        print "Accuracy when no refusal: ", accuracy_no_refuse
    return total_accuracy, accuracy_no_refuse

if __name__ == "__main__":
    input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
    pos_dir = os.path.join(os.path.join(input_address,"PTC_toy_sample_4x4x4"),
                       "MR_positive")
    neg_dir = os.path.join(os.path.join(input_address,"PTC_toy_sample_4x4x4"),
                       "MR_negative")
    test_dir = os.path.join(os.path.join(input_address,"PTC_toy_sample_4x4x4"),
                        "MR_test")
    labels_filename = os.path.join(input_address,"training_set_results.txt")
    exp, pred = test_lazy_classification(
        input_address=input_address,
        pos_dir=pos_dir,
        neg_dir=neg_dir,
        test_dir=test_dir,
        grouptype="MR",
        labels_filename=labels_filename)
#     print exp, pred
    
#     exp, pred = test_lazy_classification(
#         input_address="C:\\Users\\User\\Documents\\eclipse_workspace\\graphlet_lazy\\input\\",
#         pos_dir="PTC_training_set\\MR_positive",
#         neg_dir="PTC_training_set\MR_negative",
#         test_dir="PTC_training_set\MR_test",
#         labels_filename="training_set_results.txt")
    accuracy_with_refusal(exp, pred)
    