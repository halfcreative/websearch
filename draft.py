#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 13:28:25 2018

@author: nate
"""
from revind import r_index
from crawler_lite import crawler
import collections
import math
import numpy as np
import pickle
import prep
import operator

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
                    domaincrawl.crawl('http://www.'+domain+'.edu',10000)
                    print('creating reverse index...')
                    ri = r_index(domain)
                    ri.make_file()
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
            return
    else:
        with open('dicts/' + domain + '.pkl', 'rb') as f:
            dom_ind = pickle.load(f)
        print('index loaded')
    do = True
    while do:   
        query = input('what we searchin?: ')
        wordsin = prep.prep(query)
        retrieve(wordsin, dom_ind)
        redo = input('want to do it again? (y/n) ')
        if redo == 'n':
            print('Understandable, have a nice day.')
            do = False
        elif redo != 'y':
            redo = input('that was neither "y" nor "n". want to search again? (y/n)' )
        else:
            query = input('what we searchin?: ')
            retrieve(prep.prep(query), dom_ind)
        return
        
def retrieve(q_words, revind):
    q_vec = []
    relevant_docs = []  #harvest all docs that contain any q_words
    for qw in q_words:
        if revind.get(qw) != None:
            for d in revind[qw]:
                if revind[qw]!= 0.0 and d != '<df>' and d != '<total>':
                    relevant_docs.append(d)
            
    doclist = list(set(relevant_docs))
    docveclist = []
    urllist =[]
    for rd in doclist:    #create document vectors
        urllist.append(revind['<urls>'][rd])
        vec = []
        for i in range(len(q_words)):
            if revind.get(q_words[i]) == None:
                revind[q_words[i]] = {}
                revind[q_words[i]][rd] = 0.0
                revind[q_words[i]]['<df>'] = 0.0
                revind[q_words[i]]['<total>'] = 0.0
            elif revind[q_words[i]].get(rd) == None:
                revind[q_words[i]][rd] = 0.0
                revind[q_words[i]]['<df>'] = 0.0
                revind[q_words[i]]['<total>'] = 0.0
            weight = revind[q_words[i]][rd]
            vec.append(weight) # sets the vector to the tf-idf weights as stored in the revese index
        docveclist.append(vec)
    
    freq_info = collections.Counter(q_words)
    max_freq = freq_info.most_common(1)[0][1] #make query vectors
    
    for i in range(len(q_words)): 
        freq_wq = freq_info[q_words[i]]
        if revind.get(q_words[i]) == None:
            q_vec.append(0.0)
        elif revind[q_words[i]]['<df>'] <= 0:
            q_vec.append(0.0)
        else:
            freq_wq = freq_info[q_words[i]]
            q_vec.append(freq_wq * max_freq *math.log10( revind['<total>']/revind[q_words[i]]['<df>'] ))
            
        
    #compute cosine similarities
    cos_similarity = []
    for h in range(len(docveclist)):
        cos_similarity.append(cos_sim(q_vec, docveclist[h]))
    results_w_score = list(zip(urllist,cos_similarity))
    results_w_score.sort(key = operator.itemgetter(1), reverse = True)
    print(cos_similarity)
    
    print('\n\nR E S U L T S:\n')
    count = 0
    result_count = len(results_w_score)
    
    nextpage = 'y'
    while nextpage != 'n':
        for r in range(10):
            count += 1
            if count < result_count:
                print('\t{0} {1}\n'.format(results_w_score[r][1],results_w_score[r][0][11:]))
            else:
                print("That's all the results!")
                nextpage = 'n'
                break
        nextpage = input('another page? press anything but n to see it. ')
    if nextpage == 'n':
        print('ok\n')
        


        
def cos_sim(a,b):
    dp = np.dot(a,b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dp/(norm_a * norm_b)
        
            

main()
