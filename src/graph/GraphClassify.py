from GraphContext import GraphContext
from time import time
# from sklearn import metrics
from GraphDescriptionElement import graphlet_descs
from graph.GraphDescription import graphlet_descriptions
from parse_PTC_2001_data.parse_PTC_train_labels import select_labels
import os
import numpy as np

class GraphClassify:  
    
    def __init__(self, pos_cxt_file, neg_cxt_file, build_graphlets=False, 
                 min_nodes=3, max_nodes=3, ptc=False):
        self.positive_cxt = GraphContext(pos_cxt_file, 
                build_graphlets=build_graphlets, 
                min_nodes=min_nodes, max_nodes=max_nodes, ptc=ptc)
        self.negative_cxt = GraphContext(neg_cxt_file, 
                build_graphlets=build_graphlets, 
                min_nodes=min_nodes, max_nodes=max_nodes, ptc=ptc)
        self.context = GraphContext
        self.build_graphlets, self.min_nodes, self.max_nodes, self.ptc = \
        build_graphlets, min_nodes, max_nodes, ptc
    
    def graphlet_train_test(self, test_dir, labels_filename,
                            grouptype):
        self.test_cxt = self.context(test_dir, self.build_graphlets, 
                                     self.min_nodes, self.max_nodes, self.ptc)
        train_set = graphlet_descriptions(desc_set=self.positive_cxt.table + 
                                          self.negative_cxt.table,
                                          training_set=self.positive_cxt.table + 
                                          self.negative_cxt.table, 
                                          min_nodes=self.min_nodes, 
                                          max_nodes=self.max_nodes)[1]
        test_set = graphlet_descriptions(self.test_cxt.table, 
                                         training_set=self.positive_cxt.table + 
                                          self.negative_cxt.table,
                                          min_nodes=self.min_nodes, 
                                          max_nodes=self.max_nodes)[1]
        train_labels = np.array([1]*len(self.positive_cxt.table) +
                                [0]*len(self.positive_cxt.table)) 
        test_labels = select_labels(test_dir, labels_filename, grouptype)
        return train_set, test_set, train_labels, test_labels
        
    def lazy_classify(self, test_cxt_file, use_graphlets=True,
                      min_nodes=1, max_nodes=100000, 
                      weighted=False,
                      verbose=False,
                      ptc=False):
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
