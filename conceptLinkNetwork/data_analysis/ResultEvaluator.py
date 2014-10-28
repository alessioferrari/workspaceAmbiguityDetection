'''
Created on Sep 25, 2014

@author: alessioferrari
'''
from decimal import Decimal
import numpy
import os

POSITIVE = '1' #identifier for positive cases
NEGATIVE = '0' #identifier for negative cases

class ResultEvaluator(object):
    '''
    This class evaluates the results of an analysis of a set of requirements.
    It compares a manually tagged set of requirements with an automatically 
    tagged set of requirements 
    '''

    def __init__(self, result_folder_path, file_name_manual, file_name_auto):
        '''
        Constructor
        '''
        self.file_manual = result_folder_path + os.sep + file_name_manual
        self.file_auto = result_folder_path + os.sep + file_name_auto
        self.id_dict_file_manual = dict()
        self.id_dict_file_auto = dict()
        
    def __read_file(self, file_to_read):
        fp=open(file_to_read,"r")
        lines = fp.readlines()
        fp.close()
        return lines
    
    def __load_results(self, lines, dictionary):
        for line in lines:
            res = line.strip().split(',')
            dictionary[res[0]] = res[1].strip()
    
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
    
    def compare_results(self):
        lines_manual = self.__read_file(self.file_manual)
        lines_auto = self.__read_file(self.file_auto)
        self.__load_results(lines_manual, self.id_dict_file_manual)
        self.__load_results(lines_auto, self.id_dict_file_auto)
        
        
        false_pos, false_neg, true_pos, true_neg = self.__compute_fp_fn_tp_tn(self.id_dict_file_auto,self.id_dict_file_manual)       
        p, r, f1 = self.__compute_prec_recall_f1(false_pos, false_neg, true_pos, true_neg)
        return p, r, f1        

NUM_EXP = 1                
                
for i in range(NUM_EXP):
    
    print "\n\n", "EXPERIMENT", i, "\n\n"
    
    for threshold in numpy.arange(0, 1, 0.01):    
        file_name= "file_automatic" + str(threshold) + ".txt"    
        e = ResultEvaluator(str('./combination' + str(i)), '../file_manual.txt', file_name)    
        print "threshold: ", threshold, " (p, r, f1) ", e.compare_results()

#fp=open('tmp.txt',"w")
#for i in range(114):
#    fp.write(str(str(i+1) + ', 0\n'))
#fp.close()
