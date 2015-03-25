# -*- coding: utf-8 -*-
from graph.GraphClassify import GraphClassify
import os
from sklearn.metrics import metrics
from parse_PTC_2001_data.parse_PTC_train_labels import select_labels
import numpy as np

input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
all_labels_filename = os.path.join(input_address,"training_set_results.txt")
sample_adress = os.path.join(input_address, "PTC_training_set")

#def form_latex_output():

for grouptype in ['MM', 'FR', 'FM', 'MR']:
    report = np.array()
    pos_dir = os.path.join(sample_adress, grouptype + "_positive")
    neg_dir = os.path.join(sample_adress, grouptype + "_negative")
    test_dir = os.path.join(sample_adress, grouptype + "_test")
    true_labels = select_labels(
            test_address=test_dir, 
            label_file_address=all_labels_filename, 
            grouptype=grouptype)
    for k_nodes in [4,5]:
        subreport_lazy, subreport_svm = np.array(), np.array()
        print "Grouptype: {0}, {1}-graphlets".format(grouptype, str(k_nodes))
        train_filename = os.path.join(sample_adress,
                                      grouptype + "_train_{0}-graphlet_descriptions.txt".format(k_nodes))
        test_filename = os.path.join(sample_adress,
                                    grouptype + "_test_{0}-graphlet_descriptions.txt".format(k_nodes))
        train_labels_filename = os.path.join(sample_adress,
                                             grouptype + "_train_labels.txt")
        test_labels_filename = os.path.join(sample_adress,
                                            grouptype + "_test_labels.txt")
    
        molecules = GraphClassify(pos_cxt_file=pos_dir,
                                  neg_cxt_file=neg_dir,
                                  build_graphlets=True, 
                                  min_nodes=k_nodes, max_nodes=k_nodes, ptc=True,
                                  verbose=False)
        
        lazy_pred, lazy_pred_time = molecules.lazy_graphlet_classify(test_dir, 
                                                      all_labels_filename, 

                    grouptype=grouptype, 
                    descs_from_file=False,
                    train_filename=train_filename,
                    test_filename=test_filename, 
                    train_labels_filename=train_labels_filename, 
                    test_labels_filename=test_labels_filename, 
                    descs_to_file=True,
                    verbose=False,
                    output_time=True)
        
        svm_pred, svm_pred_time = molecules.svm_graphlet_classify(test_dir, all_labels_filename, 
                        grouptype=grouptype, 
                        descs_from_file=False,
                        train_filename=train_filename,
                        test_filename=test_filename, 
                        train_labels_filename=train_labels_filename, 
                        test_labels_filename=test_labels_filename, 
                        descs_to_file=True,
                        verbose=False,
                        output_time=True)
        subreport_lazy.append(k_nodes)
        subreport_lazy.append(metrics.accuracy_score(true_labels, lazy_pred))
        # add precision, recall and F-score to the report
        subreport_lazy.extend(metrics.precision_recall_fscore_support(true_labels, lazy_pred, average="macro")[:3])
        subreport_lazy.append(lazy_pred_time)
        report.append(subreport_lazy)
        
        subreport_svm.append(k_nodes)
        subreport_svm.append(metrics.accuracy_score(true_labels, svm_pred))
        # add precision, recall and F-score to the report
        subreport_svm.extend(metrics.precision_recall_fscore_support(true_labels, svm_pred, average="macro")[:3])
        subreport_svm.append(svm_pred_time)
        report.append(subreport_svm)
        
        print "True labels: \n", true_labels
        print "Lazy prediction: \n", lazy_pred
        print "SVM prediction: \n", svm_pred
        print "Lazy time: {0}, SVM time: {1}".format(lazy_pred_time, svm_pred_time)
        print(metrics.classification_report(true_labels, lazy_pred))
        print(metrics.confusion_matrix(true_labels, lazy_pred)) 
        print(metrics.classification_report(true_labels, svm_pred))
        print(metrics.confusion_matrix(true_labels, svm_pred)) 
        
np.savetxt("report.txt",report,fmt='%d',delimiter=',')