'''
Created on Oct 29, 2014

@author: alessioferrari
'''
from irutils.TextFilter import TextFilter
from knowledge_graph.SentenceNet import SentenceNet
from knowledge_graph.SentenceNetVisitor import SentenceNetVisitor
from knowledge_graph.constants import DIST_MIN_PATH_SUBGRAPH
from pygraph.classes.digraph import digraph
import nltk


class Subject(SentenceNet):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(Subject, self).__init__()
        self.files_path = dict()
        self.visitor = []
        
    def add_file(self, name, path):
        self.files_path[name] = path
        
    def get_paths(self):
        return self.files_path
    
    def build_knowledge_graph(self):
        fp = [self.files_path[k] for k in self.files_path.keys()]
        super(Subject, self).createNet(fp)
        self.visitor = SentenceNetVisitor(self.get_net(), self.get_edge_start_weight(), self.get_start_occurrences_num()) 
        
        
    def perform_interpretation(self, requirement, type):
        if type == DIST_MIN_PATH_SUBGRAPH:
            
            terms_filter = TextFilter()
            filtered_sent = terms_filter.filter_all(requirement)
        
            path, path_weight = self.visitor.search_A_star(filtered_sent)
            path_tokens = nltk.word_tokenize(path)
        
            current_subgraph = digraph()
        
        for index, term in enumerate(path_tokens):
            subgraph_req = self.get_connected_subgraph(term)
            current_subgraph = self.get_merged_subgraph(current_subgraph,subgraph_req)
            del subgraph_req
        
        return current_subgraph