from SentenceNetVisitor import SentenceNetVisitor
from XMLReqManager import XMLReqManager
from SentenceNet import SentenceNet
from irutils.TextFilter import TextFilter


s1 = SentenceNet()
n1 = s1.get_net()
v1 = SentenceNetVisitor(n1, s1.get_edge_start_weight(), s1.get_start_occurrences_num())

xml_doc_handler = XMLReqManager('req_document.xsd', '2007 - eirene fun 7.xml')
req_document = xml_doc_handler.get_requirements_text()

terms_filter = TextFilter()

for sent in req_document:
    filtered_sent = terms_filter.filter_all(sent)
    filtered_sent = terms_filter.remove_item(filtered_sent, "\"")
    filtered_sent = terms_filter.remove_item(filtered_sent, "-")
    print filtered_sent
    v1.search_A_star(filtered_sent)

s1.write_graph("eireneGraph.gv")
