import os
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
import pickle
import prep
import math
#import progressbar
#ripped straight from stackoverflow, 0 shame, 
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
               

        def construct(self):
            if not os.path.exists(self.domain):
                print('domain folder not found')
            else:
                #pb = progressbar.Progressbar('scanning', len(os.listdir(self.domain)),69, 'X' )
                for file in os.listdir(self.domain):
                    self.scan_doc(file)
                    #pb.yep_rand()

        def get(self,w):
            return self.rind.get(w)
                    
        def scan_doc(self, doc):
            try:
                body = open(self.domain+'/'+doc, 'r').read()
            except UnicodeDecodeError as e:
                return
            else:
                self.totaldocs += 1
                regex = re.compile(r'^(URL)\[(.*)\]')
                thing = regex.search(body)
                if thing == None:
                    url = 'URL NOT FOUND'
                else:
                    url = thing.group(2)
                self.doc2url[doc] = url
                text = text_from_html(body)
                words = prep.prep(text)
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

                                
        def finalize(self): #does the math, then stores the index as a .pkl file
            for w in self.d.keys():
                idf = math.log10(self.totaldocs/self.d[w]['<df>'])
                for doc in self.d[w]:
                    self.rind['<urldict>'] = self.doc2url
                    if w not in self.rind.keys():
                        self.rind[w] = {}
                    self.rind[w][doc] = 0.0
                    tf = self.d[w][doc]
                    self.rind[w][doc] = tf*idf
                self.rind[w]['<df>'] = self.d[w]['<df>']
                self.rind['<total>'] = self.totaldocs
            with open('dicts/'+ self.domain + '.pkl', 'wb') as f:
                pickle.dump(self.rind, f, pickle.HIGHEST_PROTOCOL)
            print("it is done.")

        def toString(self):
            out = 'WORDS:\n'
            for word in self.d.keys():
                out += '{0}\n'.format(word)
                for doc in self.d[word]:
                    out += '\tdoc: {0} count: {1}\n'.format(doc, self.d[word][doc])
            return out
