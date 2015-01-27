import os
import shutil

# input_address = '/Users/yorko/Documents/workspace/graphlet_lazy/input/'
input_address = "C:\\Users\\User\\Documents\\eclipse_workspace\\graphlet_lazy\\input\\"
PTC_train_address = input_address + "PTC_training_set\\"
label_file_address = input_address + "training_set_results.txt"
classes = {"CE":1, "SE":1, "P":1, "NE":0, "N":0, "EE":-1, "E":-1, "IS":-1}

def mol_nodes_and_edges(mol_name, train_address):
    full_mol_address = train_address + mol_name
    f = open(full_mol_address,'r')
    f.readline()
    f.readline()
    f.readline()
    [node_num, edge_num] = [int(val) for val in f.readline().split()[:2]]
    return node_num, edge_num

def copy_mols(classtype, label, train_address, mol_name):
    
    full_mol_address = train_address + mol_name
    positive_dest = train_address + classtype + "_positive"
    negative_dest = train_address + classtype + "_negative"
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
                copy_mols(classtype, label, PTC_train_address, mol_name)

def select_labels(test_address, label_file_address, grouptype="MR"):
    labels = []
    test_molecules = os.listdir(test_address)
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
#     select_small_molecules(label_file_address, PTC_train_address, 
#                            min_nodes=5, min_edges=5,
#                            max_nodes=20, max_edges=20)
    print select_labels("C:\Users\User\Documents\eclipse_workspace\graphlet_lazy\input\PTC_sample_53x45x44\MR_test", 
                  label_file_address, grouptype="MR")