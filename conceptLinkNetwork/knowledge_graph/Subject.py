'''
Created on Oct 29, 2014

@author: alessioferrari
'''
from irutils.TextFilter import TextFilter
from knowledge_graph.SentenceNet import SentenceNet
from knowledge_graph.SentenceNetVisitor import SentenceNetVisitor
from knowledge_graph.constants import INT_MIN_PATH_SUBGRAPH, REQ_TERMS_REMOVE, \
    INT_SUBGRAPH
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
     
    def __perform_min_path_subgraph(self, filtered_sent):
                    
    
        path, path_weight = self.visitor.search_A_star(filtered_sent)
        #path_tokens = nltk.word_tokenize(path)
              
        return self.__perform_int_subgraph(path)
    
    def __perform_int_subgraph(self, filtered_sent):
        
        current_subgraph = digraph()
        sent_tokens =  nltk.word_tokenize(filtered_sent)
        
        for term in sent_tokens:
            
            subgraph_req = self.get_connected_subgraph(term)
            if subgraph_req.nodes() != []:
                current_subgraph = self.get_merged_subgraph(current_subgraph,subgraph_req)
            del subgraph_req
            
        return current_subgraph
        
    def perform_interpretation(self, requirement, type, flag_remove_req_terms):
        '''
        the @param remove_req_terms: when set to REQ_TERMS_REMOVE, removes from the
        interpretation all the nodes corresponding to the terms in the original
        requirement, if these have been stored in the path. 
        '''
        terms_filter = TextFilter()
        filtered_sent = terms_filter.filter_all(requirement)
        
        if type == INT_MIN_PATH_SUBGRAPH:
            current_subgraph = self.__perform_min_path_subgraph(filtered_sent)
        elif type == INT_SUBGRAPH:
            current_subgraph = self.__perform_int_subgraph(filtered_sent)
            
        if flag_remove_req_terms == REQ_TERMS_REMOVE:
            for term in set(nltk.word_tokenize(filtered_sent)):
                if term in current_subgraph.nodes():
                    current_subgraph.del_node(term)
        
        return current_subgraph