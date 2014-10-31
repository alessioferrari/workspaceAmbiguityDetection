'''
Created on Oct 30, 2014

@author: alessioferrari
'''
from InterpretationManager import InterpretationManager
from data_analysis.ResultsEvaluator import ResultsEvaluator
from distances.constants import DIST_TYPE_JACCARD
from doc_retrieval.DocumentCrawler import DocumentCrawler
from knowledge_graph.constants import INT_MIN_PATH_SUBGRAPH, INT_SUBGRAPH
from os import listdir
from os.path import isfile, join, basename, isdir
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
KNOWLEDGE_BASE_PATH = PROJECT_PATH + os.sep + 'knowledge_base'
REQUIREMENTS_FILE_PATH = PROJECT_PATH + os.sep + "AllRequirements.txt"        
DISTANCES_FILE_PATH = PROJECT_PATH + os.sep + 'distances'
MANUAL_AMBIGUITY_FILE = PROJECT_PATH + os.sep + 'manual.csv'        
EVALUATION_RESULT_PATH = PROJECT_PATH + os.sep + 'evaluation'  
LOG_FILE_PATH = PROJECT_PATH + os.sep + __name__ + '.log'

experiment_log = utils.start_logger(__name__, LOG_FILE_PATH)
      
        
#=======================================================================
# DocumentCrawler parameters 
#=======================================================================
p_crawl_config_dict = {'0':['Outbreak','System'],'1':['Health','System']}
p_t_depth = 2
p_t_links = 3

#===============================================================================
# InterpretationManager parameters
#===============================================================================
p_n_subjects = 2
p_int_type = [INT_SUBGRAPH, INT_MIN_PATH_SUBGRAPH]
p_dist_type = [DIST_TYPE_JACCARD]

#===============================================================================
# ResultsEvaluator parameters
#===============================================================================

p_step = 0.1

#===============================================================================
# Flags to activate components
#===============================================================================
p_do_crawl = 0
p_do_compute_dist = 1
p_do_evaluate_results = 1

utils.create_folder(PROJECT_PATH)
utils.create_folder(KNOWLEDGE_BASE_PATH)
utils.create_folder(DISTANCES_FILE_PATH)
utils.create_folder(EVALUATION_RESULT_PATH)

if p_do_crawl == 1:
    experiment_log.info("START Document crawl")
    for experiment in p_crawl_config_dict.keys():
        experiment_path = KNOWLEDGE_BASE_PATH + os.sep + str(experiment)
        d = DocumentCrawler(experiment_path)
        for k in p_crawl_config_dict[experiment]:    
            d.search_and_store(k, t_depth = p_t_depth, t_links = p_t_links, depth = 0, root_path = experiment_path, create_subfolders="Y")
    experiment_log.info("END Document crawl")

if p_do_compute_dist == 1:
    knowledge_dirs = [join(KNOWLEDGE_BASE_PATH,f) for f in listdir(KNOWLEDGE_BASE_PATH) if isdir(join(KNOWLEDGE_BASE_PATH,f))]
    for knowledge_dir in knowledge_dirs:   
        experiment_log.info("START Subject creation")
        i = InterpretationManager()
        i.create_subjects(p_n_subjects, knowledge_dir)
        experiment_log.info("END Subject creation")
        for interpretation_type in p_int_type:
            experiment_log.info("START Interpretation " + interpretation_type)
            interpretations = i.perform_interpretations(REQUIREMENTS_FILE_PATH, interpretation_type, flg_reduce_list=1, max_requirements=2)
            experiment_log.info("END Interpretation " + interpretation_type)
            for distance_type in p_dist_type:
                experiment_log.info("START Evaluating Distances " + distance_type)
                distances = i.compare_interpretations(distance_type, interpretations)
                i.store_distances(distances, DISTANCES_FILE_PATH + os.sep + basename(knowledge_dir) +'_' + interpretation_type + '_' + distance_type + '.csv')
                experiment_log.info("END Evaluating Distances " + distance_type)

if p_do_evaluate_results == 1:
    experiment_log.info("START Evaluating Results ")
    r = ResultsEvaluator()
    manual_dict = r.read_manual_ambiguity_file(MANUAL_AMBIGUITY_FILE)
    
    dist_files = [join(DISTANCES_FILE_PATH,f) for f in listdir(DISTANCES_FILE_PATH) if isfile(join(DISTANCES_FILE_PATH,f)) and f.endswith('.csv')]
    for f in dist_files:
        dist = r.read_distances(f)
        d = r.perform_evaluation(dist, manual_dict, 0, 1, p_step)  
        if not (d == -1):
            r.store_evaluation(d, EVALUATION_RESULT_PATH + os.sep + 'res_' + basename(f))  
    experiment_log.info("END Evaluating Results ")

print 'done'
