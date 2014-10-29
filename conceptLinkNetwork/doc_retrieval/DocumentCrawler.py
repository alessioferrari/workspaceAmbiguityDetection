'''
Created on Sep 22, 2014

@author: alessioferrari
'''
from __future__ import division
from wikipedia.exceptions import PageError, DisambiguationError
import numpy
import os
import wikipedia
import logging


ROOT_PATH = "../knowledge_base"
LOG_FILENAME = ROOT_PATH + os.sep + __name__ + '.log'


class DocumentCrawler(object):
    '''
    This class searches for documents in Wikipedia according to a keyword.
    Moreover, it searches for all the documents linked to the root document associated to the keyword.
    The search is iterated until a certain threshold.
    All the documents are stored in a folder tree, where sub-folders include documents
    with lower depth.  
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.doc_dict = dict()
        
        self.logger = logging.getLogger(__name__) 
        hdlr = logging.FileHandler(LOG_FILENAME, mode="w")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.INFO)  
        
    def __create_folder(self, input_path):
        if not os.path.exists(input_path):
            os.makedirs(input_path) 

    def get_text(self, wikipage=""):
        return wikipedia.page(wikipage).content
        
    def get_links(self, wikipage=""):
        return wikipedia.page(wikipage).links
    
    def write_file(self, file_path, link):
        try:    
            txt = self.get_text(link)
            txt_file = open(file_path + os.sep + link.replace("/","") + ".txt","w")
            txt_file.write(txt)
            txt_file.close()
        except PageError:
            self.logger.exception("Document " + link + " Not found!") 
        except DisambiguationError:
            self.logger.exception("Disambiguation page discarded!") 
        
        self.doc_dict[link] = file_path
    
    def store_files(self, file_path, links):
        for i, link in enumerate(links): 
            self.write_file(file_path, link)
                
    
    def search_and_store(self, term, t_depth, t_links, depth, root_path, create_subfolders):
        '''
        Search the Wikipedia document associated to "term" and store
        the linked documents in a folder named root_path/depth. 
        '''       
            
        if depth == 0:
            self.doc_dict[term] = root_path
            self.write_file(root_path, term)
        
        if create_subfolders == "Y": 
            sub_path= root_path + os.sep + str(depth+1)
            self.__create_folder(sub_path)
        else:
            sub_path = root_path
        
        tabs = ""
        for i in range(depth):
            tabs = tabs + "    "  
        self.logger.info(tabs + "getting links for " + term)  
        links = self.get_links(term)
        num_links = len(links)
        self.logger.info(tabs + "number of links: " + str(num_links))
        
        new_links = list()  
        for link in links:  
            if link not in self.doc_dict.keys():
                    new_links.append(link)
        
        
        self.store_files(sub_path, new_links[0:t_links])
        
        if depth < t_depth-1:
            depth = depth + 1
            for link in new_links[0:t_links]:
                self.search_and_store(link, t_depth, t_links, depth, sub_path, create_subfolders)    
                
    def get_retieved_files(self):
        '''
        This function returns the set of retrieved files in a dictionary.
        It can be used to track where the files are stored
        '''
        return self.doc_dict

d = DocumentCrawler()
d.search_and_store('Outbreak', t_depth = 2, t_links = 10, depth = 0, root_path = ROOT_PATH, create_subfolders="Y")
#print d.get_retieved_files()