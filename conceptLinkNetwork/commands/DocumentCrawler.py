'''
Created on Sep 22, 2014

@author: alessioferrari
'''
from __future__ import division
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
    
    def write_file(self, chosen_dir, i, link):
        txt = self.get_text(link)
        txt_file = open(chosen_dir + str(i) + "-" + link + ".txt","w")
        txt_file.write(txt)
        txt_file.close()
        
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
        
        if depth < threshold_depth:
            depth = depth + 1
            print depth, threshold_depth
            for link in links[0:threshold_links]:
                self.search_and_store(link, pathsub1, pathsub2, depth, threshold_depth, threshold_links)
                
                
#prj_path = '../tmp/tmp'                
#pathsub1= prj_path + '/1Subject/'
#pathsub2= prj_path + '/2Subject/'
#    
#d = DocumentCrawler()
#d.search_and_store("Outbreak", pathsub1, pathsub2, depth=0, threshold_depth=1, threshold_links=10)
#
#print "done"