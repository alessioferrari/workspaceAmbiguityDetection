'''
Created on Sep 23, 2014

@author: alessioferrari
'''

from SentenceNet import SentenceNet
from os import listdir
from os.path import isfile, join
from pygraph.classes.digraph import digraph

class SentenceNetPruner(object):
    '''
    classdocs
    '''


    def __init__(self):
        return
    
    @staticmethod
    def pruneNet(sentence_net, threshold_term_count = 0, threshold_edge_weight = float(0.5)):
        '''
        Prunes the @param sentence_net network
        '''
        n = sentence_net.get_net()
        
        #prune the nodes
        term_dict = sentence_net.get_dictionary()
        
        for item in term_dict.keys():
            if term_dict[item] < threshold_term_count:
                n.del_node(item)
        
        #prune the edges
        for e in n.edges():
            if n.edge_weight(e) > threshold_edge_weight:
                n.del_edge(e) 
        
prj_path = './tmp/tmp'                
pathsub1= prj_path + '/1Subject/'


#create the graphs
fp1 = [ (pathsub1 + f) for f in listdir(pathsub1) if isfile(join(pathsub1,f)) ]

s1 = SentenceNet()
s1.createNet(fp1)
print "first graph created", len(s1.get_net().nodes()), len(s1.get_net().edges())
SentenceNetPruner.pruneNet(s1, 10, float(0.5))
print len(s1.get_net().nodes()), len(s1.get_net().edges())

