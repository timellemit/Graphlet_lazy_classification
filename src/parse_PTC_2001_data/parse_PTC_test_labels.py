input_address = '../../input/'
label_file_address = input_address + "PTC_labels.txt"
train_labels = open(label_file_address,'r')
MR_labels = open(input_address + "MR_labels.txt",'w')
FR_labels = open(input_address + "FR_labels.txt",'w')
MM_labels = open(input_address + "MM_labels.txt",'w')
FM_labels = open(input_address + "FM_labels.txt",'w')
for line in train_labels:
    elems = line.split()
    compound_id = elems[0]
    mr, fr, mm, fm = elems[2:6]
    MR_labels.write(str(compound_id) + "\t" + str(1 if mr == "+" else 0) + "\n")
    FR_labels.write(str(compound_id) + "\t" + str(1 if fr == "+" else 0) + "\n")
    MM_labels.write(str(compound_id) + "\t" + str(1 if mm == "+" else 0) + "\n")
    FM_labels.write(str(compound_id) + "\t" + str(1 if fm == "+" else 0) + "\n")
MR_labels.close()
FR_labels.close()
MM_labels.close()
FM_labels.close()