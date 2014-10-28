'''
@author: Giuseppe Lipari
'''
from __future__ import division
from SentenceNet import SentenceNet
from SentenceNetVisitor import SentenceNetVisitor
from irutils.TextFilter import TextFilter
from pygraph.classes.digraph import digraph
import nltk


class DistanceEvaluators(object):
    '''
    this class provide methods for evaluate distance of two graph path
    '''
    
    def __get_minimum_jaccard(self, nodes1, nodes2):
        '''
        Given two dictionaries of nodes, get the minimum overlap among common
        elements of the two dictionaries
        '''
        
        min_key = ""
        min_jaccard = float(1.0)
        common_keys = set(nodes1.keys()) | set(nodes2.keys())
        
        for key in common_keys:
            intersection_len = len((nodes1[key] & nodes2[key]))
            union_len = len((nodes1[key] | nodes2[key]))
            
            jaccard = 1.0
            if union_len != 0:
                jaccard = intersection_len / union_len
            else:
                jaccard = 1.0
                
            if jaccard <= min_jaccard:
                min_jaccard = jaccard
                min_key = key 
        
        return min_key, min_jaccard
        

    '''
    Method for Jaccard Evaluation
    '''
    def jaccard_evaluator(self,requirement,sentence_net1,sentence_net2,sentence_visitor1,sentence_visitor2):
        
        terms_filter = TextFilter()
        filtered_sent = terms_filter.filter_all(requirement)
        
        path1, path_weight1 = sentence_visitor1.search_A_star(filtered_sent)
        path2, path_weight2 = sentence_visitor2.search_A_star(filtered_sent)
        path1_tokens = nltk.word_tokenize(path1)
        path2_tokens = nltk.word_tokenize(path2)
        current_subgraph1 = digraph()
        current_subgraph2 = digraph()
        
        for index, term in enumerate(path1_tokens):
            subgraph1_req = sentence_net1.get_connected_subgraph(term)
            current_subgraph1 = sentence_net1.get_merged_subgraph(current_subgraph1,subgraph1_req)
            del subgraph1_req
        for index, term in enumerate(path2_tokens):
            subgraph2_req = sentence_net2.get_connected_subgraph(term)
            current_subgraph2 = sentence_net2.get_merged_subgraph(current_subgraph2,subgraph2_req)
            del subgraph2_req
        """
        evaluate the jaccard distance but deletes the words that are contained in filtered_sent
        """
        setpath1 = set(current_subgraph1.nodes())
        setdiff=set(nltk.word_tokenize(filtered_sent))
        setpath2 = set(current_subgraph2.nodes())
        intersection_len = len((setpath1 & setpath2).difference(setdiff))
        union_len = len((setpath1 | setpath2).difference(setdiff))            

        if union_len != 0:
            jaccard = intersection_len / union_len
        else:
            jaccard = 1.0

        return jaccard, current_subgraph1, current_subgraph2    
            
    def jaccard_evaluator_simple(self,requirement,sentence_net1,sentence_net2,sentence_visitor1,sentence_visitor2):
        '''
        This function performs the evaluation of the jaccard distance, but without building the merged graphs.
        Returns the overlapping value, and the sets of concepts for each graph 
        '''
        terms_filter = TextFilter()
        filtered_sent = terms_filter.filter_all(requirement)
        
        path1, path_weight1 = sentence_visitor1.search_A_star(filtered_sent)
        path2, path_weight2 = sentence_visitor2.search_A_star(filtered_sent)
        path1_tokens = nltk.word_tokenize(path1)
        path2_tokens = nltk.word_tokenize(path2)
        subgraph1_nodes = set()
        subgraph2_nodes = set()
        
        for index, term in enumerate(path1_tokens):
            subgraph1_req = sentence_net1.get_connected_subgraph(term)
            subgraph1_nodes = set(set(subgraph1_req.nodes()) | subgraph1_nodes)
            del subgraph1_req
        for index, term in enumerate(path2_tokens):
            subgraph2_req = sentence_net2.get_connected_subgraph(term)
            subgraph2_nodes = set(set(subgraph2_req.nodes()) | subgraph2_nodes)
            del subgraph2_req
        """
        evaluate the jaccard distance but deletes the words that are contained in filtered_sent
        """
        
        setdiff=set(nltk.word_tokenize(filtered_sent))
        intersection_len = len((subgraph1_nodes & subgraph2_nodes).difference(setdiff))
        union_len = len((subgraph1_nodes | subgraph2_nodes).difference(setdiff))            

        if union_len != 0:
            jaccard = intersection_len / union_len
        else:
            jaccard = 1.0

        return jaccard, subgraph1_nodes, subgraph2_nodes
    
    def jaccard_evaluator_minimum(self,requirement,sentence_net1,sentence_net2):
        """
        This function evaluates the jaccard distance as the minimum jaccard among the connected subgraph of 
        the terms included in the sentence, without considering the associated terms
        """
        terms_filter = TextFilter()
        filtered_sent = terms_filter.filter_all(requirement)
        tokens = nltk.word_tokenize(filtered_sent)
        
        subgraph1_nodes = dict()
        subgraph2_nodes = dict()
        
        
        for term in tokens:
            subgraph1_req = sentence_net1.get_connected_subgraph(term)
            subgraph1_nodes[term] = set(set(subgraph1_req.nodes()))
            
            subgraph2_req = sentence_net2.get_connected_subgraph(term)
            subgraph2_nodes[term] = set(set(subgraph2_req.nodes()))
            
            del subgraph2_req
            del subgraph1_req
        
            min_term, min_jaccard = self.__get_minimum_jaccard(subgraph1_nodes, subgraph2_nodes)
        

        return min_jaccard, min_term, subgraph1_nodes[min_term], subgraph2_nodes[min_term] 
        
        
        