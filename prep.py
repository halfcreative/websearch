#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
swList = open('sw.txt', 'r').read()
swFilter = True
stem = True

def prep(str):
    str = re.sub(r'[^\w\'\s]', '', str)
    words = str.lower().split()
    
    if swFilter:
        for i in range(len(words)):
            if words[i] in swList:
               words[i] = '<sw>'
               
    words = list(filter(lambda x: x != '<sw>', words))

    if stem:
        for i in range(len(words)):
            words[i] = stem(words[i])

    return words

def stem(word): #still 100% trash, but no need for premature optimizaition
    #suffix-stripping:
    word = re.sub(r's$', '', word)
    word = re.sub(r'ed$', '', word)
    word = re.sub(r'i?ly$', '', word)
    word = re.sub(r'ing$', '', word)
    word = re.sub(r"\'\w*$", '', word) #an apostrophe and anything after it
    return word