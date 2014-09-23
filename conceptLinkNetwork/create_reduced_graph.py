"""
This function creates the domain knowledge graphs from two documents,
fp1 and fp2. Then, given a sentence, returns the shortest path
within each graph together with the subgraphs attached to each node.
"""

from SentenceNet import SentenceNet
from SentenceNetVisitor import SentenceNetVisitor
from irutils.TextFilter import TextFilter
from pygraph.classes.digraph import digraph
import nltk

fp1 = '../docs/wikipedia.txt'
fp2 = '../docs/gediminas2005.txt'
fp3 = '../docs/ricci.txt'
fp4 = '../docs/wikipediagediminas2005.txt'

sentenceNetWiki = SentenceNet()
sentenceNetWiki.createNet([fp1])
sentenceNetWiki.write_graph('wikipedia_graph.gv')
print 'Wiki size', len(sentenceNetWiki.get_net().nodes())

sentenceNetGediminas = SentenceNet()
sentenceNetGediminas.createNet([fp2])
sentenceNetGediminas.write_graph('gediminas_graph.gv')
print 'Gediminas size', len(sentenceNetGediminas.get_net().nodes())

sentenceNetRicci = SentenceNet()
sentenceNetRicci.createNet([fp3])
sentenceNetRicci.write_graph('ricci_graph.gv')
print 'Ricci size', len(sentenceNetRicci.get_net().nodes())

sentenceNetWikiGedi = SentenceNet()
sentenceNetWikiGedi.createNet([fp4])
sentenceNetWikiGedi.write_graph('wikigedi_graph.gv')
print 'WikiGedi size', len(sentenceNetWikiGedi.get_net().nodes())

print "Weighted Knowledge Graphs created"

terms_filter = TextFilter()
sentence = "The system shall display similar books"
filtered_sent = terms_filter.filter_all(sentence)

visitor_wiki = SentenceNetVisitor(sentenceNetWiki.get_net(), sentenceNetWiki.get_edge_start_weight(), sentenceNetWiki.get_start_occurrences_num())
path_wiki, path_weight_wiki = visitor_wiki.search_A_star(filtered_sent)

print path_wiki
print path_weight_wiki

visitor_gediminas = SentenceNetVisitor(sentenceNetGediminas.get_net(), sentenceNetGediminas.get_edge_start_weight(), sentenceNetGediminas.get_start_occurrences_num())
path_gediminas, path_weight_gediminas = visitor_gediminas.search_A_star(filtered_sent)

print path_gediminas
print path_weight_gediminas

visitor_ricci = SentenceNetVisitor(sentenceNetRicci.get_net(), sentenceNetRicci.get_edge_start_weight(), sentenceNetGediminas.get_start_occurrences_num())
path_ricci, path_weight_ricci = visitor_ricci.search_A_star(filtered_sent)

print path_ricci
print path_weight_ricci

visitor_wikigedi = SentenceNetVisitor(sentenceNetWikiGedi.get_net(), sentenceNetWikiGedi.get_edge_start_weight(), sentenceNetGediminas.get_start_occurrences_num())
path_wikigedi, path_weight_wikigedi = visitor_wikigedi.search_A_star(filtered_sent)

print path_wikigedi
print path_weight_wikigedi

#now saving the subgraph associated to each term in the minimum weighted path
#note that a path is currently a string: 
'''@todo: this thing shall be modified
'''
path_wiki_tokens = nltk.word_tokenize(path_wiki)
current_subgraph = digraph()
for index, term in enumerate(path_wiki_tokens):
    subgraphwiki = sentenceNetWiki.get_connected_subgraph(term)
    current_subgraph = sentenceNetWiki.get_merged_subgraph(current_subgraph, subgraphwiki)
    #sentenceNetWiki.write_subgraph('./graphs/subgraph_wiki' + str(index) + '.gv', subgraphwiki)
SentenceNet.write_subgraph('./graphs/subgraph_wiki' + '.gv', current_subgraph)

path_gediminas_tokens = nltk.word_tokenize(path_gediminas)
current_subgraph = digraph()
for index, term in enumerate(path_gediminas_tokens):
    subgraphgediminas = sentenceNetGediminas.get_connected_subgraph(term)
    current_subgraph = sentenceNetGediminas.get_merged_subgraph(current_subgraph, subgraphgediminas)   
    #sentenceNetGediminas.write_subgraph('./graphs/subgraph_gediminas' + str(index) + '.gv', subgraphgediminas)
SentenceNet.write_subgraph('./graphs/subgraph_gediminas' + '.gv', current_subgraph)

path_ricci_tokens = nltk.word_tokenize(path_ricci)
current_subgraph = digraph()
for index, term in enumerate(path_ricci_tokens):
    subgraphricci = sentenceNetRicci.get_connected_subgraph(term)
    current_subgraph = SentenceNet.merge_graphs(current_subgraph, subgraphricci)   
    #sentenceNetRicci.write_subgraph('./graphs/subgraph_ricci' + str(index) + '.gv', subgraphricci)
SentenceNet.write_subgraph('./graphs/subgraph_ricci' + '.gv', current_subgraph)

path_wikigedi_tokens = nltk.word_tokenize(path_wikigedi)
current_subgraph = digraph()
for index, term in enumerate(path_wikigedi_tokens):
    subgraphwikigedi = sentenceNetWikiGedi.get_connected_subgraph(term)
    current_subgraph = SentenceNet.merge_graphs(current_subgraph, subgraphwikigedi) 
    #sentenceNetWikiGedi.write_subgraph('./graphs/subgraph_wikigedi' + str(index) + '.gv', subgraphwikigedi)
SentenceNet.write_subgraph('./graphs/subgraph_wikigedi' + '.gv', current_subgraph)
