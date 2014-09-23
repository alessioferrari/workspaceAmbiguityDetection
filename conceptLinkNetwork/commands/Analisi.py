'''
@author: Giuseppe Lipari
'''
from DistanceEvaluators import DistanceEvaluators
#from ProgressBar import progressBar
from SentenceNetCreator import SentenceNetCreator
from SentenceNetVisitor import SentenceNetVisitor
from irutils.TextFilter import TextFilter
from os import listdir
from os.path import isfile, join
from pygraph.classes.digraph import digraph
import nltk
import sys

'''
Metodo che Crea un grafo da una lista di file di testo usando A*
'''
def file_netvisit(file_list,sentencenetvisitor):
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        #first we have to get the sentences from the files
        sentences = []
        
        for f in file_list:
            input_file = f
            fp = open(input_file, 'r')
            text = fp.read()
            sentences.extend(sent_tokenizer.tokenize(text))
            fp.close()
            
        text_filter = TextFilter()
        for sentence in sentences:
                filtered_sent = text_filter.filter_all(sentence)
                
                print filtered_sent
                
                if len(filtered_sent)>0 :
                        sentencenetvisitor.search_A_star(filtered_sent)

                

'''
Initialization
'''
prj_path = '../tmp/tmp'                
pathsub1= prj_path + '/1Subject/'
pathsub2= prj_path + '/2Subject/'
pathreq= prj_path + '/Requirements/'
pathres= prj_path + '/Result/'
distancemethod= 'jaccard'
createmethod= 'nopriority'


fp1 = [ (pathsub1 + f) for f in listdir(pathsub1) if isfile(join(pathsub1,f)) ]
fp2 = [ (pathsub2 + f) for f in listdir(pathsub2) if isfile(join(pathsub2,f)) ]

#Open requirements file and associate one requirement for each line
path_file_req=pathreq + listdir(pathreq)[0]
req_file=open(path_file_req,"r")
reqs = req_file.readlines()
req_file.close()

evaluator=DistanceEvaluators()

EDGE_START_WEIGHT = 1.0
OCCURRENCES_POS = 0 # the tuple representing the number of occurrences is the first attribute (position 0) for each edge
OCCURRENCES_VALUE_POS = 1 # the value of the number of occurrences is in position 1 in the tuple ('occurrences', <occurrences_number>)
START_OCCURRENCES_NUM = 1 # the starting value for the number of occurrences, which will be placed in the node label
'''
Net-Create from list of file with SentenceNetCreator createNet
'''
if createmethod == "nopriority" :
        s1 = SentenceNetCreator()
        s1.createNet(fp1)
        n1 = s1.get_net()
        v1 = SentenceNetVisitor(n1, EDGE_START_WEIGHT, START_OCCURRENCES_NUM) 

        s2 = SentenceNetCreator()
        s2.createNet(fp2)
        n2 = s2.get_net()
        v2 = SentenceNetVisitor(n2, EDGE_START_WEIGHT, START_OCCURRENCES_NUM)


'''
Start net-Create with visit A-star
'''
if createmethod == "priority" :
        s1 = SentenceNetCreator()
        n1 = s1.get_net()
        v1 = SentenceNetVisitor(n1, EDGE_START_WEIGHT, START_OCCURRENCES_NUM)
        file_netvisit(fp1,v1)

        s2 = SentenceNetCreator()
        n2 = s2.get_net()
        v2 = SentenceNetVisitor(n2, EDGE_START_WEIGHT, START_OCCURRENCES_NUM)
        file_netvisit(fp2,v2)


overlap_file = open(pathres+"knowledge_overlap.txt","w")
subject1 = [(f) for f in listdir(pathsub1) if isfile(join(pathsub1,f))]
subject2 = [(f) for f in listdir(pathsub2) if isfile(join(pathsub2,f))]
domain='Subject1:' + ", ".join(subject1) + '\nSubject2:' + ", ".join(subject2) + ' \nDistance Method: '+distancemethod+' with Knowledge Method '+createmethod+'\n'
overlap_file.write(domain)

ind=1
overlap=0

for req in reqs:
        if distancemethod == 'jaccard' :
                overlap, subgraph1, subgraph2 = evaluator.jaccard_evaluator(req,s1,s2,v1,v2)
        else:
                overlap, subgraph1, subgraph2 = evaluator.jaccard_evaluator(req,s1,s2,v1,v2)
        shortreq = req[0:20].replace("/", "-")
        shortreq = shortreq.replace("\\", "-")
        SentenceNetCreator.write_subgraph(pathres + 'R%d-'%(ind)+ shortreq + '-Subject1.gv', subgraph1)
        SentenceNetCreator.write_subgraph(pathres + 'R%d-'%(ind)+ shortreq + '-Subject2.gv', subgraph2)
        r='Overlap:R%d-%s\n%.10f\n'%(ind,req[0:30],overlap)
        
        overlap_file.write(r)
        ind+=1
        del subgraph1
        del subgraph2

overlap_file.close()




