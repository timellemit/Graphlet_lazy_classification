from time import time
from graph.GraphClassify import GraphClassify
from parse_PTC_2001_data.parse_PTC_train_labels import select_labels
import numpy as np

def test_lazy_classification(input_address, pos_dir, neg_dir, test_dir,
                             labels_filename="training_set_results.txt",
                             use_graphlets=True, min_nodes=3, max_nodes=3,
                             parse_ptc=True, verbose=True):
    init_time = time()
    test_dir_address = input_address+"\\"+test_dir+"\\"
    molecules = GraphClassify(pos_cxt_file=input_address+"\\"+pos_dir+"\\",
                              neg_cxt_file=input_address+"\\"+neg_dir+"\\",
                              build_graphlets=use_graphlets, 
                              min_nodes=min_nodes, max_nodes=max_nodes, ptc=parse_ptc) 
    predicted = molecules.lazy_classify(test_cxt_file=test_dir_address,
                                        use_graphlets=use_graphlets,
                                        min_nodes=min_nodes, max_nodes=max_nodes, 
                                        ptc=parse_ptc, verbose=verbose)
    expected = select_labels(
        test_address=test_dir_address, 
        label_file_address=input_address + labels_filename, 
        grouptype="MR")
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
    exp, pred = test_lazy_classification(
        input_address="C:\\Users\\User\\Documents\\eclipse_workspace\\graphlet_lazy\\input\\",
        pos_dir="PTC_sample_16x16x16\\positive",
        neg_dir="PTC_sample_16x16x16\\negative",
        test_dir="PTC_sample_16x16x16\\test",
        labels_filename="training_set_results.txt")
#     print exp, pred
    
#     exp, pred = test_lazy_classification(
#         input_address="C:\\Users\\User\\Documents\\eclipse_workspace\\graphlet_lazy\\input\\",
#         pos_dir="PTC_training_set\\MR_positive",
#         neg_dir="PTC_training_set\MR_negative",
#         test_dir="PTC_training_set\MR_test",
#         labels_filename="training_set_results.txt")
    accuracy_with_refusal(exp, pred)
    