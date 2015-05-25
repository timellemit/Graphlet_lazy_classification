import os
import shutil

input_address = os.path.join(os.path.join(os.pardir, os.pardir), os.path.join("input", "PTC"))
train_address = os.path.join(input_address,"train")
raw_train_labels_file_address = os.path.join(input_address,"train_set_results.txt")
raw_test_labels_file_address = os.path.join(input_address,"test_set_results.txt")
classes = {"CE":1, "SE":1, "P":1, "NE":0, "N":0, "EE":-1, "E":-1, "IS":-1}

def mol_nodes_and_edges(mol_name, train_address):
    full_mol_address = os.path.join(train_address, mol_name)
    f = open(full_mol_address,'r')
    f.readline()
    f.readline()
    f.readline()
    [node_num, edge_num] = [int(val) for val in f.readline().split()[:2]]
    return node_num, edge_num

def copy_mols(classtype, label, train_address, mol_name):
    
    full_mol_address = os.path.join(train_address, mol_name)
    positive_dest = os.path.join(train_address, classtype + "_positive")
    negative_dest = os.path.join(train_address, classtype + "_negative")
    try:
        os.makedirs(positive_dest)
        os.makedirs(negative_dest)
    except OSError:
        pass
    class_label = classes[label]
    if class_label == 1:
                if (os.path.isfile(full_mol_address)):
                    shutil.copy(full_mol_address, positive_dest)
    elif class_label == 0:
                if (os.path.isfile(full_mol_address)):
                    shutil.copy(full_mol_address, negative_dest)   

def select_small_molecules(label_file_address, train_address, 
                           min_nodes, min_edges,
                           max_nodes, max_edges):                       
    train_labels = open(label_file_address,'r')
    for line in train_labels:  
        elems = line.split(",")
        mol_name = elems[0].strip()
        node_num, edge_num = mol_nodes_and_edges(mol_name, train_address)
        for elem in elems[1:]:
            classtype, label = elem.strip().split("=")
            if min_nodes <= node_num <= max_nodes and \
                min_edges <= edge_num <= max_edges:
                copy_mols(classtype, label, train_address, mol_name)

def select_labels(test_address, label_file_address, grouptype="MR"):
    labels = []
    test_molecules = os.listdir(test_address)
    test_molecules = [mol.rstrip(".sdf") for mol in test_molecules]
    print test_molecules
    train_labels = open(label_file_address,'r')
    for line in train_labels:  
        elems = line.split(",")
        mol_name = elems[0].strip()
        if mol_name in test_molecules:
            for elem in elems[1:]:
                # gtype - MR, FR, MM or FM
                gtype, label = elem.strip().split("=")
                if gtype == grouptype:
                    labels.append(classes[label])
    return labels
#     for mol_filename in test_mols_addresses:
#         full_file_name = os.path.join(test_address, mol_filename)
#         if (os.path.isfile(full_file_name)):
#             print mol_filename, full_file_name
#             shutil.copy(full_file_name, dest)
if __name__ == "__main__":
    select_small_molecules(raw_train_labels_file_address, train_address, 
                           min_nodes=0, min_edges=0,
                           max_nodes=2400, max_edges=2400)
#     print select_labels("C:\Users\User\Documents\eclipse_workspace\graphlet_lazy\input\PTC_training_set\original", 
#                   label_file_address, grouptype="MR")