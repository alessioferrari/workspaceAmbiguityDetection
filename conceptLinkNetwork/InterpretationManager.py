'''
Created on Oct 29, 2014

@author: alessioferrari
'''

 
from distances.DistanceEvaluation import DistanceEvaluation
from distances.constants import DIST_TYPE_JACCARD
from knowledge_graph.SentenceNet import SentenceNet
from knowledge_graph.Subject import Subject
from knowledge_graph.SubjectsCreator import SubjectsCreator
from knowledge_graph.constants import INT_MIN_PATH_SUBGRAPH, REQ_TERMS_REMOVE, \
    REQ_TERMS_NO_REMOVE
from numpy.random import choice
from os import listdir
from os.path import isfile, join
from utils import utils
import csv
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
        self.interpretation_dictionaries = dict()
        self.distance_dictionaries = dict()
        
        self.logger = logging.getLogger(__file__) 
        hdlr = logging.FileHandler(LOG_FILENAME, mode="w")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.INFO)
    
    def create_subjects(self, n, root_folder):
        return self.subj_creator.create_subjects(n, root_folder)
            
    def perform_interpretations(self, requirements_file_path, type, flg_reduce_list, max_requirements):    
        '''
        This function takes the file in @param requirements_file_path,
        which includes one requirement for each line. Interpreation
        is performed by each knowledge graph, according to the selected @param type.
        Interpretations for each requirement and each type are stored in an Interpretation object.
        '''
        req_file=open(requirements_file_path,"r")
        reqs = req_file.readlines()
        req_file.close()
        
        if flg_reduce_list == 1:
            req_list = reqs[0:max_requirements]
        else:
            req_list = reqs 
        
        interpretations_dictionary = dict()
        
        for index, req in enumerate(req_list):
            interpretation_list = list()
            for sub in self.subj_creator.subject_dict.keys():
                interpretation = self.subj_creator.subject_dict[sub].perform_interpretation(req, type, REQ_TERMS_REMOVE)
                interpretation_list.append(interpretation)
            interpretations_dictionary[index] = interpretation_list
        
        self.interpretation_dictionaries[type] = interpretations_dictionary
        
        return interpretations_dictionary
        
    
    def compare_interpretations(self, dist_type, interpretations_dictionary):
        """
        This function compares the interpretations in a dictionary for each entry in the dictionary.
        Each entry in @param interpretations_dictionary is associated to a requirement.
        The content of each entry is a list of digraphs that represent the interpretation
        of the same requirement. The function @return a dictionary of distances values,
        where the key of each entry is the key in the original dictionary and the 
        value is the value of the distance.
        """
        evaluator = DistanceEvaluation()
        distance_dictionary = dict()
        for item in interpretations_dictionary.keys():
            distance = evaluator.evaluate_distance(dist_type, interpretations_dictionary[item])
            distance_dictionary[item] = distance
        
        self.distance_dictionaries[dist_type] = distance_dictionary
        
        return distance_dictionary
    
    def store_distances(self, dictionary, file_path):
        utils.store_dict_in_csv(dictionary, file_path)
        
                  
#i = InterpretationManager()
#i.create_subjects(2,'knowledge_base')
#interpretations = i.perform_interpretations("AllRequirements.txt",INT_MIN_PATH_SUBGRAPH)
#distances = i.compare_interpretations(DIST_TYPE_JACCARD, interpretations)
#i.store_distances(distances,"distances.csv")

