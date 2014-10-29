'''
Created on 01/feb/2012

@author: ferrari
'''

from pygraph.algorithms.heuristics.chow import chow
from pygraph.algorithms.heuristics.euclidean import euclidean
from pygraph.algorithms.minmax import heuristic_search, shortest_path
from pygraph.algorithms.searching import breadth_first_search
from pygraph.classes.digraph import digraph
from pygraph.classes.exceptions import NodeUnreachable
from pygraph.classes.graph import graph
from pygraph.readwrite.dot import write
import nltk
import pygraph.algorithms.heuristics.chow





class SentenceNetVisitor(object):
    '''
    this class visits the nodes of a graph and returns the path containing the required sentence
    '''


    def __init__(self, net, edge_start_weight, edge_start_occurrences_num):
        '''
        @param net: is the network to be visited
        @param edge_start_weight: the start weight of each edge
        @param edge_start_occurrences_num: is the starting number of occurrences (normally 1)
        '''
        self.net = net
        self.EDGE_START_WEIGHT = edge_start_weight
        self.START_OCCURRENCES_NUM = edge_start_occurrences_num
        
        
    def search(self):
        st, order = breadth_first_search(self.net, "book")
        gst = digraph()
        gst.add_spanning_tree(st)
        dot = write(gst, True)
        out_file = open("file.gv", "w")
        out_file.write(dot)
        out_file.close()
        
    def search_A_star(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        
        #if a node does not exist, it shall be added to the graph and connected to the previous node
        for i, token in enumerate(tokens):
            if not self.net.has_node(token):
                self.net.add_node(str(token))

                #print "adding node", token
                
            #if the edge does not exist between the current node and the previous one, an edge shall be added
            if i!=0:
                edge = (tokens[i-1], token)
                if not self.net.has_edge(edge):             
                    self.net.add_edge(edge, wt=self.EDGE_START_WEIGHT, label = self.START_OCCURRENCES_NUM)


                    
        h = chow(tokens[0]) #this optimization shall be performed chooosing a term which is connected: the choice of this term shall be performed accoding to some rule
        h.optimize(self.net)
        path = ''
        
        for k, token in enumerate(tokens):
            if k!=0:
                try:                     
                    intermediate_node_path = heuristic_search(self.net, tokens[k-1], token, h) #the path between each couple
                    
                except NodeUnreachable, e:
                    print str(e)
                    print "NODE UREACHABLE"
                        
                for j, node in enumerate(intermediate_node_path): #increase the weight of the edges in the path
                    if j != 0:
                        edge = (intermediate_node_path[j-1], node)
                        if not self.net.has_edge(edge):
                            raise Exception('edge not found')
                        else: #if the edge exists, its weight is divided by the number of occurrences stored in the label
                            number_of_occurrences = self.net.edge_label(edge)
                            new_number_of_occurrences = number_of_occurrences + 1
                            self.net.set_edge_label(edge, new_number_of_occurrences)
                            self.net.set_edge_weight(edge, wt = 1.0/new_number_of_occurrences)
                
                if k < len(tokens)-1: 
                    #we remove the last element to prevent repetitions of head and tail in the subsequences of the final path
                    path = path + ' ' + ' '.join(intermediate_node_path[0:-1])
                else:
                    path = path + ' ' + ' '.join(intermediate_node_path)
                
        path = path[1:] #remove the leading space
        path_weight = self.__get_path_weight(path)
        
        return path, path_weight
                
    def __get_path_weight(self, path_string):
        """
        measures the weight of the @param path given as input
        @param path: the path for which we have to resconstruct the total weight
        """
        path = nltk.word_tokenize(path_string) #the path is currently a string
        edges = [(node, path[i+1]) for i, node in enumerate(path) if i < len(path)-1]
        path_weight = 0
        for e in edges:
            path_weight = path_weight + self.net.edge_weight(e)
        return path_weight

    def __get_min_dist_node(self, source, list_of_inhibited_nodes):
        """
        Returns the neighboring node with minimum distance from @param source.
        The nodes in list_of_inhibited_nodes are not considered
        """
        
        min_dist = 1.0
        min_neighbor = ''

        neighbors = self.net.neighbors(source)

        if source != '':
            if len(neighbors) > 0:

                min_edge = (source, neighbors[0])
                min_dist = self.net.edge_weight(min_edge)
                min_neighbor = neighbors[0]
                
                for n in neighbors:
                    min_edge = (source, n)
                    if self.net.edge_weight(min_edge) < min_dist and n not in list_of_inhibited_nodes:
                        min_dist = self.net.edge_weight(min_edge)
                        min_neighbor = n

        return min_neighbor

    def get_random_sentence(self, seed_term, desired_length):
        """
        Given the @param seed_term, the function starts exploring the graph
        and outputs a sentence of @param desired_length traversing the graph.
        The traversal follows the liks that have the lower weights, but
        does not traverse links that are already traversed
        """
        final_sentence = list()

        if self.net.has_node(seed_term) and desired_length > 0:
            current_node = seed_term
            for num in range(0, desired_length):
                if current_node != '':
                    min_dist_node = self.__get_min_dist_node(current_node, final_sentence)
                    final_sentence.append(min_dist_node)
                    current_node = min_dist_node
                
        return final_sentence
