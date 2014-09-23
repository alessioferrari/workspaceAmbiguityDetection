'''
Created on 16/12/2013

@author: Giuseppe Lipari
La classe riceve in ingresso il path del progetto, il path di conceptLink,
ed il path del documento dei requisiti da analizzare in formato txt formato una riga per ogni requisito.
'''
from __future__ import division
import nltk
import sys
from pygraph.classes.digraph import digraph
sys.path.insert(1, sys.argv[2])
sys.path.insert(1, sys.argv[2]+'irutils')
from os import listdir
from os.path import isfile, join
from irutils.TextFilter import TextFilter
from SentenceNetCreator import SentenceNetCreator
from SentenceNetVisitor import SentenceNetVisitor

EDGE_START_WEIGHT = 1.0
OCCURRENCES_POS = 0 # the tuple representing the number of occurrences is the first attribute (position 0) for each edge
OCCURRENCES_VALUE_POS = 1 # the value of the number of occurrences is in position 1 in the tuple ('occurrences', <occurrences_number>)
START_OCCURRENCES_NUM = 1 # the starting value for the number of occurrences, which will be placed in the node label

pathsub1=sys.argv[1] + '/1Subject/'
pathsub2=sys.argv[1] + '/2Subject/'
requirements_doc=sys.argv[3]
pathres=sys.argv[1] + '/Result/'

requirements_terms = 0
new_terms1 = 0
new_terms2 = 0

#print path_file_req
req_file=open(requirements_doc,"r")
reqs= req_file.readlines()
req_file.close()
print len(reqs)
result_understand=open(pathres + "understand.txt","w")
sub1_terms = []
sub2_terms = []

fp1 = [ (pathsub1 + f) for f in listdir(pathsub1) if isfile(join(pathsub1,f)) ]
fp2 = [ (pathsub2 + f) for f in listdir(pathsub2) if isfile(join(pathsub2,f)) ]
result_understand.write("File Document:"+requirements_doc+"\nSubject1 Knowledge: "+", ".join(listdir(pathsub1))+"\nSubject2 Knowledge: "+", ".join(listdir(pathsub2))+"\n")
#Creo i KG dei soggetti
s1 = SentenceNetCreator()
s1.createNet(fp1)
n1 = s1.get_net()
v1 = SentenceNetVisitor(n1, EDGE_START_WEIGHT, START_OCCURRENCES_NUM)

s2 = SentenceNetCreator()
s2.createNet(fp2)
n2 = s2.get_net()
v2 = SentenceNetVisitor(n2, EDGE_START_WEIGHT, START_OCCURRENCES_NUM)

text_filter = TextFilter()

for requirement in reqs:
    sub1_terms=[]
    sub2_terms=[]
    filtered_requirement = text_filter.filter_all(requirement)
    tokens = nltk.word_tokenize(filtered_requirement)
    single_tokens=list(set(tokens))
    for token in single_tokens:
        requirements_terms+=1
        if not s1.gr.has_node(token):
            sub1_terms.append(str(token))
            new_terms1+=1
            s1.gr.add_node(str(token))
        if not s2.gr.has_node(token):
            new_terms2+=1
            sub2_terms.append(str(token))
            s2.gr.add_node(str(token))
    if len(sub1_terms)>0 or len(sub2_terms)>0:
        result_understand.write("\n"+ requirement.upper())
        if len(sub1_terms)>0:
            terms1=', '.join(sub1_terms)
            result_understand.write("Subject1 missing terms:" + terms1 +"\n")
        if len(sub2_terms)>0:
            terms2=', '.join(sub2_terms)
            result_understand.write("Subject2 missing terms:" + terms2 + "\n")
        
sub1_degree=(requirements_terms - new_terms1)/ requirements_terms
sub2_degree=(requirements_terms - new_terms2)/ requirements_terms
result_understand.write('\nSubject1 understandable degree:%.10f\n'%(sub1_degree))
result_understand.write('Subject2 understandable degree:%.10f\n'%(sub2_degree))
result_understand.close()

           
