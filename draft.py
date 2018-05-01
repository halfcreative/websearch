#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 13:28:25 2018

@author: nate
"""
from revind import r_index
from crawler_lite import crawler
import pickle

def main():
    # load GUI, w input for domain and search term
    # if domain is not on file, ask user if they'd like to make a file.
    # if they would, crawl us a new mf database
    
    domain = input("What domain are we searchin?: ")
    try:
        open('dicts/{0}.pkl'.format(domain), 'r')
    except FileNotFoundError as e0:
        choice0 = input('reverse index file does not exist, make file? (y/n)')
        if choice0 == 'y':
            
            try:
                open('{0}/{0}page#0.txt'.format(domain), 'r')
            except FileNotFoundError as e:
                decide = input('data does not exist, make new folder? (y/n)')
                if decide == 'y':#make directory for this domain
                    domaincrawl = crawler()
                    domaincrawl.crawl(domain)
                else:
                    print('no problem, ending program!')
            else:
                print('creating reverse index...')
                ri = r_index(domain)
                ri.make_file()
                print(ri.toString())
                if 'javascript' in ri.d.keys():
                    print('its not filtering out javascript yet')
                    
        else: 
            print('no worries, come back another time.')
    else:
        with open('dicts/' + domain + '.pkl', 'rb') as f:
            dom_ind = pickle.load(f)
        print('index loaded')

    query = input('what we searchin?')
    
        
main()
