class r_index:
        def __init__():
               d = {}
        def scan_doc(self, doc):
                text = open(doc, 'r').read()
                words = preprocess(text)
                for w in words:
                        if w not in self.d.keys:
                                self.d[w] = {}
                        if doc not in self.d[w].keys:
                                self.d[w][doc] = 1
                        else:
                                self.d[w][doc] += 1








