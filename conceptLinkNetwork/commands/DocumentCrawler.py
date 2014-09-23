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
    (with the same probability) and with a probability of storing the documents in BOTH folders that decreases while the index
    of the document increases. 
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
    
    
    
prj_path = '../tmp/tmp'                
pathsub1= prj_path + '/1Subject/'
pathsub2= prj_path + '/2Subject/'
    
d = DocumentCrawler()

d.get_text("Outbreak")
links = d.get_links("Outbreak")
num_links = len(links)

#binomial distribution: each document will go in one folder with the same distribution 
n, p = 1, .5
rand_num = numpy.random.binomial(n, p, num_links)


for i, link in enumerate(links): 

    if 'disambiguation' not in link: #disambiguation pages create problems
        
        if rand_num[i]:
            chosen_dir = pathsub1
        else:
            chosen_dir = pathsub2
        
        d.write_file(chosen_dir, i, link)
            
        #probability of a common document decreases
        nc, pc = 1, float(float(1)/float(i+1))    
        rand_num_common = numpy.random.binomial(nc,pc,num_links)
        
        if rand_num_common[i] == 1:
            print 'common!', str(i)
            if chosen_dir == pathsub1:
                chosen_dir = pathsub2
                d.write_file(chosen_dir, i, link)
            elif chosen_dir == pathsub2:
                chosen_dir = pathsub1
                d.write_file(chosen_dir, i, link)
            else:
                print "fail"
            
            
        
print "done"