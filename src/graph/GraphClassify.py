# -*- coding: utf-8 -*-
from GraphContext import GraphContext
from time import time
from parse_PTC_2001_data.parse_PTC_train_labels import select_labels
import numpy as np
from parse_PTC_2001_data.parse_binary_graphlet_descriptions import parse_graphlet_descriptions
from sklearn import svm, metrics, neighbors

class GraphClassify:  
    
    def __init__(self, pos_cxt_file, neg_cxt_file, build_graphlets=True, 
                 min_nodes=3, max_nodes=3, ptc=False, verbose=False):
        self.positive_cxt = GraphContext(pos_cxt_file, 
                build_graphlets=build_graphlets, 
                min_nodes=min_nodes, max_nodes=max_nodes, ptc=ptc,
                verbose=verbose)
        self.negative_cxt = GraphContext(neg_cxt_file, 
                build_graphlets=build_graphlets, 
                min_nodes=min_nodes, max_nodes=max_nodes, ptc=ptc,
                verbose=verbose)
        self.context = GraphContext
        self.build_graphlets, self.min_nodes, self.max_nodes, self.ptc = \
        build_graphlets, min_nodes, max_nodes, ptc
    
    def all_train_graphlets(self, min_nodes=3, max_nodes=3, verbose=False):
        init_time = time()
        graphlets = []
        for desc in self.positive_cxt.table + self.negative_cxt.table:
            for elem in desc.value:
                for n_nodes in xrange(max_nodes, min_nodes - 1, -1):
                    for graphlet in elem.graphlet_iter(n_nodes):
                        if graphlet.unique_graphlet(graphlets):
                            graphlets.append(graphlet)
        if verbose:
            print "All graphlets time: ", round(time() - init_time, 2)
        return graphlets
    
    def graphlet_train_test(self, test_dir, labels_filename,
                            grouptype, 
                            fromfile=True,
                            tofile=False, train_filename=None,
                            test_filename=None,
                            train_labels_filename=None,
                            test_labels_filename=None,
                            verbose=False):
        init_time = time()
        self.test_cxt = self.context(data_file_address=test_dir,
                                      build_graphlets=self.build_graphlets,
                                     min_nodes=self.min_nodes, 
                                     max_nodes=self.max_nodes, ptc=self.ptc,
                                     verbose=verbose)
        if fromfile:
            train_set, test_set, train_labels, test_labels = \
            parse_graphlet_descriptions(
                                train_filename, 
                                test_filename,
                                train_labels_filename,
                                test_labels_filename)
        else:
            graphlets =  []
            train_length = len(self.positive_cxt.table + 
                             self.negative_cxt.table)
            train_test_length = train_length + len(self.test_cxt.table)
#             for desc in self.positive_cxt.table + \
#                              self.negative_cxt.table + self.test_cxt.table:
#                 for elem in desc.value:
#                     all_graph_elems.append(elem)
            all_graph_elems = [elem for desc in self.positive_cxt.table + 
                             self.negative_cxt.table + self.test_cxt.table
                            for elem in desc.value]
#             print "all_graph_elems ", len(all_graph_elems)
#             all_graph_elems = self.positive_cxt.table + \
#                              self.negative_cxt.table + self.test_cxt.table
            binary_descriptions = []#np.array([])
            for train_desc in self.positive_cxt.table + self.negative_cxt.table:
                for elem in train_desc.value:
                    for n_nodes in xrange(self.max_nodes, self.min_nodes - 1, -1):
                        for graphlet in elem.graphlet_iter(n_nodes):
                            if graphlet.unique_graphlet(graphlets):
                                graphlets.append(graphlet)
                                for test_elem in all_graph_elems:
                                    value = int(graphlet.is_subgraph(test_elem,
                                            use_graphlets=True))
                                    binary_descriptions.append(value)
            binary_descriptions = np.array(binary_descriptions).reshape([len(graphlets),
                                                                train_test_length]).T   
            print "binary_descriptions ", binary_descriptions.shape
            train_set, test_set = binary_descriptions[:train_length,:], \
                                  binary_descriptions[train_length:,:]
            train_labels = np.array([1]*len(self.positive_cxt.table) +
                                    [0]*len(self.negative_cxt.table)) 
            test_labels = select_labels(test_dir, labels_filename, grouptype)
#             print "train_set ", train_set.shape
            if tofile:
                np.savetxt(train_filename,train_set,fmt='%d',delimiter=',')
                np.savetxt(test_filename,test_set,fmt='%d',delimiter=',') 
                np.savetxt(train_labels_filename,train_labels,fmt='%d',delimiter=',') 
                np.savetxt(test_labels_filename,test_labels,fmt='%d',delimiter=',') 
            if verbose:
                print graphlets
                print "Graphlet description time in sec: ", round(time() - init_time, 2) 
        return train_set, test_set, train_labels, test_labels
    
    def svm_graphlet_classify(self, test_dir, labels_filename,
                              grouptype="MR",
                              descs_from_file=True,
                              train_filename=None,
                              test_filename=None,
                              train_labels_filename=None,
                              test_labels_filename=None,
                              descs_to_file=False,
                              verbose=True,
                              output_time=True):
        init_time = time()
        # Создание бинарных описаний обучающей и тестовой выборки, 
        # а также парсинг меток тестовой выборки
        # Параметр grouptype - половидовой признак (муж/жен, крысы/мыши)
        train_set, test_set, train_labels, test_labels = \
        self.graphlet_train_test(test_dir, 
                              labels_filename,
                              fromfile=descs_from_file,
                              tofile=descs_to_file,
                              grouptype=grouptype,
                              train_filename=train_filename,
                              test_filename=test_filename,
                              train_labels_filename=train_labels_filename,
                              test_labels_filename=test_labels_filename,
                              verbose=verbose)   
        print "train_set ", train_set.shape
#         print "Train set descs\n", train_set
#         print "Test set descs\n", test_set
        clf = svm.SVC(kernel='linear')
        clf.fit(train_set, train_labels)
        predicted =  clf.predict(test_set)
        if verbose:
            print "True: ", test_labels
            print "Predicted: ", predicted
            print(metrics.classification_report(test_labels, predicted))
            print(metrics.confusion_matrix(test_labels, predicted)) 
            print "svm_graphlet_classify, time in sec: ", round(time() - init_time, 2)
        if output_time:
            return predicted, round(time() - init_time, 2)
        else:
            return predicted
    
    def scikit_graphlet_classify(self, clf,
                                 test_dir, labels_filename,
                                 grouptype="MR",
                                 descs_from_file=True,
                                 train_filename=None,
                                 test_filename=None,
                                 train_labels_filename=None,
                                 test_labels_filename=None,
                                 descs_to_file=False,
                                 verbose=True,
                                 output_time=True):
        init_time = time()
        # Создание бинарных описаний обучающей и тестовой выборки, 
        # а также парсинг меток тестовой выборки
        # Параметр grouptype - половидовой признак (муж/жен, крысы/мыши)
        train_set, test_set, train_labels, test_labels = \
        self.graphlet_train_test(test_dir, 
                              labels_filename,
                              fromfile=descs_from_file,
                              tofile=descs_to_file,
                              grouptype=grouptype,
                              train_filename=train_filename,
                              test_filename=test_filename,
                              train_labels_filename=train_labels_filename,
                              test_labels_filename=test_labels_filename,
                              verbose=verbose)   
        print "train_set ", train_set.shape
#         print "Train set descs\n", train_set
#         print "Test set descs\n", test_set
        clf = clf;
        clf.fit(train_set, train_labels)
        predicted =  clf.predict(test_set)
        if verbose:
            print "True: ", test_labels
            print "Predicted: ", predicted
            print(metrics.classification_report(test_labels, predicted))
            print(metrics.confusion_matrix(test_labels, predicted)) 
            print "scikit_graphlet_classify, time in sec: ", round(time() - init_time, 2)
        if output_time:
            return predicted, round(time() - init_time, 2)
        else:
            return predicted
        
    def knn_graphlet_classify(self, test_dir, labels_filename,
                              grouptype="MR",
                              descs_from_file=True,
                              train_filename=None,
                              test_filename=None,
                              train_labels_filename=None,
                              test_labels_filename=None,
                              descs_to_file=False,
                              verbose=True,
                              output_time=True):
        init_time = time()
        # Создание бинарных описаний обучающей и тестовой выборки, 
        # а также парсинг меток тестовой выборки
        # Параметр grouptype - половидовой признак (муж/жен, крысы/мыши)
        train_set, test_set, train_labels, test_labels = \
        self.graphlet_train_test(test_dir, 
                              labels_filename,
                              fromfile=descs_from_file,
                              tofile=descs_to_file,
                              grouptype=grouptype,
                              train_filename=train_filename,
                              test_filename=test_filename,
                              train_labels_filename=train_labels_filename,
                              test_labels_filename=test_labels_filename,
                              verbose=verbose)   
        print "train_set ", train_set.shape
#         print "Train set descs\n", train_set
#         print "Test set descs\n", test_set
        clf = neighbors.KNeighborsClassifier(4)
        clf.fit(train_set, train_labels)
        predicted =  clf.predict(test_set)
        if verbose:
            print "True: ", test_labels
            print "Predicted: ", predicted
            print(metrics.classification_report(test_labels, predicted))
            print(metrics.confusion_matrix(test_labels, predicted)) 
            print "knn_graphlet_classify, time in sec: ", round(time() - init_time, 2)
        if output_time:
            return predicted, round(time() - init_time, 2)
        else:
            return predicted
        
    def lazy_graphlet_classify(self, test_dir, labels_filename,
                              grouptype="MR",
                              descs_from_file=True,
                              train_filename=None,
                              test_filename=None,
                              train_labels_filename=None,
                              test_labels_filename=None,
                              descs_to_file=False,
                              verbose=True,
                              output_time=True):

        init_time = time()
        # Создание бинарных описаний обучающей и тестовой выборки, 
        # а также парсинг меток тестовой выборки
        # Параметр grouptype - половидовой признак (муж/жен, крысы/мыши)
        train_set, test_set, _, test_labels = \
        self.graphlet_train_test(test_dir, 
                              labels_filename,
                              fromfile=descs_from_file,
                              tofile=descs_to_file,
                              grouptype=grouptype,
                              train_filename=train_filename,
                              test_filename=test_filename,
                              train_labels_filename=train_labels_filename,
                              test_labels_filename=test_labels_filename,
                              verbose=verbose)  
         
        pos_set, neg_set = train_set[:len(self.positive_cxt.table),:],\
        train_set[len(self.positive_cxt.table):,:]
        
        def binary_intersect(binary_desc1, binary_desc2):
            res = []
            for i in xrange(len(binary_desc1)):
                if binary_desc1[i] == binary_desc2[i]:
                    res.append(binary_desc1[i])
                else:
                    res.append(-1) 
            return np.array(res)
        
        def inter_matches(inter, binary_desc):
            for i in xrange(len(binary_desc)):
                if inter[i] != 1 and inter[i] != binary_desc[i]:
                    return False
            return True
        
        predicted = []    
        for test_obj in test_set:
            pos_votes, neg_votes = 0,0
            for pos_obj in pos_set:
                inter = binary_intersect(test_obj,pos_obj)
                for neg_obj in neg_set:
                    if not inter_matches(inter, neg_obj):
                        pos_votes += sum(inter != -1)
#                         pos_votes += 1
            for neg_obj in neg_set:
                inter = binary_intersect(test_obj, neg_obj)
                for pos_obj in pos_set:
                    if not inter_matches(inter, pos_obj):
                        neg_votes += sum(inter != -1)
#                         neg_votes += 1
            if pos_votes == neg_votes:
                predicted.append(-1)
            else:
                predicted.append(int(pos_votes > neg_votes))
        if verbose:
            print "True: ", test_labels
            print "Predicted: ", predicted
            print(metrics.classification_report(test_labels, predicted))
            print(metrics.confusion_matrix(test_labels, predicted)) 
            print "lazy_graphlet_classify, time in sec: ", round(time() - init_time, 2)
        if output_time:
            return predicted, round(time() - init_time, 2)
        else:
            return predicted

    
    def lazy_classify(self, test_cxt_file, use_graphlets=True,
                      min_nodes=3, max_nodes=3, 
                      weighted=False,
                      verbose=False,
                      ptc=False,
                      output_time=False):

        def test_intersections(train_context, opposite_context,
                               test_object, use_graphlets,
                               min_nodes, max_nodes, 
                               weighted, verbose):
            vote_num = 0
            for train_object in train_context.table:
                intersection = train_object.intersect(test_object, use_graphlets,
                                                      min_nodes, max_nodes)
                if not self.intersection_covers_example_from_set(
                        intersection=intersection, 
                        object_set=opposite_context.table,
                        use_graphlets=use_graphlets,
                        min_nodes=min_nodes, max_nodes=max_nodes):
                    
                    vote_num += (len(intersection) if weighted else 1)
                    
                if verbose:
                    print "Intersection of " + test_object.__str__() + " and " + \
                    train_object.__str__() + " = " + intersection.__str__()
#                     for opposite_object in opposite_context.table:
#                         if intersection.is_sub_description(opposite_object, use_graphlets,
#                                                            min_nodes, max_nodes):
#                             print "Falsified by " + opposite_object.__str__()
#                             break
            return vote_num
        
        if use_graphlets and not self.build_graphlets:
            Warning("Graphlets were not built")
            use_graphlets = False
        init_time = time()
        labels = []
        self.test_cxt = self.context(test_cxt_file, self.build_graphlets, 
                                     min_nodes, max_nodes, ptc)
        for test_object in self.test_cxt.table:
            pos_votes = test_intersections(train_context=self.positive_cxt,
                                           opposite_context=self.negative_cxt, 
                                           test_object=test_object, 
                                           use_graphlets=use_graphlets,
                                           min_nodes=min_nodes,
                                           max_nodes=max_nodes, 
                                           weighted=weighted,
                                           verbose=verbose)
            neg_votes = test_intersections(train_context=self.negative_cxt, 
                                           opposite_context=self.positive_cxt, 
                                           use_graphlets=use_graphlets,
                                           test_object=test_object, 
                                           min_nodes=min_nodes,
                                           max_nodes=max_nodes, 
                                           weighted=weighted,
                                           verbose=verbose)
            if pos_votes == neg_votes:
                labels.append(-1)
            else:
                labels.append(int(pos_votes > neg_votes))
            if verbose:
                print "Score: ", pos_votes, ":", neg_votes
        if verbose:
            print "Classification time in sec: ", round(time() - init_time, 2)
            class_labels = {1: "positive", 0: "negative", -1: "undefined"}
            for i in xrange(len(self.test_cxt.obj_names)):
                print "Example " + self.test_cxt.obj_names[i] + \
                    " is classified as " + class_labels[labels[i]]
        if output_time:
            return labels, output_time
        else:
            return labels
    
    def intersection_covers_example_from_set(self, intersection, object_set,
                                             use_graphlets=False,
                                             min_nodes=1, max_nodes=100000):
        """
        Checks if an intersection covers at least one example from object_set.
        :type intersection: GraphDescription
        :param intersection: 
        :param object_set: a container 
        :rtype : bool
        """
        for example in object_set:
            if intersection.is_sub_description(other=example, 
                use_graphlets=use_graphlets,
                min_nodes=min_nodes, 
                max_nodes=max_nodes):
                return True
        return False
        
if __name__ == "__main__":
#     init_time = time()
#     molecules = GraphClassify("../../input/toy_molecules_positive.csv",
#                           "../../input/toy_molecules_negative.csv",
#                           build_graphlets=True, min_nodes=3, max_nodes=3) 
#     print molecules.lazy_classify("../../input/toy_molecules_test.csv",
#                          use_graphlets=True, 
#                          min_nodes=3, max_nodes=3, verbose=True)
    init_time = time()
    molecules = GraphClassify("../../input/PTC_toy_sample/positive/",
                          "../../input/PTC_toy_sample/negative/", 
                          build_graphlets=True, min_nodes=3, max_nodes=3, ptc=True) 
    predicted = molecules.lazy_classify("../../input/PTC_toy_sample/test/",
                        use_graphlets=True,
                         min_nodes=3, max_nodes=3, 
                         weighted = True,
                         ptc=True, verbose=True)
    expected = [0,1,0,1,0,1]
#     molecules = GraphClassify("../../input/PTC_medium_sample/positive/",
#                           "../../input/PTC_medium_sample/negative/", 
#                           build_graphlets=True, min_nodes=3, max_nodes=3, ptc=True) 
#     predicted = molecules.lazy_classify("../../input/PTC_medium_sample/test/",
#                         use_graphlets=True,
#                          min_nodes=3, max_nodes=3, ptc=True, verbose=True)
#     expected = [0,1,1,0,0,0,1,0,1,1,0,1,0,1,0,1]
#     molecules = GraphClassify("../../input/PTC_training_set/MR_positive/",
#                           "../../input/PTC_training_set/MR_negative/", 
#                           build_graphlets=True, min_nodes=3, max_nodes=3, ptc=True) 
#     print molecules.lazy_classify("../../input/PTC_training_set/MR_test/",
#                         use_graphlets=True,
#                          min_nodes=3, max_nodes=3, ptc=True, verbose=True)
    print "Classification time in sec: ", round(time() - init_time, 2) 
#     print(metrics.classification_report(expected, predicted))
#     print(metrics.confusion_matrix(expected, predicted))
    
#     print molecules.svm_graphlet_classify("../../input/PTC_toy_sample/test/",
#                                           min_nodes=3, max_nodes=3)
