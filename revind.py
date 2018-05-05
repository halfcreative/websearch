#Nate Levy, Alan Sato
#reverse-index-generator and exporter that accesses a corpus of html pages sotred as .txt files

import os
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
import pickle
import prep
import math
import progressbar

#the following two funtions were accessed through stackoverflow, they still include javascript but 
#everything we've tried to circumvent that has failed.
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')    
    #this is supposed to filter out script, but does no such thing.
    for script in soup.find_all('script', src=False):
        script.decompose()    # rip it out
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    strout = u" ".join(t.strip() for t in visible_texts)
    strout = re.sub(r'<[^>]*?>', '', strout)
    return strout


class r_index:
        def __init__(self, dom):
               self.d = {}
               self.domain = dom
               self.totaldocs = 0.0
               self.rind = {}
               self.doc2url = {}
               self.rind['<total>'] = 0.0
               self.construct()
               self.finalize()
               
        #go through the folder of html text documents and scan them
        def construct(self):
            if not os.path.exists(self.domain):
                print('domain folder not found')
            else:
                #make a reverse index
                pb = progressbar.Progressbar('scanning', len(os.listdir(self.domain)),69, 'X' )
                for file in os.listdir(self.domain):
                    self.scan_doc(file)
                    pb.yep_rand()
                    
        def scan_doc(self, doc):
            #sometimes it would hit us with one of these, so we added this so it wouldn't
            try:
                body = open(self.domain+'/'+doc, 'r').read()
            except UnicodeDecodeError as e:
                return
            else:
                self.totaldocs += 1
                #extract url from document
                thing = re.search(r'URL:(.*)\n', body)
                if thing == None:
                    url = 'URL NOT FOUND'
                else:
                    url = thing.group(1)
                self.doc2url[doc] = url
                #get actual displayed text, uses beautifulsoup, we never got it working nearly as well without it, sorry
                text = text_from_html(body)
                words = prep.prep(text)
                #get all those juicy words crammed into our dictionary for safekeeping and eventual analysis
                for w in words:
                    if w not in self.d.keys():
                        self.d[w] = {}
                        self.d[w]['<total>'] = 1.0
                        self.d[w]['<df>'] = 1.0
                        self.d[w][doc] = 1.0
                    elif doc not in self.d[w].keys():
                        self.d[w][doc] = 1.0
                        self.d[w]['<total>'] += 1.0
                        self.d[w]['<df>'] += 1.0
                    else:
                        self.d[w][doc] +=1.0
                        self.d[w]['<total>'] += 1.0

        #does all the math, then stores a more streamlined dictionary-based
        #reverse-index implementation as a .pkl file
        def finalize(self):
            for w in self.d.keys():
                idf = math.log10(self.totaldocs/self.d[w]['<df>'])
                for doc in self.d[w]:
                    #don't forget the url's!
                    self.rind['<urldict>'] = self.doc2url
                    if w not in self.rind.keys():
                        self.rind[w] = {}
                    #initialize dicitonary for word/document combo
                    self.rind[w][doc] = 0.0
                    #puts the tf idf in there
                    tf = self.d[w][doc]
                    self.rind[w][doc] = tf*idf
                #store corpus-dependant data
                self.rind[w]['<df>'] = self.d[w]['<df>']
                self.rind['<total>'] = self.totaldocs
            #create .pkl file of self.rind
            with open('dicts/'+ self.domain + '.pkl', 'wb') as f:
                pickle.dump(self.rind, f, pickle.HIGHEST_PROTOCOL)
            print("it is done.") #forsooth.

        #exactly what you'd expect
        def toString(self):
            out = 'WORDS:\n'
            for word in self.d.keys():
                out += '{0}\n'.format(word)
                for doc in self.d[word]:
                    out += '\tdoc: {0} count: {1}\n'.format(doc, self.d[word][doc])
            return out
