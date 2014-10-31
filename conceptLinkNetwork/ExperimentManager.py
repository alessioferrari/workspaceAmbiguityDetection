'''
Created on Oct 30, 2014

@author: alessioferrari
'''
from InterpretationManager import InterpretationManager
from data_analysis.ResultsEvaluator import ResultsEvaluator
from distances.constants import DIST_TYPE_JACCARD
from doc_retrieval.DocumentCrawler import DocumentCrawler
from knowledge_graph.constants import INT_MIN_PATH_SUBGRAPH
from os import listdir
from os.path import isfile, join, basename
from utils import utils
import os

class ExperimentManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
PROJECT_PATH = './project'
KNOWLEDGE_BASE_PATH = os.path.abspath(PROJECT_PATH + os.sep + 'knowledge_base')
REQUIREMENTS_FILE_PATH = PROJECT_PATH + os.sep + "AllRequirements.txt"        
DISTANCES_FILE_PATH = PROJECT_PATH + os.sep + 'distances'
MANUAL_AMBIGUITY_FILE = PROJECT_PATH + os.sep + 'manual.csv'        
EVALUATION_RESULT_PATH = PROJECT_PATH + os.sep + 'evaluation'        
        
#=======================================================================
# DocumentCrawler parameters 
#=======================================================================
p_keywords = ['Outbreak','System']
p_t_depth = 2
p_t_links = 3

#===============================================================================
# InterpretationManager parameters
#===============================================================================
p_n_subjects = 2
p_int_type = INT_MIN_PATH_SUBGRAPH
p_dist_type = DIST_TYPE_JACCARD

#===============================================================================
# ResultsEvaluator parameters
#===============================================================================

p_step = 0.1

#===============================================================================
# Flags to activate components
#===============================================================================
p_do_crawl = 1
p_do_compute_dist = 1
p_do_evaluate_results = 1

utils.create_folder(PROJECT_PATH)
utils.create_folder(DISTANCES_FILE_PATH)
utils.create_folder(EVALUATION_RESULT_PATH)

if p_do_crawl == 1:
    d = DocumentCrawler(KNOWLEDGE_BASE_PATH)
    for k in p_keywords:    
        d.search_and_store(k, t_depth = p_t_depth, t_links = p_t_links, depth = 0, root_path = KNOWLEDGE_BASE_PATH, create_subfolders="Y")

if p_do_compute_dist == 1:
    i = InterpretationManager()
    i.create_subjects(p_n_subjects, KNOWLEDGE_BASE_PATH)
    interpretations = i.perform_interpretations(REQUIREMENTS_FILE_PATH, p_int_type, flg_reduce_list=1, max_requirements=2)
    distances = i.compare_interpretations(p_dist_type, interpretations)
    i.store_distances(distances, DISTANCES_FILE_PATH + os.sep + p_dist_type + '.csv')

if p_do_evaluate_results == 1:
    r = ResultsEvaluator()
    manual_dict = r.read_manual_ambiguity_file(MANUAL_AMBIGUITY_FILE)
    
    dist_files = [join(DISTANCES_FILE_PATH,f) for f in listdir(DISTANCES_FILE_PATH) if isfile(join(DISTANCES_FILE_PATH,f)) ]
    for f in dist_files:
        dist = r.read_distances(f)
        d = r.perform_evaluation(dist, manual_dict, 0, 1, p_step)  
        if not (d == -1):
            r.store_evaluation(d, EVALUATION_RESULT_PATH + os.sep + 'res_' + basename(f))  

print 'done'
