# -*- coding: utf-8 -*-
from graph.GraphClassify import GraphClassify
import os
from sklearn.metrics import metrics
from parse_PTC_2001_data.parse_PTC_train_labels import select_labels
import numpy as np

input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
all_labels_filename = os.path.join(input_address,"training_set_results.txt")
sample_adress = os.path.join(input_address, "PTC_training_set")

report = np.array([])
for grouptype in ['MM']:#, 'FR','FM', 'MR']:
    group_report = np.array([])
    pos_dir = os.path.join(sample_adress, grouptype + "_positive_sample")
    neg_dir = os.path.join(sample_adress, grouptype + "_negative_sample")
    test_dir = os.path.join(sample_adress, grouptype + "_test_sample")
    true_labels = select_labels(
            test_address=test_dir, 
            label_file_address=all_labels_filename, 
            grouptype=grouptype)
    for k_nodes in [3]:#,4]:#,5]:#,6]:
        subreport_lazy = np.array([])
        print "Grouptype: {0}, {1}-graphlets".format(grouptype, str(k_nodes))
        train_filename = os.path.join(sample_adress,
                                      grouptype + "_train_sample_{0}-graphlet_descriptions.txt".format(k_nodes))
        test_filename = os.path.join(sample_adress,
                                    grouptype + "_test_sample_{0}-graphlet_descriptions.txt".format(k_nodes))
        train_labels_filename = os.path.join(sample_adress,
                                             grouptype + "_train_labels.txt")
        test_labels_filename = os.path.join(sample_adress,
                                            grouptype + "_test_labels.txt")
    
        molecules = GraphClassify(pos_cxt_file=pos_dir,
                                  neg_cxt_file=neg_dir,
                                  build_graphlets=True, 
                                  min_nodes=3, max_nodes=k_nodes, ptc=True,
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
                    verbose=True,
                    output_time=True)
        
        
        subreport_lazy = np.append(subreport_lazy, 1)
        subreport_lazy = np.append(subreport_lazy, k_nodes)
        subreport_lazy = np.append(subreport_lazy, metrics.accuracy_score(true_labels, lazy_pred))
        # add precision, recall and F-score to the report
        subreport_lazy = np.append(subreport_lazy, metrics.precision_recall_fscore_support(true_labels, lazy_pred, average="macro")[:3])
        subreport_lazy = np.append(subreport_lazy, lazy_pred_time)
        if len(group_report):
            group_report = np.vstack((group_report, subreport_lazy))
        else:
            group_report = subreport_lazy
        
        print "True labels: \n", true_labels
        print "Lazy prediction: \n", lazy_pred
        print(metrics.classification_report(true_labels, lazy_pred))
        print(metrics.confusion_matrix(true_labels, lazy_pred)) 
    if len(report):
            report = np.vstack((report, group_report))
    else:
        report = group_report
        
print report
np.savetxt(os.path.join("C:\\Users\\User\\YandexDisk", "report.txt"), report, fmt='%.2f',delimiter=',')