#!/usr/bin/python3
import tkinter as tk
class MainWindow(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        label1 = tk.Label(self,text="Domain to search")
        label1.pack()

        defaultDomain = tk.StringVar()
        defaultDomain.set("http://www.muhlenberg.edu")
        
        fullDomain = tk.Entry(self,textvariable=defaultDomain,width=30)
        fullDomain.pack()

        label2 = tk.Label(self,text="Terms to search for")
        label2.pack()
        searchterms = tk.Entry(self,width=30)
        searchterms.pack()
        searchbutton = tk.Button(self,command = self.searchDom)
        return
    def searchDom():
        return

root = tk.Tk()
root.geometry('300x400')
MainWindow(root).pack()
root.mainloop()
