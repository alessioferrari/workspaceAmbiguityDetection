'''
Created on 08/feb/2012

@author: ferrari
'''

from xgoogle.search import GoogleSearch, SearchError

class DocumentRetriever(object):
    '''
    This class retrieve the documents from the net, store the textual content of the documents
    in a DomainKnowledgeDocument object. Furthermore, it provides an interface for accessing 
    the textual content of the retrieved documents 
    '''
    documentsURLs= list()


    def __init__(self):
        '''
        Constructor
        '''
    
    def searchDocuments(self, terms):
        '''
        This function search terms in google and store the textual content in DomainKnowledgeDocument objects
        @param terms: list of string terms to be searched through internet
        '''
        try:
            sentence = ' '.join(terms)  
            gs = GoogleSearch(sentence)
            results = gs.get_results()
            for result in results:
                self.documentsURLs.append(result.get_URL())
            print gs.num_results
        
        except SearchError, e:
            print "Search failed: %s" % e
        
    def __parse(self, htmlDocument):
        '''
        the function takes an html document as input, it parses the document
        and returns the textual content of the document
        @param htmlDocument: an HTML formatted document 
        '''
        
    def __store(self, textualContent):
        '''
        the function takes the text of a document and store it in an internal
        object for later retrieval, it returns an ID associated to the document stored
        @param textualContent: the textual content of the document to be stored 
        '''
        
        
d = DocumentRetriever()
d.searchDocuments(['model checking'])