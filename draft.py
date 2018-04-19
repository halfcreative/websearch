#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 13:28:25 2018

@author: nate
"""

def main():
    # load GUI, w input for domain and search term
    # if domain is not on file, ask user if they'd like to make a file.
    # if they would, crawl us a new mf database
    
    domain = input("What domain are we searchin?: ")
    
    try:
        open('{0}/{0}#0'.format(domain), 'r')
    except FileNotFoundError as e:
        print('file does not exist')
        #make directory for this domain
    else:
        print("file exists")
    
    
    
    
main()