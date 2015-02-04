# -*- coding: utf-8 -*-
from graph.GraphClassify import GraphClassify
import os
from tests.test_lazy_classify import test_lazy_classification
from sklearn.metrics import metrics

# Полные адреса каталогов input, полож и отриц и тестовых примеров и их меток 
input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
all_labels_filename = os.path.join(input_address,"training_set_results.txt")
sample_adress = os.path.join(input_address, "PTC_sample_16x16x16")

for grouptype in ['MR', 'MM', 'FR', 'FM']:
    pos_dir = os.path.join(sample_adress, grouptype + "_positive")
    neg_dir = os.path.join(sample_adress, grouptype + "_negative")
    test_dir = os.path.join(sample_adress, grouptype + "_test")
    train_filename = os.path.join(sample_adress,
                                  grouptype + "_train_3_graphlet_descriptions.txt")
    test_filename = os.path.join(sample_adress,
                                grouptype + "_test_3_graphlet_descriptions.txt")
    train_labels_filename = os.path.join(sample_adress,
                                         grouptype + "_train_labels.txt")
    test_labels_filename = os.path.join(sample_adress,
                                        grouptype + "_test_labels.txt")

    # Параметры build_graphlets, min_nodes, max_nodes, означают, что
    # граф описывается множеством своих связных подграфов с числом вершин
    # от min_nodes до max_nodes
    molecules = GraphClassify(pos_cxt_file=pos_dir,
                              neg_cxt_file=neg_dir,
                              build_graphlets=True, 
                              min_nodes=3, max_nodes=3, ptc=True,
                              verbose=True)
    
    true_labels, lazy_pred = test_lazy_classification(
            input_address=input_address,
            pos_dir=pos_dir,neg_dir=neg_dir,
            test_dir=test_dir,
            labels_filename=all_labels_filename,
            grouptype=grouptype,
            weighted=True,
            verbose=True)
    
    svm_pred = molecules.svm_graphlet_classify(test_dir, all_labels_filename, 
                    grouptype=grouptype, 
                    descs_from_file=False,
                    train_filename=train_filename,
                    test_filename=test_filename, 
                    train_labels_filename=train_labels_filename, 
                    test_labels_filename=test_labels_filename, 
                    descs_to_file=True,
                    verbose=True)
    
    print "True labels: \n", true_labels
    print "Lazy prediction: \n", lazy_pred
    print "SVM prediction: \n", svm_pred
    print(metrics.classification_report(true_labels, lazy_pred))
    print(metrics.confusion_matrix(true_labels, lazy_pred)) 
    print(metrics.classification_report(true_labels, svm_pred))
    print(metrics.confusion_matrix(true_labels, svm_pred)) 