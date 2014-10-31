'''
Created on Oct 31, 2014

@author: alessioferrari
'''
from distances.constants import DIST_TYPE_JACCARD
from knowledge_graph.constants import INT_SUBGRAPH, INT_MIN_PATH_SUBGRAPH
from utils import utils

class ConfigurationManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def create_configuration(self):
        #=======================================================================
        # DocumentCrawler parameters 
        #=======================================================================
        configuration_dictionary = dict()
        configuration_dictionary['p_crawl_config_dict'] = {'0':['Outbreak','System'],'1':['Health','System']}
        configuration_dictionary['p_t_depth'] = 2
        configuration_dictionary['p_t_links'] = 3
        
        #===============================================================================
        # InterpretationManager parameters
        #===============================================================================
        
        #parameter to cut the nodes and the edges of the subjects
        configuration_dictionary['p_list_cut'] = [(0,float(1.0)),(3,float(0.5))]
        
        configuration_dictionary['p_n_subjects'] = 2
        configuration_dictionary['p_int_type'] = [INT_SUBGRAPH, INT_MIN_PATH_SUBGRAPH]
        configuration_dictionary['p_dist_type'] = [DIST_TYPE_JACCARD]
        
        #===============================================================================
        # ResultsEvaluator parameters
        #===============================================================================
        
        configuration_dictionary['p_step'] = 0.1
        utils.store_dict_in_csv(configuration_dictionary, 'configuration.csv') 
        
    def load_configuration(self):
        dict = utils.read_dict_from_csv('configuration.csv', 'misc')
        print dict
        
c = ConfigurationManager()
c.create_configuration()
c.load_configuration()          