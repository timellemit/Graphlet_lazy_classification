from test_lazy_classify import test_lazy_classification,\
    accuracy_with_refusal
import os

if os.name == 'nt':
    input_address = "C:\\Users\\User\\Documents\\eclipse_workspace\\graphlet_lazy\\input\\" 
elif os.name == 'posix':
    input_address = "/Users/yorko/Documents/workspace/graphlet_lazy/input"
    
exp, pred = test_lazy_classification(
        input_address=input_address,
        pos_dir=os.path.join("PTC_sample_16x16x16","MR_positive"),
        neg_dir=os.path.join("PTC_sample_16x16x16","MR_negative"),
        test_dir=os.path.join("PTC_sample_16x16x16","MR_test"),
        labels_filename="training_set_results.txt",
        grouptype="MR",
        verbose=False)

print "Expected", exp
print "Predicted", pred
print accuracy_with_refusal(exp, pred, verbose=False)