'''
Created on Oct 30, 2014

@author: alessioferrari
'''
from __future__ import division
from distances.constants import DIST_TYPE_JACCARD


class DistanceEvaluation(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def __compute_union(self,graph_list):
        nodes_union = set()
        for g in graph_list:
            nodes_union = nodes_union | set(g.nodes())
        return nodes_union
        
    def __compute_intersection(self,graph_list):
        nodes_intersection = set(graph_list[0])
        for g in graph_list[1:len(graph_list)]:
            g_nodes = set(g.nodes())
            nodes_intersection = nodes_intersection & g_nodes
        return nodes_intersection     
        
    def evaluate_distance(self, dist_type, graph_list):
        
        if dist_type == DIST_TYPE_JACCARD:
            nodes_union = self.__compute_union(graph_list)
            nodes_intersection = self.__compute_intersection(graph_list)
            union_len = len(nodes_union)
            intersection_len = len(nodes_intersection)
            
            if union_len != 0:
                jaccard = float(intersection_len / union_len)
            else:
                jaccard = 1.0
            
            return jaccard
        
        else:
            return -1
                