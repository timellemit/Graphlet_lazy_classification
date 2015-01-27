from test_lazy_classify import test_lazy_classification,\
    accuracy_with_refusal

MM_expected, MM_predicted = test_lazy_classification(
        input_address="C:\\Users\\User\\Documents\\eclipse_workspace\\graphlet_lazy\\input\\",
        pos_dir="PTC_sample_44x44x44\\MM_positive",
        neg_dir="PTC_sample_44x44x44\\MM_negative",
        test_dir="PTC_sample_44x44x44\\MM_test",
        labels_filename="training_set_results.txt",
        verbose=False)

print "MM expected", MM_expected
print "MM predicted", MM_predicted
print accuracy_with_refusal(MM_expected, MM_predicted, 
                            verbose=False)

MR_expected, MR_predicted = test_lazy_classification(
        input_address="C:\\Users\\User\\Documents\\eclipse_workspace\\graphlet_lazy\\input\\",
        pos_dir="PTC_sample_44x44x44\\MR_positive",
        neg_dir="PTC_sample_44x44x44\\MR_negative",
        test_dir="PTC_sample_44x44x44\\MR_test",
        labels_filename="training_set_results.txt",
        verbose=False)

print "MR expected", MR_expected
print "MR predicted", MR_predicted
print accuracy_with_refusal(MR_expected, MR_predicted, 
                            verbose=False)

FM_expected, FM_predicted = test_lazy_classification(
        input_address="C:\\Users\\User\\Documents\\eclipse_workspace\\graphlet_lazy\\input\\",
        pos_dir="PTC_sample_44x44x44\\FM_positive",
        neg_dir="PTC_sample_44x44x44\\FM_negative",
        test_dir="PTC_sample_44x44x44\\FM_test",
        labels_filename="training_set_results.txt",
        verbose=False)

print "FM expected", FM_expected
print "FM predicted", FM_predicted
print accuracy_with_refusal(FM_expected, FM_predicted, 
                            verbose=False)

FR_expected, FR_predicted = test_lazy_classification(
        input_address="C:\\Users\\User\\Documents\\eclipse_workspace\\graphlet_lazy\\input\\",
        pos_dir="PTC_sample_44x44x44\\FR_positive",
        neg_dir="PTC_sample_44x44x44\\FR_negative",
        test_dir="PTC_sample_44x44x44\\FR_test",
        labels_filename="training_set_results.txt",
        verbose=False)

print "FR expected", FR_expected
print "FR predicted", FR_predicted
print accuracy_with_refusal(FR_expected, FR_predicted, 
                            verbose=False)