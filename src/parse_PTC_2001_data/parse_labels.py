import os, shutil


def parse_train_labels(input_address, train_address, raw_labels_address, grouptype="FM"):
    raw_train_labels = open(raw_labels_address,'r')
    labels_file = open(os.path.join(input_address, grouptype + "_train_labels.txt"),'w')
    try:
        os.makedirs(os.path.join(input_address, grouptype + "_train"))
    except WindowsError:
        pass
    for line in raw_train_labels:  
        elems = line.split(",")
        mol_name = elems[0].strip()
        for elem in elems[1:]:
            classtype, label = elem.strip().split("=")    
            if classtype == grouptype and classes[label] != -1:
                print mol_name, classtype, label
                try:
                    shutil.copy(os.path.join(train_address, mol_name), os.path.join(input_address, classtype + "_train"))
                except IOError:
                    pass
                labels_file.write(mol_name + "\t" + str(classes[label]) + "\n")
    raw_train_labels.close()
    labels_file.close()

def parse_test_labels(input_address, train_address, raw_labels_address, grouptype="FM"):
    grouptype_dic = {"MR":0, "FR":1, "MM":2, "FM":3}
    raw_test_labels = open(raw_labels_address,'r')
    labels_file = open(os.path.join(input_address, grouptype + "_test_labels.txt"),'w')
    raw_test_labels.readline()
    for line in raw_test_labels:
        elems = line.split()
        compound_id = elems[0]
        # label - + or - 
        label = elems[2:6][grouptype_dic[grouptype]]
        labels_file.write(str(compound_id) + "\t" + str(1 if label == "+" else 0) + "\n")
    raw_test_labels.close()
    labels_file.close()

def labels_to_array(labels_address):
    true_labels = []
    true_labels_file = open(labels_address,'r')
    for line in true_labels_file:
        true_labels.append(int(line.strip().split()[1]))
    return true_labels

if __name__ == "__main__":
    input_address = os.path.join(os.path.join(os.pardir, os.pardir), os.path.join("input", "PTC"))
    train_address = os.path.join(input_address,"train")
    raw_train_labels_file_address = os.path.join(input_address,"train_set_results.txt")
    raw_test_labels_file_address = os.path.join(input_address,"test_set_results.txt")
    classes = {"CE":1, "SE":1, "P":1, "NE":0, "N":0, "EE":-1, "E":-1, "IS":-1}
    
    parse_train_labels(input_address, train_address, raw_train_labels_file_address, grouptype="MR")
    parse_test_labels(input_address, train_address, raw_test_labels_file_address, grouptype="MR")
