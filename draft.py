#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 13:28:25 2018

@author: nate
"""
from revind import r_index
import crawler_lite

def main():
    # load GUI, w input for domain and search term
    # if domain is not on file, ask user if they'd like to make a file.
    # if they would, crawl us a new mf database
    
    domain = input("What domain are we searchin?: ")
    
    try:
        open('{0}/{0}page#0.txt'.format(domain), 'r')
    except FileNotFoundError as e:
        decide = input('data does not exist, make new folder? (y/n)')
        if decide == 'y':#make directory for this domain
            domaincrawl = crawler_lite.crawler()
            domaincrawl.crawl(domain)
        else:
            print('no problem, ending program!')
    else:
        print('creating reverse index...')
        ri = r_index(domain)
        print(ri.toString())
        
    
    
    
    
main()
