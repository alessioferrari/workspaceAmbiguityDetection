'''
Created on Sep 23, 2014

@author: alessioferrari
'''

from SentenceNet import SentenceNet
from SentenceNetVisitor import SentenceNetVisitor
from DistanceEvaluators import DistanceEvaluators
from os import listdir
from os.path import isfile, join


class GraphCreatorManager(object):
    '''
    stage 0: the class creates two knowledge graphs from the files included in two folders
    stage 1: the class calls the visitor and evaluate the jaccard distance for the example requirements
    '''

    def __init__(self):
        '''
        '''

prj_path = '../tmp/tmp'                
pathsub1= prj_path + '/1Subject/'
pathsub2= prj_path + '/2Subject/'
pathres= prj_path + '/Result/'

#get the documents    
#d = DocumentCrawler()
#d.search_and_store("Outbreak", pathsub1, pathsub2, depth=0, threshold_depth=1, threshold_links=10)


#create the graphs
fp1 = [ (pathsub1 + f) for f in listdir(pathsub1) if isfile(join(pathsub1,f)) ]
fp2 = [ (pathsub2 + f) for f in listdir(pathsub2) if isfile(join(pathsub2,f)) ]

s1 = SentenceNet()
s1.createNet(fp1)
n1 = s1.get_net()
v1 = SentenceNetVisitor(n1, s1.get_edge_start_weight(), s1.get_start_occurrences_num()) 

print "first graph created: nodes ", len(s1.get_net().nodes()), " edges ", len(s1.get_net().edges())

s2 = SentenceNet()
s2.createNet(fp2)

n2 = s2.get_net()
v2 = SentenceNetVisitor(n2, s2.get_edge_start_weight(), s2.get_start_occurrences_num())

print "second graph created: nodes ",  len(s2.get_net().nodes()), " edges ", len(s2.get_net().edges())

requirement = "Each new case must be able to link an assigned Entity ID to an Event ID within the scope of the investigation."
evaluator = DistanceEvaluators()

print "evaluating distance..."
overlap, subgraph1, subgraph2 = evaluator.jaccard_evaluator(requirement, s1, s2, v1, v2)
print "done"
#shortreq = requirement[0:20].replace("/", "-")
#shortreq = shortreq.replace("\\", "-")
#SentenceNet.write_subgraph(pathres + shortreq + '-Subject1.gv', subgraph1)
#SentenceNet.write_subgraph(pathres + shortreq + '-Subject2.gv', subgraph2)
#print 'Overlap:R%d-%s\n%.10f\n'%(requirement[0:30],overlap)


