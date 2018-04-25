class r_index:
        def __init__():
                self.d = {}
        def scan_doc(self, doc):
                text = open(doc, 'r').read()
                words = preprocess(text)
                for w in words:
                        if word not in d.keys:
                                d[word] = {}
                        if doc not in d[word].keys:
                                d[word][doc] = 1
                        else:
                                d[word][doc] += 1








