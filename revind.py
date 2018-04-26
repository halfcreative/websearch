import os

class r_index:
        def __init__(self, dom):
               self.d = {}
               self.domain = dom
               self.construct()

        def construct(self):
            if not os.path.exists(self.domain):
                print('domain folder not found')
            else:
                for file in os.listdir(self.domain):
                    self.scan_doc(file)
                    
        def scan_doc(self, doc):
                text = open(self.domain+'/'+doc, 'r').read()
                words = text.split()
                for w in words:
                        if w not in self.d.keys():
                                self.d[w] = {}
                        if doc not in self.d[w].keys():
                                self.d[w][doc] = 1
                        else:
                                self.d[w][doc] += 1
                                
        def toString(self):
            out = 'WORDS:\n'
            for word in self.d.keys():
                out += '{0}\n'.format(word)
                for doc in self.d[word]:
                    out += '\tdoc: {0} count: {1}\n'.format(doc, self.d[word][doc])
            return out