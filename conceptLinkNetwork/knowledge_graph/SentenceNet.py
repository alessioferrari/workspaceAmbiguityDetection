'''
Created on 24/gen/2012

@author: ferrari
'''
from __future__ import division
from SentenceNetVisitor import SentenceNetVisitor
from irutils.TextFilter import TextFilter
from pygraph.classes.digraph import digraph
from pygraph.classes.graph import graph
from pygraph.readwrite.dot import write
import nltk



##fp1 = '../docs/wikipedia.txt'
##fp2 = '../docs/gediminas2005.txt'
##fp3 = '../docs/burke.txt'
##fp4 = '../docs/felfering2007.txt'


EDGE_START_WEIGHT = 1.0
OCCURRENCES_POS = 0 # the tuple representing the number of occurrences is the first attribute (position 0) for each edge
OCCURRENCES_VALUE_POS = 1 # the value of the number of occurrences is in position 1 in the tuple ('occurrences', <occurrences_number>)
START_OCCURRENCES_NUM = 1 # the starting value for the number of occurrences, which will be placed in the node label

class SentenceNet(object):
    
    '''
    classdocs
    '''


    def __init__(self):
        self.gr = digraph()
        self.term_dict = dict()
        #self.sentences = []
        self.edge_start_weight = EDGE_START_WEIGHT
        self.start_occurrences_num = START_OCCURRENCES_NUM 
            
    def get_net(self):
        return self.gr

    def get_edge_start_weight(self):
        return self.edge_start_weight

    def get_start_occurrences_num(self):
        return self.start_occurrences_num
    
    def get_dictionary(self):
        return self.term_dict

    @staticmethod    
    def write_subgraph(dest_file_name, subgraph):
        dot = write(subgraph, True)
        out_file = open(dest_file_name, "w")
        out_file.write(dot)
        out_file.close()
    
    @staticmethod    
    def merge_graphs(g1, g2):
        """
        This function merges two graphs. Merging the two graphs
        implies adding to the first graph all nodes and edges 
        of the second graph, if these do not exist.
        """
        subgraph = digraph()
        subgraph.add_nodes(g1.nodes())
        
        for edge in g1.edges():
            subgraph.add_edge(edge)
        
        for node in g2.nodes():
            if node not in subgraph.nodes():
                subgraph.add_node(node)
                
        for edge in g2.edges():
            if edge not in subgraph.edges():
                subgraph.add_edge(edge)

        return subgraph


    def createNet(self, sentences_file_list):
        """
        this function takes a list of files and build a network from the words contained in the files
        @param sentence_file_list: the list of paths (string)  to the files
        """
        
        
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        #first we have to get the sentences from the files
        sentences = []
        
        for f in sentences_file_list:
            input_file = f
            fp = open(input_file, 'r')
            text = fp.read()
            sentences.extend(sent_tokenizer.tokenize(text))
            fp.close()
        
        self.createNetFromSentences(sentences)
       
            
    def createNetFromSentences(self, sentences):
        "This function creates the network starting from a set of sentences"
        
        text_filter = TextFilter()
        for sentence in sentences:
            filtered_sentence = text_filter.filter_all(sentence)
            
            
            tokens = nltk.word_tokenize(filtered_sentence)
            single_tokens = list(set(tokens))
            
            for token in single_tokens:
                if not self.gr.has_node(token):
                    self.gr.add_node(str(token))
                    self.term_dict[token] = 1
                else:
                    self.term_dict[token] = self.term_dict[token] + 1 
            
            for i, token in enumerate(tokens):
                if i != 0:
                    edge = (tokens[i-1], token)
                    if not self.gr.has_edge(edge):
                        self.gr.add_edge(edge, wt=1.0, label = START_OCCURRENCES_NUM)
                    else:
                        #If the edge exists, the weight of the edge shall divided by the number of occurrences of the couple of terms.
                        #Therefore, we shall keep memory of the number of occurrences for each couple of terms.
                        number_of_occurrences = self.gr.edge_label(edge)
                        new_number_of_occurrences = number_of_occurrences + 1
                        self.gr.set_edge_label(edge, new_number_of_occurrences)
                        self.gr.set_edge_weight(edge, wt = 1.0/new_number_of_occurrences)
            
    def write_graph(self, dest_file_name):
        dot = write(self.gr, True)
        out_file = open(dest_file_name, "w")
        out_file.write(dot)
        out_file.close()
        
    def get_subgraph(self, nodes):
        """"
        The function takes a set of nodes and returns a graph 
        that contain all such nodes together with the edges
        of the current graph that connect those nodes.
        The function returns -1 if one of the nodes does not belong
        to the current graph.
        """
        
        for node in nodes:
            if node not in self.gr.nodes():
                return -1
        
        subgraph = digraph()
        
        for node in nodes:
            subgraph.add_node(node)
        
        for edge in self.gr.edges():
            if edge[0] in nodes and edge[1] in nodes:
                edge_weight = self.gr.edge_weight(edge)
                subgraph.add_edge(edge, wt=edge_weight, label=str(edge_weight))
                
        return subgraph
            
        
    def get_merged_subgraph(self, g1, g2):
        """
        The function takes the two graphs @param g1 and @param g2 and 
        returns the subgraph of the original graph that
        contains the nodes of the two subgraphs , otgether with the weigthed edges of the original graph.
        The function returns -1 if the get_subgraph function returns -1
        """
        nodes = list(set(g1.nodes()) | set(g2.nodes()))
        
        merged_subgraph = self.get_subgraph(nodes)
        
        if merged_subgraph != -1:
            return merged_subgraph
        else:
            return -1 
        
        
    def get_connected_subgraph(self, node):
        """
        Given a @param node extracts the subgraph connected to the node
        if the weigth is lower than 1
        """
        subgraph = digraph()
        for edge in self.gr.edges():
            if node in edge:
                if self.gr.edge_weight(edge) < 1.0:
                    if edge[0] not in subgraph.nodes():
                        subgraph.add_node(edge[0])
                    if edge[1] not in subgraph.nodes():
                        subgraph.add_node(edge[1])
                    if edge not in subgraph.edges():
                        subgraph.add_edge(edge, wt = self.gr.edge_weight(edge))

        return subgraph

    

    
#    def evaluate_jaccard(self, path1, path2, filtered_sent):
#        """
#        evaluate the jaccard distance but deletes the words that are contained in filtered_sent
#        """
#        intersection_len = len((set(nltk.word_tokenize(path1)) & (set(nltk.word_tokenize(path2)))).difference(set(nltk.word_tokenize(filtered_sent))))
#        union_len = len((set(nltk.word_tokenize(path1)) | set(nltk.word_tokenize(path2))).difference(set(nltk.word_tokenize(filtered_sent))))              
#        if union_len != 0:
#            jaccard = intersection_len / union_len
#        else:
#            jaccard = 1.0
#
#        return jaccard
    
    def get_avg_edge_weight(self):
        """
        Extracts the average edge weight
        """
        total_weight = 0.0
        for edge in self.gr.edges():
            total_weight = total_weight + self.gr.edge_weight(edge)
        
        return total_weight / len(self.gr.edges())
    
    def get_minumum_weight(self):
        """
        Extracts the edge with minimum weight
        """
        min_weight = 1.0
        min_edge = None
        for edge in self.gr.edges():
            if self.gr.edge_weight(edge) < min_weight and edge != ('recommend', 'system'):
                min_edge = edge
                min_weight = self.gr.edge_weight(edge)
        
        return min_weight, min_edge
    
    def resubgraph(self, g1, g2):
        """
        given two graphs subtract the first to the second
        """
        for edge in g2.edges():
            if edge not in g1.edges():
                g2.del_edge(edge)
            
        return g2
            
###Subject 1        
##s1 = SentenceNet()
###s1.createNet([fp1])
##n1 = s1.get_net()
##v1 = SentenceNetVisitor(n1, EDGE_START_WEIGHT, START_OCCURRENCES_NUM)

###Subject 2
##s2 = SentenceNet()
#s2.createNet([fp2])
##n2 = s2.get_net()
##v2 = SentenceNetVisitor(n2, EDGE_START_WEIGHT, START_OCCURRENCES_NUM)
##
##
##xml_doc_handler = XMLReqManager('req_document.xsd', '2007 - eirene fun 7.xml')
##req_document = xml_doc_handler.get_requirements_text()

##req_document = [
##                'The network services necessary to meet the range of UIC requirements are detailed \
##below.  These  services  are  to  be  considered  as  a  minimum  set  for  implementation \
##within  each  UIC  standard  network.  Railways  may  implement  additional  network \
##services as desired',
##                'This section describes the generic voice telephony services which are to be supported \
##by the EIRENE network',
##                'The network  necessary to  the range of  requirements are detailed \
##below.  These  services  are  to  be  considered  as  a    set  for  implementation \
##within  each  UIC  standard  network.  may  implement  additional  network \
##services as desired',
##                ]

##terms_filter = TextFilter()
##
##for sent in req_document:
##    filtered_sent = terms_filter.filter_all(sent)
##    #print "considering sentence: ", filtered_sent
##    #print "first automaton"   
##    path1, path_weight1 = v1.search_A_star(filtered_sent)
##
##print "graph built"
##
##print "now producing a random sentence according to the document learnt..."
##print v1.get_random_sentence('network', 100)




##    print "second automaton"
##    path2, path_weight2 = v2.search_A_star(filtered_sent)
##    print 'path_intersection = ', (set(nltk.word_tokenize(path1)) & (set(nltk.word_tokenize(path2)))).difference(set(nltk.word_tokenize(filtered_sent)))
##    if len(nltk.word_tokenize(path1)) != 0 and len(nltk.word_tokenize(path2)) != 0:
##        print 'path1_weight = ', path_weight1/(len(nltk.word_tokenize(path1)))
##        print 'path2_weight = ', path_weight2/(len(nltk.word_tokenize(path2)))
##        print 'path_diff = ', path_weight1/(len(nltk.word_tokenize(path1))) - path_weight2/(len(nltk.word_tokenize(path2)))    
##        print 'jaccard = ', s2.evaluate_jaccard(path1, path2, filtered_sent)
##    else:
##        print 'one of the paths is empty'
    
##for sent in req_document:
##    filtered_sent = terms_filter.filter_all(sent)
##    path1, path_weight1 = v1.search_A_star(filtered_sent)
##    path2, path_weight2 = v2.search_A_star(filtered_sent)
##    print path1
##    print path2
##    print 'path_intersection = ', (set(nltk.word_tokenize(path1)) & (set(nltk.word_tokenize(path2)))).difference(set(nltk.word_tokenize(filtered_sent)))
##    print 'path1_weight = ', path_weight1/(len(nltk.word_tokenize(path1)))
##    print 'path2_weight = ', path_weight2/(len(nltk.word_tokenize(path2)))
##    print 'path_diff = ', path_weight1/(len(nltk.word_tokenize(path1))) - path_weight2/(len(nltk.word_tokenize(path2)))    
##    print 'jaccard = ', s2.evaluate_jaccard(path1, path2, filtered_sent)
##    
