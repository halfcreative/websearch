#!/usr/bin/python3
import search
from revind import r_index
from crawler import crawler
import re
import collections
import math
import numpy as np
import pickle
import prep
import operator
import tkinter as tk
import os

class MainWindow(tk.Frame):

    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.label1 = tk.Label(self,text="Domain to search")
        self.label1.pack()

        self.defaultDomain = tk.StringVar()
        self.defaultDomain.set("http://www.muhlenberg.edu")
        
        self.fullDomainbox = tk.Entry(self,textvariable=self.defaultDomain,width=30)
        self.fullDomainbox.pack()

        self.label2 = tk.Label(self,text="Terms to search for")
        self.label2.pack()
        self.searchtermsbox = tk.Entry(self,width=30)
        self.searchtermsbox.pack()
        self.searchbutton = tk.Button(self,command = self.searchDom,text="Search!")
        self.searchbutton.pack()

    def searchDom(self):
        fullDomain = self.fullDomainbox.get()
        searchterms = self.searchtermsbox.get()
        if searchterms == '':
            print("no search term")
        else:
            searchterms = prep.prep(searchterms)
            print("The button was pressed! Requesting a search for {0} on {1}".format(searchterms,fullDomain))
            #Have both a domain and a search term.
            #Check if folder for the domain exists
            regex = re.compile(r'https?:\/\/(www\.)?(.+)\.(.+)$')
            baseurl = regex.match(fullDomain).group(2) # for baseurl https://www.muhlenberg.edu this returns "muhlenberg"
            if not os.path.exists(baseurl):
                #make directory for the url if it doesnt
                print("Folder did not exist making Folder")
                os.makedirs(baseurl)
            #Try to open a reverse index
            if not os.path.exists('dicts'):
                os.makedirs('dicts')
            try:
                with open('dicts/' + baseurl + '.pkl', 'rb') as f:
                    ri = pickle.load(f)
            except FileNotFoundError as e0:
                #rev index doesnt exist, check for crawled files
                try:
                    open('{0}/{0}page#0.txt'.format(baseurl),'r')
                except FileNotFoundError as e1:
                    #crawled files dont exist: crawl!
                    crwl = crawler()
                    crwl.crawl(fullDomain,100)
                    ri = r_index(baseurl)
                    search.retrieve(searchterms,ri)
                else:
                    ri = r_index(baseurl)
                    #Crawler files exist!
        search.retrieve(searchterms,ri)
                
root = tk.Tk()
root.geometry('300x400')
MainWindow(root).pack()
root.mainloop()
