'''
Created on Sep 30, 2014

@author: alessioferrari
'''
from constants import DIR_NAMES, DIST_TYPES
from constants import SUBJECT_1
import os



class ExperimentFolderManager(object):
    '''
    This class manages all the folders associated to an experiment
    for pragmatic ambiguity detection.
    '''


    def __init__(self, base_path):
        '''
        Constructor
        '''
        self.base_path = base_path
        self.base_dir_paths = list()
        
    ################----------PRIVATE METHODS--------------##############
    
    def __get_base_dir_path(self, keywords, t_depth, t_links):    
        return self.base_path + "-".join(keywords) + "-d" + str(t_depth) + "-l" + str(t_links)
    
    def __get_set_path(self, base_dir_path, set_id):
        return base_dir_path + os.sep + "set" + str(set_id)
    
    def __get_cute_cutn_res_path(self, set_path, cut_e, cut_n):
        return set_path + os.sep + DIR_NAMES[4] + os.sep + "cute-" + str(cut_e) + "cutn-" + str(cut_n)
    
    def __get_cute_cutn_eval_path(self, set_path, cut_e, cut_n):
        return set_path + os.sep + DIR_NAMES[2] + os.sep + "cute-" + str(cut_e) + "cutn-" + str(cut_n)
    
    def __get_nets_path(self, keywords, t_depth, t_links, set_id, cut_e, cut_n):
        base_dir_path = self.__get_base_dir_path(keywords, t_depth, t_links)
        set_path = self.__get_set_path(base_dir_path, set_id)
        return set_path + os.sep + DIR_NAMES[3] + os.sep + "cute-" + str(cut_e) + "cutn-" + str(cut_n)
    
    def __get_docs_path(self, keywords, t_depth, t_links, set_id):
        base_dir_path = self.__get_base_dir_path(keywords, t_depth, t_links)
        set_path = self.__get_set_path(base_dir_path, set_id)
        return set_path + os.sep + DIR_NAMES[1]
    
    def __get_distance_path(self, keywords, t_depth, t_links, set_id, cut_e, cut_n):
        base_dir_path = self.__get_base_dir_path(keywords, t_depth, t_links)
        set_path = self.__get_set_path(base_dir_path, set_id)
        return set_path + os.sep + DIR_NAMES[0] + os.sep + "cute-" + str(cut_e) + "cutn-" + str(cut_n)
    
    def __get_result_path(self, keywords, t_depth, t_links, set_id, cut_e, cut_n, dist_type):
        base_dir_path = self.__get_base_dir_path(keywords, t_depth, t_links)
        set_path = self.__get_set_path(base_dir_path, set_id)
        return set_path + os.sep + DIR_NAMES[4] + os.sep + "cute-" + str(cut_e) + "cutn-" + str(cut_n) + os.sep + dist_type
    
    def __get_eval_path(self, keywords, t_depth, t_links, set_id, cut_e, cut_n, dist_type):
        base_dir_path = self.__get_base_dir_path(keywords, t_depth, t_links)
        set_path = self.__get_set_path(base_dir_path, set_id)
        return set_path + os.sep + DIR_NAMES[2] + os.sep + "cute-" + str(cut_e) + "cutn-" + str(cut_n) + os.sep + dist_type
    
    
    def __create_folder(self, input_path):
        if not os.path.exists(input_path):
            os.makedirs(input_path)    
        
    def __create_set_folder_structure(self, set_path):
        for dir_name in DIR_NAMES:
            self.__create_folder(set_path + os.sep + dir_name)
        
        self.__create_folder(set_path + os.sep + DIR_NAMES[1] + os.sep + "subj1")
        self.__create_folder(set_path + os.sep + DIR_NAMES[1] + os.sep + "subj2")
    
    def __create_distance_folder_structure(self, cut_e_cut_n):
        for dist in DIST_TYPES:
            self.__create_folder(cut_e_cut_n + os.sep + dist)
        
        
    ################----------PUBLIC METHODS--------------##############    
        
    ################----------CREATORS--------------------##############

    def create_basic_folder(self, keywords, t_depth, t_links):
        '''
        @param keywords: list of keywords used for the document search
        @param t_depth: threshold depth for the documents to be searched
        @param t_link: threshold on the number of links to be considered  
        ''' 
        main_dir_path =  self.__get_base_dir_path(keywords, t_depth, t_links)
        self.__create_folder(main_dir_path)
        if main_dir_path not in self.base_dir_paths:
            self.base_dir_paths.append(main_dir_path)
            
    def create_set_folder(self, keywords, t_depth, t_links, set_id):
        '''
        @param keywords: list of keywords used for the document search
        @param t_depth: threshold depth for the documents to be searched
        @param t_link: threshold on the number of links to be considered 
        @param set_id: numeric identifier of the set 
        '''
        main_dir_path =  self.__get_base_dir_path(keywords, t_depth, t_links)
        if main_dir_path not in self.base_dir_paths:
            self.create_basic_folder(keywords, t_depth, t_links)
        
        set_path = self.__get_set_path(main_dir_path, set_id)
        self.__create_folder(set_path)
        self.__create_set_folder_structure(set_path)
        
    def create_cuts_folders(self, keywords, t_depth, t_links, set_id, cut_e, cut_n):
        base_dir_path = self.__get_base_dir_path(keywords, t_depth, t_links)
        set_path = self.__get_set_path(base_dir_path, set_id)
        self.__create_folder(set_path + os.sep + DIR_NAMES[0] + os.sep + "cute-" + str(cut_e) + "cutn-" + str(cut_n))
        self.__create_folder(set_path + os.sep + DIR_NAMES[2] + os.sep + "cute-" + str(cut_e) + "cutn-" + str(cut_n))
        self.__create_folder(set_path + os.sep + DIR_NAMES[3] + os.sep + "cute-" + str(cut_e) + "cutn-" + str(cut_n))
        self.__create_folder(set_path + os.sep + DIR_NAMES[4] + os.sep + "cute-" + str(cut_e) + "cutn-" + str(cut_n))
        
    
    def create_result_folders(self, keywords, t_depth, t_links, set_id, cut_e, cut_n):
        base_dir_path = self.__get_base_dir_path(keywords, t_depth, t_links)
        set_path = self.__get_set_path(base_dir_path, set_id)
        cut_e_cut_n_res = self.__get_cute_cutn_res_path(set_path, cut_e, cut_n)
        self.__create_distance_folder_structure(cut_e_cut_n_res)
        
    def create_eval_folders(self, keywords, t_depth, t_links, set_id, cut_e, cut_n):
        base_dir_path = self.__get_base_dir_path(keywords, t_depth, t_links)
        set_path = self.__get_set_path(base_dir_path, set_id)
        cut_e_cut_n_eval = self.__get_cute_cutn_eval_path(set_path, cut_e, cut_n)
        self.__create_distance_folder_structure(cut_e_cut_n_eval)
    
    def create_experiment_folder_structure(self, keywords, t_depth, t_links, sets_num, cut_e, cut_n):
        '''
        @param sets_num: number of sets
        '''
        self.create_basic_folder(keywords, t_depth, t_links)
        for i in range(sets_num):
            self.create_set_folder(keywords, t_depth, t_links, i)
            self.create_cuts_folders(keywords, t_depth, t_links, i, cut_e, cut_n)
            self.create_result_folders(keywords, t_depth, t_links, i, cut_e, cut_n)
            self.create_eval_folders(keywords, t_depth, t_links, i, cut_e, cut_n)
    
    ###################-------------STORE FILES---------###################
    
    def store_doc(self, keywords, t_depth, t_links, set_id, doc_name, doc, subject):
        docs_path = self.__get_docs_path(keywords, t_depth, t_links, set_id)
        if subject == SUBJECT_1:
            fp = open(docs_path + os.sep + "subj1" + os.sep + doc_name, "w")
        else:
            fp = open(docs_path + os.sep + "subj2" + os.sep + doc_name, "w")
        fp.write(doc)
        fp.close()   
    
    def store_nets(self, keywords, t_depth, t_links, set_id, cut_e, cut_n, g1, g2):
        nets_path = self.__get_nets_path(keywords, t_depth, t_links, set_id, cut_e, cut_n)
        
        file_name_g1 = "graphsubj1-set" + str(set_id) + "-cute-" + str(cut_e) + "-cutn-" + str(cut_n) + ".txt"
        fp = open(nets_path + os.sep + file_name_g1, "w")
        ##WRITE NETWORK HERE!
        fp.close() 
        
        file_name_g2 = "graphsubj2-set" + str(set_id) + "-cute-" + str(cut_e) + "-cutn-" + str(cut_n) + ".txt"
        fp = open(nets_path + os.sep + file_name_g2, "w")
        ##WRITE NETWORK HERE!
        fp.close() 
        
    def store_distance_file(self, keywords, t_depth, t_links, set_id, cut_e, cut_n, dist_type, content):
        distance_path = self.__get_distance_path(keywords, t_depth, t_links, set_id, cut_e, cut_n)
        file_name = str(dist_type) + "-set" + str(set_id) + "-cute-" + str(cut_e) + "-cutn-" + str(cut_n) + ".txt"
        fp = open(distance_path + os.sep + file_name, "w")
        fp.write(content)
        fp.close() 
        
    def store_result_file(self, keywords, t_depth, t_links, set_id, cut_e, cut_n, dist_type, threshold, content):
        result_path = self.__get_result_path(keywords, t_depth, t_links, set_id, cut_e, cut_n, dist_type)
        file_name = "res-t" + str(threshold) + "-" + str(dist_type) + "-set" + str(set_id) + "-cute-" + str(cut_e) + "-cutn-" + str(cut_n) + ".txt"
        fp =open(result_path + os.sep + file_name, "w")
        fp.write(content)
        fp.close()
        
    def store_evaluation_file(self, keywords, t_depth, t_links, set_id, cut_e, cut_n, dist_type, t_start, t_end, step, content):
        eval_path = self.__get_eval_path(keywords, t_depth, t_links, set_id, cut_e, cut_n, dist_type)
        file_name = "eval-r" + str(t_start) + "_" + str(t_end) + "s-" + str(step) + "-" + str(dist_type) + "-set" + str(set_id) + "-cute-" + str(cut_e) + "-cutn-" + str(cut_n) + ".txt"
        fp = open(eval_path + os.sep + file_name, "w")
        fp.write(content)
        fp.close()
 
 
    ###################-------------GETTERS-------------###################
    
    def get_basic_folder(self, keywords, t_depth, t_links):       
        return self.__get_base_dir_path(keywords, t_depth, t_links)
    
    def get_set_folder(self, keywords, t_depth, t_links, set_id):
        main_dir_path =  self.__get_base_dir_path(keywords, t_depth, t_links)        
        return self.__get_set_path(main_dir_path, set_id)
    
          
            
#e = ExperimentFolderManager("./")
#e.create_experiment_folder_structure(["Outbreak","System","Management"], 2, 10, 3, 0.5, 10)
#e.create_basic_folder(["Outbreak","System"], 2, 10)
#for i in range(2):
#    e.create_set_folder(["Outbreak","System"], 2, 10, i)
#    e.create_cuts_folders(["Outbreak","System"], 2, 10, i, 0.5, 10)
#    e.create_result_folders(["Outbreak","System"], 2, 10, i, 0.5, 10)
#    e.create_eval_folders(["Outbreak","System"], 2, 10, i, 0.5, 10)
    
#e.store_nets(["Outbreak","System","Management"], 2, 10, 2, 0.5, 10, 1, 2)
#e.store_doc(["Outbreak","System","Management"], 2, 10, 0, "prova.txt", "content", 1)
#e.store_distance_file(["Outbreak","System","Management"], 2, 10, 0, 0.5, 10, "min_path", "content")
#e.store_result_file(["Outbreak","System","Management"], 2, 10, 0, 0.5, 10, "min_path", 0.1, "content")
#e.store_evaluation_file(["Outbreak","System","Management"], 2, 10, 0, 0.5, 10, "min_path", t_start=0, t_end=1, step=0.1, content="content")