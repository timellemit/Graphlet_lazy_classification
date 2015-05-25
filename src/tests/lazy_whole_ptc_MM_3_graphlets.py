# -*- coding: utf-8 -*-
from graph.GraphClassify import GraphClassify
import os
from sklearn.metrics import metrics
from parse_PTC_2001_data.parse_PTC_test_labels import select_labels
import numpy as np

input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
train_labels_filename = os.path.join(input_address,"training_set_results.txt")
test_labels_filename = os.path.join(input_address,"test_set_results.txt")
sample_adress = os.path.join(input_address, "PTC")
MM_train_labels_address = os.path.join(sample_adress,"MM_train_labels.txt")
MM_test_labels_address = os.path.join(sample_adress,"MM_test_labels.txt")

for grouptype in ['MM','FR','FM', 'MR']:
    group_report = np.array([])
    pos_dir = os.path.join(sample_adress, grouptype + "_positive_sample")
    neg_dir = os.path.join(sample_adress, grouptype + "_negative_sample")
    test_dir = os.path.join(sample_adress, "test")
    true_labels = select_labels(MM_test_labels_address)
    for k_nodes in [5]:#,4]:#,5,6]:
        subreport_lazy, subreport_svm = np.array([]), np.array([])
        print "Grouptype: {0}, {1}-graphlets".format(grouptype, str(k_nodes))
        train_graphlet_filename = os.path.join(sample_adress,
                                      grouptype + "_train_{0}-graphlet_descriptions.txt".format(k_nodes))
        test_graphlet_filename = os.path.join(sample_adress,
                                    grouptype + "_test_{0}-graphlet_descriptions.txt".format(k_nodes))
        train_labels_filename = os.path.join(sample_adress,
                                             grouptype + "_train_labels.txt")
        test_labels_filename = os.path.join(sample_adress,
                                            grouptype + "_test_labels.txt")
     
        molecules = GraphClassify(pos_cxt_file=pos_dir,
                                  neg_cxt_file=neg_dir,
                                  build_graphlets=True, 
                                  min_nodes=2, max_nodes=k_nodes, ptc=True,
                                  verbose=False)
         
        lazy_pred, lazy_pred_time = molecules.lazy_graphlet_classify2(
                    pos_dir=pos_dir, neg_dir=neg_dir,
                    test_dir=test_dir, 
                    descs_from_file=False,
                    train_graphlet_filename=train_graphlet_filename,
                    test_graphlet_filename=test_graphlet_filename, 
                    train_labels_file=train_labels_filename, 
                    descs_to_file=True,
                    verbose=False,
                    output_time=True)
#         
    print "True labels: \n", true_labels
    print "Lazy prediction: \n", lazy_pred
    print "Accuracy: ", metrics.accuracy_score(true_labels, lazy_pred)
    print(metrics.classification_report(true_labels, lazy_pred))
    print(metrics.confusion_matrix(true_labels, lazy_pred)) 
    fpr, tpr, _ = metrics.roc_curve(true_labels, lazy_pred)
    print "TPR: ", tpr
    print "FPR: ", fpr
    print "AUC score:", metrics.roc_auc_score(true_labels, lazy_pred)
    