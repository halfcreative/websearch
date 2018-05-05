#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  4 03:30:06 2018

@author: nate
"""
import random
import string


class Progressbar:
    def __init__(self, title, max_count, res, block_char):
        self.max = max_count #the number that is the bar's goal
        self.bars = res
        self.block = block_char
        self.mod = self.max / self.bars
        if len(title) < res-4:
            self.topbar = ('{0}...{1}v'.format(title, ' ' * (res-len(title)-4)))
        elif len(title) < res-1:
            self.topbar = ('{0}{1}v'.format(title, ' ' * (res-len(title)-1)))
        else:
            self.topbar = (title+'...\n'+(' ' * (res-1)) + 'v') #this is probably not gonna work right
        self.currcount = 0
        self.barcts = []
        for i in range(self.bars):
            num = int(i * self.max / self.bars)
            self.barcts.append(num)
        self.barcts.append(self.max)
        print(self.topbar)
        
    def yep(self):
        self.currcount += 1
        if self.currcount in self.barcts:
            print(self.block,end = '')
            
    def yep_rand(self):
        char = random.choice(string.printable)
        while char == ' ' or char == '\n' or char == '\t':
            char = random.choice(string.printable)
        self.currcount += 1
        if self.currcount in self.barcts:
            print(char, end ='')
            