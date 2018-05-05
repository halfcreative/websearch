#!/usr/bin/python3

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
                open('dicts/{0}.pkt'.format(baseurl))
            except FileNotFoundError as e0:
                #rev index doesnt exist, check for crawled files
                try:
                    open('{0}/{0}page#0.txt'.format(baseurl),'r')
                except FileNotFoundError as e1:
                    #crawled files dont exist: crawl!
                    crwl = crawler()
                    crwl.crawl(fullDomain,100)
                    ri = r_index(baseurl)
                    ri.make_file()
                else:
                    ri = r_index(baseurl)
                    ri.make_file()
                    #Crawler files exist!
            else:
                #Reverse Index found!
                ri = r_index(baseurl)
                ri.make_file()
                
root = tk.Tk()
root.geometry('300x400')
MainWindow(root).pack()
root.mainloop()

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

