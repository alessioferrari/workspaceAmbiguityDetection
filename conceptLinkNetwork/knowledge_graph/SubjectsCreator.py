'''
Created on Oct 29, 2014

@author: alessioferrari
'''

from knowledge_graph.SentenceNet import SentenceNet
from knowledge_graph.Subject import Subject
from numpy.random import choice
from os import listdir
from os.path import isfile, join
import irutils
import logging
import os

LOG_FILENAME = __file__ + '.log'

class SubjectsCreator(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.subject_dict = dict()
        
    def __assign_doc(self, n, depth, doc_path):
            
            file_name = os.path.basename(doc_path)
            
            prob_common =(float(1)/float(depth+1))
            common = choice([0,1], p=[float(1.0)-float(prob_common),float(prob_common)])
            
            if common:
                for subject in self.subject_dict.keys():                    
                    self.subject_dict[subject].add_file(file_name, doc_path)
            else:
                weights = [1.0/float(n) for i in range(n)]  
                chosen_subject = choice(self.subject_dict.keys(), p=weights)
                self.subject_dict[chosen_subject].add_file(file_name, doc_path)
    
    def __assign_docs_in_subfolders(self, n, root_folder, depth):
        fp = [ join(root_folder,f) for f in listdir(root_folder) if isfile(join(root_folder,f)) and f.lower().endswith(".txt")]
        for f in fp:
            self.__assign_doc(n,depth,f)
        
        subfolders = [ join(root_folder,f) for f in listdir(root_folder) if os.path.isdir(join(root_folder,f)) ]
        if len(subfolders) > 0:    
            for subfolder_name in subfolders:
                self.__assign_docs_in_subfolders(n,subfolder_name,depth+1) 
        
    def create_subjects(self, n, root_folder):
        '''
        This function creates @param n subjects, by taking documents from a folder
        and distributing the documents in all the folders with a probability that decreases with
        the depth of the folder.
        '''  
        
        for i in range(n):
            s = Subject()
            self.subject_dict['subj-' + str(i)] = s
        
        self.__assign_docs_in_subfolders(n,root_folder,0) 
        
        for k in self.subject_dict.keys():
            self.subject_dict[k].build_knowledge_graph()    
            
        
        return self.subject_dict