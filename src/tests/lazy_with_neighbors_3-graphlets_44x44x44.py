# -*- coding: utf-8 -*-
from graph.GraphClassify import GraphClassify
import os
from sklearn.metrics import metrics
from parse_PTC_2001_data.parse_PTC_train_labels import select_labels

# Полные адреса каталогов input, полож и отриц и тестовых примеров и их меток 
input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
all_labels_filename = os.path.join(input_address,"training_set_results.txt")
sample_adress = os.path.join(input_address, "PTC_sample_44x44x44")

for grouptype in ['MR']:#, 'MM', 'FR', 'FM']:
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
    
    true_labels = select_labels(
        test_address=test_dir, 
        label_file_address=all_labels_filename, 
        grouptype=grouptype)
    
    
    lazy_pred =  molecules.lazy_graphlet_classify_with_neighbors(
                pos_dir=pos_dir, neg_dir=neg_dir, test_dir=test_dir, 
                descs_from_file=True,
                train_graphlet_filename=train_filename,
                test_graphlet_filename=test_filename, 
                descs_to_file=False,
                similarity_threshold=0.9,
                verbose=True,
                output_time=False)
    
    
    
    print "True labels: \n", true_labels
    print "Lazy prediction: \n", lazy_pred
    print(metrics.classification_report(true_labels, lazy_pred))
    print(metrics.confusion_matrix(true_labels, lazy_pred)) 