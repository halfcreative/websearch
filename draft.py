#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 13:28:25 2018

@author: nate
"""
from revind import r_index
from crawler import crawler
import collections
import math
import pickle
import prep

def main():
    # load GUI, w input for domain and search term
    # if domain is not on file, ask user if they'd like to make a file.
    # if they would, crawl us a new mf database
    
    domain = input("What domain are we searchin?: ")
    try:
        open('dicts/{0}.pkl'.format(domain), 'r')
    except FileNotFoundError as e0:
        choice0 = input('reverse index file does not exist, make file? (y/n) ')
        if choice0 == 'y':
            try:
                open('{0}/{0}page#0.txt'.format(domain), 'r')
            except FileNotFoundError as e:
                decide = input('data does not exist, make new folder? (y/n) ')
                if decide == 'y':#make directory for this domain
                    domaincrawl = crawler()
                    domaincrawl.crawl('http://www.'+domain+'.edu',100)
                    print('creating reverse index...')
                    ri = r_index(domain)
                    ri.make_file()
                    print(ri.toString())
                    if 'javascript' in ri.d.keys():
                        print('its not filtering out javascript yet')
                    else:
                        print('no problem, ending program!')
            else:
                print('creating reverse index...')
                ri = r_index(domain)
                #print(ri.toString())
                with open('dicts/' + domain + '.pkl', 'rb') as f:
                    dom_ind = pickle.load(f)
                if 'javascript' in ri.d.keys():
                    print('its not filtering out javascript yet')
                    
        else: 
            print('no worries, come back another time.')
    else:
        with open('dicts/' + domain + '.pkl', 'rb') as f:
            dom_ind = pickle.load(f)
        print('index loaded')

    query = input('what we searchin?: ')
    wordsin = prep.prep(query)
    retrieve(wordsin, dom_ind)
    
def retrieve(q_words, revind):
    print(revind['<total>'])
    q_vec = []
    relevant_docs = []  #harvest all docs that contain any q_words
    for qw in q_words:
        for d in revind[qw]:
            print("{0} : {1}".format(d,revind[qw][d]))
            if revind[qw]!= 0.0:
                relevant_docs.append(d)
            
    doclist = list(set(relevant_docs))
    docveclist = []
    for rd in doclist:    #create document vectors
        vec = []
        for i in range(len(q_words)):
            if revind[q_words[i]].get(rd) == None:
                weight = 0.0
            else:
                weight = revind[q_words[i]][rd]
            vec.append(weight) # sets the vector to the tf-idf weights as stored in the revese index
        docveclist.append(vec)
    
    freq_info = collections.Counter(q_words)
    max_freq = freq_info.most_common(1)[0][1]
    for i in range(len(q_words)): #make query vectors
        freq_wq = freq_info[q_words[i]]
        if revind[q_words[i]]['<df>'] <= 0:
            q_vec.append(0.0)
        else:
            q_vec.append(freq_wq * max_freq *math.log10( revind['<total>']/revind[q_words[i]]['<df>'] ))
        # freq of word in q / freq of most freq word in q *math.log10(total num of docs/# of docs w/ word)
        
            
    print('query vector: {0}\ndocument vectors:'.format(q_vec))
    for d in range(len(docveclist)):
        print(docveclist[d])
    print(q_vec)
main()
