'''
Created on Oct 29, 2014

@author: alessioferrari
'''

 
from knowledge_graph.SentenceNet import SentenceNet
from knowledge_graph.Subject import Subject
from knowledge_graph.SubjectsCreator import SubjectsCreator
from numpy.random import choice
from os import listdir
from os.path import isfile, join
import irutils
import logging
import os


LOG_FILENAME = __file__ + '.log'
PATH_FILE_REQ = "none"

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
            
    def perform_interpretation(self, requirements_file_path, type):    
        '''
        This function takes the file in @param requirements_file_path,
        which includes one requirement for each line. Interpreation
        is performed by each knowledge graph, according to the selected @param type.
        Interpretations for each requirement and each type are stored in an Interpretation object.
        '''
        req_file=open(PATH_FILE_REQ,"r")
        reqs = req_file.readlines()
        
                
i = InterpretationManager()
subjects = i.create_subjects(3,'knowledge_base')
