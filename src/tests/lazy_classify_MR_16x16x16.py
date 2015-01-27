from test_lazy_classify import test_lazy_classification,\
    accuracy_with_refusal

exp, pred = test_lazy_classification(
        input_address="C:\\Users\\User\\Documents\\eclipse_workspace\\graphlet_lazy\\input\\",
        pos_dir="PTC_sample_16x16x16\\positive",
        neg_dir="PTC_sample_16x16x16\\negative",
        test_dir="PTC_sample_16x16x16\\test",
        labels_filename="training_set_results.txt",
        verbose=False)

print "Expected", exp
print "Predicted", pred
print accuracy_with_refusal(exp, pred, verbose=False)