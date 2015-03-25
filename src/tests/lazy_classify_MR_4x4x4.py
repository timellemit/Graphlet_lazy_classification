from test_lazy_classify import test_lazy_classification,\
    accuracy_with_refusal
import os

input_address = os.path.join(os.path.join(os.pardir, os.pardir), "input")
labels_filename = os.path.join(input_address, "training_set_results.txt")
sample_adress = os.path.join(input_address, "PTC_sample_4x4x4")

true_labels, pred_labels = test_lazy_classification(
        input_address=input_address,
        pos_dir=os.path.join(sample_adress,"MR_positive"),
        neg_dir=os.path.join(sample_adress,"MR_negative"),
        test_dir=os.path.join(sample_adress,"MR_test"),
        labels_filename=labels_filename,
        grouptype="MR",
        weighted=True,
        verbose=True)

print "Expected", true_labels
print "Predicted", pred_labels
print accuracy_with_refusal(true_labels, pred_labels, verbose=False)