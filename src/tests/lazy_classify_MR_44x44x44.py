from test_lazy_classify import test_lazy_classification,\
    accuracy_with_refusal
import os

input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
    
exp, pred = test_lazy_classification(
        input_address=input_address,
        pos_dir=os.path.join("PTC_sample_44x44x44","MR_positive"),
        neg_dir=os.path.join("PTC_sample_44x44x44","MR_negative"),
        test_dir=os.path.join("PTC_sample_44x44x44","MR_test"),
        labels_filename="training_set_results.txt",
        grouptype="MR",
        weighted=True,
        verbose=True)

print "Expected", exp
print "Predicted", pred
print accuracy_with_refusal(exp, pred, verbose=True)