'''
Created on Oct 29, 2014

@author: alessioferrari
'''

 
from knowledge_graph.SentenceNet import SentenceNet
from knowledge_graph.Subject import Subject
from knowledge_graph.SubjectsCreator import SubjectsCreator
from knowledge_graph.constants import DIST_MIN_PATH_SUBGRAPH
from numpy.random import choice
from os import listdir
from os.path import isfile, join
import datetime
import irutils
import logging
import os


LOG_FILENAME = __file__ + '.log'

class InterpretationManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.subj_creator = SubjectsCreator()
        
        self.logger = logging.getLogger(__file__) 
        hdlr = logging.FileHandler(LOG_FILENAME, mode="w")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.INFO)
    
    def create_subjects(self, n, root_folder):
        return self.subj_creator.create_subjects(n, root_folder)
            
    def perform_interpretations(self, requirements_file_path, type):    
        '''
        This function takes the file in @param requirements_file_path,
        which includes one requirement for each line. Interpreation
        is performed by each knowledge graph, according to the selected @param type.
        Interpretations for each requirement and each type are stored in an Interpretation object.
        '''
        req_file=open(requirements_file_path,"r")
        reqs = req_file.readlines()
        req_file.close()
        
        print "START interpretation", datetime.datetime.now().time()
        
        interpretations_dictionary = dict()
        
        for index, req in enumerate(reqs[0:2]):
            interpretation_list = list()
            for sub in self.subj_creator.subject_dict.keys():
                interpretation = self.subj_creator.subject_dict[sub].perform_interpretation(req, type)
                interpretation_list.append(interpretation)
            interpretations_dictionary[index] = interpretation_list
        
        
        print "\nFINISH", datetime.datetime.now().time()
        
        return interpretations_dictionary
                
i = InterpretationManager()
i.create_subjects(2,'knowledge_base')
i.perform_interpretations("AllRequirements.txt",DIST_MIN_PATH_SUBGRAPH)
