'''
Created on Oct 30, 2014

@author: alessioferrari
'''
from data_analysis.constants import AMBIGUOUS, NOT_AMBIGUOUS, POSITIVE, NEGATIVE
from utils import utils
from utils.utils import FLOAT, INT
import collections
import numpy

class ResultsEvaluator(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def __compute_prec_recall_f1(self, fp, fn, tp, tn):
        try:
            p = float(tp)/(float(tp) + float(fp))
        except ZeroDivisionError:
            p = float(0)
        try:
            r = float(tp)/(float(tp) + float(fn))    
        except ZeroDivisionError:
            r = float(0)
        try:
            f1 = float(2 * p * r)/float(p + r)
        except ZeroDivisionError:
            f1 = float(0)
        
        return p, r, f1 
        
    def __compute_fp_fn_tp_tn(self,dict_auto,dict_manual):
        
        false_pos = 0 
        false_neg = 0
        true_pos = 0
        true_neg = 0
        
        for key in dict_auto.keys():
            auto = dict_auto[key]
            manual = dict_manual[key]
            if auto == POSITIVE and manual == POSITIVE:
                true_pos = true_pos + 1
            elif auto == POSITIVE and manual == NEGATIVE:
                false_pos = false_pos + 1
            elif auto == NEGATIVE and manual == NEGATIVE:
                true_neg = true_neg + 1
            else:
                false_neg = false_neg + 1
           
        return false_pos, false_neg, true_pos, true_neg
    
    
    def read_distances(self, dist_file_path):
        return utils.read_dict_from_csv(dist_file_path, data_type = FLOAT)
    
    def read_manual_ambiguity_file(self, manual_file_path):
        return utils.read_dict_from_csv(manual_file_path, data_type=INT)
    
    def compute_ambiguity_result(self, dict_distances, threshold):
        dict_ambiguity_result = dict()
        for k in dict_distances.keys():
            if dict_distances[k] > float(threshold):
                dict_ambiguity_result[k] = NOT_AMBIGUOUS
            else:
                dict_ambiguity_result[k] = AMBIGUOUS
        return dict_ambiguity_result
    
    def iterate_ambiguity_computation_over_threshold(self, dict_distances, range_start, range_end, step):
        dict_ambiguity_results = dict()
        
        for threshold in numpy.arange(range_start, range_end, step):
            dict_ambiguity_results[str(threshold)] = self.compute_ambiguity_result(dict_distances, threshold)
              
        return dict_ambiguity_results
    
    def evaluate_p_r_f1(self, dict_ambiguity_result_auto, dict_ambiguity_result_manual):
        false_pos, false_neg, true_pos, true_neg = self.__compute_fp_fn_tp_tn(dict_ambiguity_result_auto,dict_ambiguity_result_manual)       
        p, r, f1 = self.__compute_prec_recall_f1(false_pos, false_neg, true_pos, true_neg)
        return [p, r, f1]
    
    def iterate_evaluation_over_dictionary(self, dict_ambiguity_results_auto, dict_ambiguity_result_manual):
        '''
        @return a dictionary where each entry is associated to a threshold, and the content include three values in an array, 
        namely precision recall and f1
        '''        
        dict_evaluation = dict()
        for k in dict_ambiguity_results_auto.keys():
            dict_evaluation[k] = self.evaluate_p_r_f1(dict_ambiguity_results_auto[k], dict_ambiguity_result_manual)
        return dict_evaluation
    
    def perform_evaluation(self, dict_distances, dict_ambiguity_result_manual, range_start, range_end, step):
        '''
        Calls the other functions in this class to evaluate p, r, f1 for different thresholds
        @return: a dictionary where each key is a threshold value in string format and each entry is a list of p,r,f1
        '''
        if len(dict_distances.keys()) == len(dict_ambiguity_result_manual.keys()):
            dict_ambiguity_results_auto = self.iterate_ambiguity_computation_over_threshold(dict_distances, range_start, range_end, step)
            dict_evaluation = self.iterate_evaluation_over_dictionary(dict_ambiguity_results_auto, dict_ambiguity_result_manual) 
            return dict_evaluation
        else:
            print "Dictionaries must have the same size"
            return -1
            
    def store_evaluation(self, dict_evaluation, file_path):
        ordered_dict_evaluation = collections.OrderedDict(sorted(dict_evaluation.items()))
        utils.store_dict_in_csv(ordered_dict_evaluation, file_path)
        

#r = ResultsEvaluator()
#dist = r.read_distances('../distances.csv')
#manual_dict = r.read_manual_ambiguity_file('../manual.csv')
#d = r.perform_evaluation(dist, manual_dict, 0, 1, 0.01)  
#if not (d == -1):
#    r.store_evaluation(d,'../result.csv')  