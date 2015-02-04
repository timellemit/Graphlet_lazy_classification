# -*- coding: utf-8 -*-
from graph.GraphClassify import GraphClassify
import os

# Полные адреса каталогов input, полож и отриц и тестовых примеров и их меток 
input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
sample_adress = os.path.join(input_address, "PTC_sample_4x4x4")
all_labels_filename = os.path.join(input_address,"training_set_results.txt")

pos_dir = os.path.join(sample_adress, "MR_positive")
neg_dir = os.path.join(sample_adress, "MR_negative")
test_dir = os.path.join(sample_adress, "MR_test")
train_filename = os.path.join(sample_adress,
                                           "MR_train_3_graphlet_descriptions.txt")
test_filename = os.path.join(sample_adress,
                                          "MR_test_3_graphlet_descriptions.txt")
train_labels_filename = os.path.join(sample_adress,"MR_train_labels.txt")
test_labels_filename = os.path.join(sample_adress,"MR_test_labels.txt")
labels_filename = os.path.join(input_address,"training_set_results.txt")

# Класс для проверки разных способов классификации
# Параметры build_graphlets, min_nodes, max_nodes, означают, что
# граф описывается множеством своих связных подграфов с числом вершин
# от min_nodes до max_nodes
molecules = GraphClassify(pos_cxt_file=pos_dir,
                          neg_cxt_file=neg_dir,
                          build_graphlets=True, 
                          min_nodes=3, max_nodes=3, ptc=True,
                          verbose=True)

print molecules.svm_graphlet_classify(test_dir, all_labels_filename, 
                grouptype="MR", 
                descs_from_file=True,
                train_filename=train_filename,
                test_filename=test_filename, 
                train_labels_filename=train_labels_filename, 
                test_labels_filename=test_labels_filename, 
                descs_to_file=True,
                verbose=True)