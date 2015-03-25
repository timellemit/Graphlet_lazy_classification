# -*- coding: utf-8 -*-
from graph.GraphClassify import GraphClassify
import os
from sklearn.metrics import metrics
from parse_PTC_2001_data.parse_PTC_train_labels import select_labels

# ������ ������ ��������� input, ����� � ����� � �������� �������� � �� ����� 
input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
all_labels_filename = os.path.join(input_address,"training_set_results.txt")
sample_adress = os.path.join(input_address, "PTC_sample_4x4x4")

for grouptype in ['MR']:#, 'MM', 'FR', 'FM']:
    pos_dir = os.path.join(sample_adress, grouptype + "_positive")
    neg_dir = os.path.join(sample_adress, grouptype + "_negative")
    test_dir = os.path.join(sample_adress, grouptype + "_test")
    train_filename = os.path.join(sample_adress,
                                  grouptype + "_train_4-graphlet_descriptions.txt")
    test_filename = os.path.join(sample_adress,
                                grouptype + "_test_4-graphlet_descriptions.txt")
    train_labels_filename = os.path.join(sample_adress,
                                         grouptype + "_train_labels.txt")
    test_labels_filename = os.path.join(sample_adress,
                                        grouptype + "_test_labels.txt")

    # ��������� build_graphlets, min_nodes, max_nodes, ��������, ���
    # ���� ����������� ���������� ����� ������� ��������� � ������ ������
    # �� min_nodes �� max_nodes
    molecules = GraphClassify(pos_cxt_file=pos_dir,
                              neg_cxt_file=neg_dir,
                              build_graphlets=True, 
                              min_nodes=4, max_nodes=4, ptc=True,
                              verbose=True)
    
    true_labels = select_labels(
        test_address=test_dir, 
        label_file_address=all_labels_filename, 
        grouptype=grouptype)
    
    lazy_pred =  molecules.lazy_graphlet_classify(test_dir, 
                                                  all_labels_filename, 
                grouptype=grouptype, 
                descs_from_file=False,
                train_filename=train_filename,
                test_filename=test_filename, 
                train_labels_filename=train_labels_filename, 
                test_labels_filename=test_labels_filename, 
                descs_to_file=True,
                verbose=True)