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
    
    def pruneNet(self, sentence_net_in, threshold_term_count = 0, threshold_edge_weight = float(0.5)):
        '''
        Prunes the @param sentence_net network
        '''
        n = sentence_net_in.get_net()
        
        #prune the nodes
        term_dictionary = sentence_net_in.get_dictionary()
        
        for item in term_dictionary.keys():
            if term_dictionary[item] < threshold_term_count:
                    n.del_node(item)
                    del term_dictionary[item]
        
        #prune the edges
        for e in n.edges():
            if n.edge_weight(e) > threshold_edge_weight:
                n.del_edge(e) 
        
prj_path = './tmp/tmp'                
pathsub2= prj_path + '/2Subject/'
pathsub1= prj_path + '/1Subject/'

##create the graphs
#fp2 = [ (pathsub2 + f) for f in listdir(pathsub2) if isfile(join(pathsub2,f)) ]
#pruner1 = SentenceNetPruner()
#pruner2 = SentenceNetPruner()
##
#s2 = SentenceNet()
#s2.createNet(fp2)
#print >> open('log.txt', 'a'), "first graph created", len(s2.get_net().nodes()), len(s2.get_net().edges())
#print >> open('log.txt', 'a'), s2.get_dictionary()
#print >> open('log.txt', 'a'), s2.get_net().nodes()
#
#pruner2.pruneNet(s2, 10, float(0.5))
#print >> open('log.txt', 'a'), len(s2.get_net().nodes()), len(s2.get_net().edges())
#
#fp1 = [ (pathsub1 + f) for f in listdir(pathsub1) if isfile(join(pathsub1,f)) ]
##
#s1 = SentenceNet()
#s1.createNet(fp1)
#print >> open('log.txt', 'a'), "second graph created", len(s1.get_net().nodes()), len(s1.get_net().edges())
#print >> open('log.txt', 'a'), s1.get_dictionary()
#print >> open('log.txt', 'a'), "nodes..."
#print >> open('log.txt', 'a'), s1.get_net().nodes()
#
#pruner1.pruneNet(s1, 10, float(0.5))
#print len(s1.get_net().nodes()), len(s1.get_net().edges())
