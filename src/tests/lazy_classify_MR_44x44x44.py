from test_lazy_classify import test_lazy_classification,\
    accuracy_with_refusal

exp, pred = test_lazy_classification(
        input_address="C:\\Users\\User\\Documents\\eclipse_workspace\\graphlet_lazy\\input\\",
        pos_dir="PTC_sample_44x44x44\\MR_positive",
        neg_dir="PTC_sample_44x44x44\\MR_negative",
        test_dir="PTC_sample_44x44x44\\MR_test",
        labels_filename="training_set_results.txt")

accuracy_with_refusal(exp, pred)