import os
import numpy as np

input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
sample_adress = os.path.join(input_address, "PTC_sample_4x4x4")
descriptions_filename = os.path.join(sample_adress,"3_graphlet_descriptions.txt")
train_labels_filename = os.path.join(sample_adress,"train_labels.txt")
test_labels_filename = os.path.join(sample_adress,"test_labels.txt")

def parse_graphlet_descriptions(train_descriptions_filename, 
                                test_descriptions_filename,
                                train_labels_filename,
                                test_labels_filename):
    train_set, test_set = [], []
    train_labels, test_labels = [], []
    train_desc_file = open(train_descriptions_filename,'r')
    test_desc_file = open(test_descriptions_filename,'r')
    train_labels_file = open(train_labels_filename,'r')
    test_labels_file = open(test_labels_filename,'r')
    
    for line in train_labels_file:
        train_labels.append(int(line.strip()))
    for line in test_labels_file:
        test_labels.append(int(line.strip()))
    for line in train_desc_file:
        train_set.append(line.strip().split(","))
    for line in test_desc_file:
        test_set.append(line.strip().split(","))
        
    return np.array(train_set, dtype='int64'), np.array(test_set, dtype='int64'), \
            np.array(train_labels, dtype='int64'), np.array(test_labels, dtype='int64')

if __name__ == "__main__":
    input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
    sample_adress = os.path.join(input_address, "PTC_sample_4x4x4")
    train_descriptions_filename = os.path.join(sample_adress,
                                               "train_3_graphlet_descriptions.txt")
    test_descriptions_filename = os.path.join(sample_adress,
                                               "test_3_graphlet_descriptions.txt")
    train_labels_filename = os.path.join(sample_adress,"train_labels.txt")
    test_labels_filename = os.path.join(sample_adress,"test_labels.txt")
    train, test, train_labels, test_labels = \
     parse_graphlet_descriptions(train_descriptions_filename, 
                                test_descriptions_filename,
                                train_labels_filename,
                                test_labels_filename)
#     print train
#     train.tofile("train.txt")
    np.savetxt("train_4x4x4.txt",train,fmt='%d',delimiter=',')
    np.savetxt("test_4x4.txt",test,fmt='%d',delimiter=',')
    
