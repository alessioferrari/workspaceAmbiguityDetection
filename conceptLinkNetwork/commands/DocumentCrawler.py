'''
Created on Sep 22, 2014

@author: alessioferrari
'''
from __future__ import division
from ExperimentFolderManager import ExperimentFolderManager
from constants import SUBJECT_1, SUBJECT_2
from wikipedia.exceptions import PageError, DisambiguationError
import numpy
import wikipedia



class DocumentCrawler(object):
    '''
    stage 0: the class searches for documents in Wikipedia and store their content in a folder
    stage 1: the class searches for documents in Wikipedia and store their content in two folders
    stage 3: the class searches for documents in Wikipedia and store their content in two folders 
    with a probability 0.7 (in first folder) and 0.3 (in second folder)
    stage 4: the class searches for documents in Wikipedia and store their content in two folders 
    (with the same probability) and with a probability of storing the documents in BOTH folders that decreases 
    while the index
    of the document increases. 
    stage 5: the class searches for documents in Wikipedia and store their content in two folders 
    (with the same probability), and with a probability of storing the documents in BOTH folders that decreases while 
    the depth of the link increases 
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.doc_list= list()
    
    def write_file(self, chosen_dir, i, link):
        txt = self.get_text(link)
        txt_file = open(chosen_dir + str(i) + "-" + link + ".txt","w")
        txt_file.write(txt)
        txt_file.close()
        
    def new_write_file(self, folder_mng, keywords, t_depth, t_links, set_id, chosen_subj, link):
        try:    
            txt = self.get_text(link)
            folder_mng.store_doc(keywords, t_depth, t_links, set_id, link.replace("/","") + ".txt", txt, chosen_subj)
        except PageError:
            print "Document " + link + " Not found!"
        except DisambiguationError:
            print "Disambiguation page discarded!"
        
        
    def get_text(self, wikipage=""):
        return wikipedia.page(wikipage).content
        
    def get_links(self, wikipage=""):
        return wikipedia.page(wikipage).links
    
    def store_files(self, pathsub1, pathsub2, links, rand_num_choice, rand_num_common):
        for i, link in enumerate(links): 
            
            if 'disambiguation' not in link: #disambiguation pages create problems
                
                #choose a folder
                if rand_num_choice[i]:
                    chosen_dir = pathsub1
                else:
                    chosen_dir = pathsub2
                self.write_file(chosen_dir, i, link)
            
                #choose to copy in the other folder or not
                if rand_num_common[i]:
                    if chosen_dir == pathsub1:
                        chosen_dir = pathsub2
                    else:
                        chosen_dir = pathsub1
                    self.write_file(chosen_dir, i, link)
    
    def search_and_store(self, term, pathsub1, pathsub2, depth, threshold_depth, threshold_links):
        #self.get_text(term)
        
        print "getting links for ", term
        links = self.get_links(term)
        num_links = len(links)
        print "number of links: ", num_links
        
        #binomial distribution: each document will go in one folder with the same distribution 
        n, p = 1, .5
        rand_num_choice = numpy.random.binomial(n,p,num_links)

        #probability of a common document decreases with the depth
        nc, pc = 1, float(float(1)/float(depth+1))    
        rand_num_common = numpy.random.binomial(nc,pc,num_links)
        
        self.store_files(pathsub1, pathsub2, links[0:threshold_links], rand_num_choice, rand_num_common)
        
        if depth <= threshold_depth:
            depth = depth + 1
            print depth, threshold_depth
            for link in links[0:threshold_links]:
                self.search_and_store(link, pathsub1, pathsub2, depth, threshold_depth, threshold_links)

    def new_store_files(self, folder_mng, keywords, t_depth, t_links, set_id, links, rand_num_choice, rand_num_common):
            for i, link in enumerate(links): 
                
                if 'disambiguation' not in link: #disambiguation pages create problems
                    self.doc_list.append(link)
                    
                    #choose a folder
                    if rand_num_choice[i]:
                        chosen_subj = SUBJECT_1
                    else:
                        chosen_subj = SUBJECT_2
                    self.new_write_file(folder_mng, keywords, t_depth, t_links, set_id, chosen_subj, link)
                
                    #choose to copy in the other folder or not
                    if rand_num_common[i]:
                        if chosen_subj == SUBJECT_1:
                            chosen_subj = SUBJECT_2
                        else:
                            chosen_subj = SUBJECT_1
                        self.new_write_file(folder_mng, keywords, t_depth, t_links, set_id, chosen_subj, link)


    def new_search_and_store(self, term, folder_mng, keywords, t_depth, t_links, set_id, depth):
            tabs = ""
            for i in range(depth):
                tabs = tabs + "    "
            
            
            if depth == 0:
                self.doc_list.append(term)
            
            print tabs, "getting links for ", term
            links = self.get_links(term)
            num_links = len(links)
            print tabs, "number of links: ", num_links
            
            #binomial distribution: each document will go in one folder with the same distribution 
            n, p = 1, .5
            rand_num_choice = numpy.random.binomial(n,p,num_links)
    
            #probability of a common document decreases with the depth
            nc, pc = 1, float(float(1)/float(depth+1))    
            rand_num_common = numpy.random.binomial(nc,pc,num_links)
            
            
            new_links = list()  
            for link in links:  
                if link not in self.doc_list:
                        new_links.append(link)
            
            self.new_store_files(folder_mng, keywords, t_depth, t_links, set_id, new_links[0:t_links], rand_num_choice, rand_num_common)
            
            if depth < t_depth-1:
                depth = depth + 1
                for link in new_links[0:t_links]:
                    self.new_search_and_store(link, folder_mng, keywords, t_depth, t_links, set_id, depth)

    def print_doc_tree(self, depth, t_depth, term, t_links):
        if depth == 0:
            self.doc_list.append(term)
            
        tabs = ""
        for i in range(depth):
            tabs = tabs + "    "
        
        print tabs, "getting links for ", term
        links = self.get_links(term)
        num_links = len(links)
        print tabs, "number of links: ", num_links
        
        new_links = list()  
        for link in links:  
            if link not in self.doc_list:
                    self.doc_list.append(link)
                    new_links.append(link)         
        
        if depth < t_depth-1:
            depth = depth + 1
            for link in new_links[0:t_links]:
                    self.print_doc_tree(depth, t_depth, link, t_links)
        
                    
#EXPERIMENT PARAMETERS
p_keywords = ['Outbreak', 'Software development']
p_t_depth = 2
p_t_links = 10
p_sets_num = 2
p_cut_e = 0.5
p_cut_n = 0

folder_manager = ExperimentFolderManager('./')   
folder_manager.create_experiment_folder_structure(p_keywords, p_t_depth, p_t_links, p_sets_num, p_cut_e, p_cut_n)     
    
d = DocumentCrawler()
#d.print_doc_tree(0,p_t_depth,"Outbreak",p_t_links)
for k in p_keywords:
    d.new_search_and_store(k, folder_manager, p_keywords, p_t_depth, p_t_links, 0, 0)

print len(d.doc_list)                
#prj_path = '../tmp/tmp'                
#pathsub1= prj_path + '/1Subject/'
#pathsub2= prj_path + '/2Subject/'
#    
#d = DocumentCrawler()
#d.search_and_store("Outbreak", pathsub1, pathsub2, depth=0, threshold_depth=1, threshold_links=10)
#
#print "done"