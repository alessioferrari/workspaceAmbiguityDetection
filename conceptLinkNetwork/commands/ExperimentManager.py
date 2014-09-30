'''
Created on Sep 23, 2014

@author: alessioferrari
'''

from DistanceEvaluators import DistanceEvaluators
from DocumentCrawler import DocumentCrawler
from SentenceNet import SentenceNet
from SentenceNetPruner import SentenceNetPruner
from SentenceNetVisitor import SentenceNetVisitor
from os import listdir
from os.path import isfile, join
import datetime
import numpy
import os


class ExperimentManager(object):
    '''
    stage 0: the class creates two knowledge graphs from the files included in two folders
    stage 1: the class calls the visitor and evaluate the jaccard distance for the example requirements
    stage 2: the class calls the visitor and evaluate the jaccard distance on all the requirements of the experiment
    stage 3: the class calls the visitor and evaluate the jaccard distance on all the requirements of the experiment
    with a reduced graph
    stage 4: the class calls another class that compares the requirements with a result file that includes the tags
    stage 5: the class automatically evaluates precision and recall
    stage 6: the class performs the experiment with different combinations of documents
    
    TODO
    
    stage X: save jaccard distances in a file
    stage X: the class uses a distance method based on single ambiguous terms
    stage X: check whether, among the ambiguous terms found manually, these match with those found automatically  
    '''

    def __init__(self):
        '''
        '''
                
    def iterate_experiment_over_threshold(self, res_path, reqs_list, range_start, range_end, step, s1, s2, v1, v2):
        
        evaluator = DistanceEvaluators()
        
        jaccard_dict = dict()
        for i, requirement in enumerate(reqs_list):
                #print "evaluating distance...", datetime.datetime.now().time()
                jaccard_dict[i], subgraph1, subgraph2 = evaluator.jaccard_evaluator_simple(requirement, s1, s2, v1, v2)
        
        for threshold in numpy.arange(range_start, range_end, step):
            print "evaluation for threshold: ", threshold, " time: ", datetime.datetime.now().time()
            file_name= "file_automatic" + str(threshold) + ".txt"
            fp = open(res_path + os.sep + file_name, "w")
            
            for req_id in jaccard_dict.keys(): 
                if jaccard_dict[req_id] > float(threshold):
                    fp.write((str(str(req_id+1) + ', 0\n')))
                else:
                    fp.write((str(str(req_id+1) + ', 1\n')))
                    
            fp.close()
    
    def set_up_experiment(self, pathsub1, pathsub2, crawl): 
        if crawl == 1:    
            d = DocumentCrawler()
            d.search_and_store("Outbreak", pathsub1, pathsub2, depth=0, threshold_depth=1, threshold_links=10)
        
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
        
        pruner = SentenceNetPruner()
        print "Pruning first network..."
        pruner.pruneNet(s1, threshold_term_count= 10, threshold_edge_weight=float(0.5))
        print "first graph pruned: nodes ", len(s1.get_net().nodes()), " edges ", len(s1.get_net().edges())
        print "Pruning second network..."
        pruner.pruneNet(s2, threshold_term_count= 10, threshold_edge_weight=float(0.5))
        print "second graph pruned: nodes ",  len(s2.get_net().nodes()), " edges ", len(s2.get_net().edges())
        
        return s1, s2, v1, v2

    def perform_experiment(self, s1, s2, v1, v2, pathreq, path_result, rstart, rend, rstep):
    
        path_file_req=pathreq + listdir(pathreq)[0]
        req_file=open(path_file_req,"r")
        reqs = req_file.readlines()
        req_file.close()
        
        print "START", datetime.datetime.now().time()
        
        self.iterate_experiment_over_threshold(path_result, reqs, rstart, rend, rstep, s1, s2, v1, v2)
        
        print "\nFINISH", datetime.datetime.now().time()


prj_path = '../tmp/tmp'                
pathsub1root= prj_path + '/1Subject/'
pathsub2root= prj_path + '/2Subject/'
pathres= prj_path + '/Result/'
pathrequirements = prj_path + '/Requirements/'

NUM_EXP = 3
p_range_start = 0.0
p_range_end = 1.0
p_range_step = 0.01

g = ExperimentManager()

exp_dict = dict()

###### SETUP EXPERIMENT

for i in range(NUM_EXP):

    print  "Set up ", str(i), " time: ", datetime.datetime.now().time()
    pathsub1 = pathsub1root + os.sep + "combination" + str(i) + os.sep
    pathsub2 = pathsub2root + os.sep + "combination" + str(i) + os.sep

    if not os.path.exists(pathsub1):
        os.makedirs(pathsub1)
        
    if not os.path.exists(pathsub2):
        os.makedirs(pathsub2)
    
    s1, s2, v1, v2 = g.set_up_experiment(pathsub1, pathsub2, crawl=0)
    
    exp_dict[i] = [s1, s2, v1, v2] 
    
print "Set up finished...", " time: ", datetime.datetime.now().time()

##### PERFORM EXPERIMENT
     
for i in range(NUM_EXP):

    print  "Experiment ", str(i), " time: ", datetime.datetime.now().time()    
    pathresult = pathres + os.sep + "combination" + str(i) + os.sep
    
    if not os.path.exists(pathresult):
        os.makedirs(pathresult)
    
    g.perform_experiment(exp_dict[i][0], exp_dict[i][1], exp_dict[i][2], exp_dict[i][3], pathrequirements, pathresult, p_range_start, p_range_end, p_range_step)
    print "Experiment ", str(i), " finished time: ", datetime.datetime.now().time()   

#### EVALUATE THRESHOLD

#for i in range(NUM_EXP):
#    
#    print "\n\n", "EXPERIMENT", i, "\n\n"
#    
#    for threshold in numpy.arange(p_range_start, p_range_end, p_range_step):    
#        file_name= "file_automatic" + str(threshold) + ".txt"    
#        e = ResultEvaluator(str('./combination' + str(i)), '../file_manual.txt', file_name)    
#        print "threshold: ", threshold, " (p, r, f1) ", e.compare_results()

#get the documents    
#d = DocumentCrawler()
#d.search_and_store("Outbreak", pathsub1, pathsub2, depth=0, threshold_depth=1, threshold_links=10)


#create the graphs
#fp1 = [ (pathsub1 + f) for f in listdir(pathsub1) if isfile(join(pathsub1,f)) ]
#fp2 = [ (pathsub2 + f) for f in listdir(pathsub2) if isfile(join(pathsub2,f)) ]
#
#s1 = SentenceNet()
#s1.createNet(fp1)
#n1 = s1.get_net()
#v1 = SentenceNetVisitor(n1, s1.get_edge_start_weight(), s1.get_start_occurrences_num()) 
#
#print "first graph created: nodes ", len(s1.get_net().nodes()), " edges ", len(s1.get_net().edges())
#
#s2 = SentenceNet()
#s2.createNet(fp2)
#n2 = s2.get_net()
#v2 = SentenceNetVisitor(n2, s2.get_edge_start_weight(), s2.get_start_occurrences_num())
#
#print "second graph created: nodes ",  len(s2.get_net().nodes()), " edges ", len(s2.get_net().edges())



#evaluator = DistanceEvaluators()
#
#path_file_req=pathreq + listdir(pathreq)[0]
#req_file=open(path_file_req,"r")
#reqs = req_file.readlines()
#req_file.close()
#
#print "START", datetime.datetime.now().time()
#
#manager = GraphCreatorManager()
#manager.iterate_experiment_over_threshold(pathres, reqs, 0.6, 0.7, 0.01, s1, s2, v1, v2)
#
#print "\nFINISH", datetime.datetime.now().time()


#fp = open("file_automatic.txt", "w")
#
#for i, requirement in enumerate(reqs):
#    print "evaluating distance...", datetime.datetime.now().time()
#    jaccard, subgraph1, subgraph2 = evaluator.jaccard_evaluator_simple(requirement, s1, s2, v1, v2)
#    print "req: ", requirement[0:30], jaccard
#    if jaccard > float(0.66):
#        fp.write((str(str(i+1) + ', 0\n')))
#    else:
#        fp.write((str(str(i+1) + ', 1\n')))
#    #jaccard, term, set1, set2 = evaluator.jaccard_evaluator_minimum(requirement, s1, s2)
#    #print "req: ", requirement[0:30], jaccard, term, set1, set2
#    print "done", datetime.datetime.now().time()
#
#fp.close()





