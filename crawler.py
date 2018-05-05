#! /usr/bin/python3
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import os
import re


# Sam's First WebCrawler... IMPROVED to version 2
## INTRO:
## Welcome to the crawler! I made this for my AI class
## The crawler has 1 function that takes a URL to crawl
## It will make 1 text file for each page visited.
## ^This project was repurposed for the Search Engine^
## In each text file, the top will have the URL of the page visited, the number of relative links on the site, and the number of absolute links on the site
##      In addition, the HTML contents will be included.
## For Extra Credit:
##      Phone Number finding
##      Finds Names


#CHANGELOG
#---------
#4/16/2018-2.4
#2.4:
#-Renamed file
#-Prepared for use in search engine
#4/10/2018-2.3
#2.3:
#-Added name finding regex
#---------
#4/7/2018-2.2
#2.2:
#-Started Extra Credit:
#       -Added Phone number regex
#---------
#4/6/2018-2.1.1
#2.1.1:
#-Added Limiter
#---------
#4/3/2018-Update to v2.1
#2.1:
#-Stopped visiting unneccesary stuff(pdf's ppts etc)
#-Some cleaning up of the code
#-Added tasks
#---------
#4/1/2018-Created Version2
#2.0:
#-Switch from recursive to iterative. Recursive returned error
#---------

#To-Do:
#--Added other Regular Expressions to find additonal information, in order to gain extra credit
#################################################


#######################################
#             Debugging               #
#######################################
DEBUG = True

def log(n):
    if DEBUG == True:
        print(n)
#######################################

class crawler():
    def __init__(self):
        self.baseurl = ""
        self.baseurlbegin = ""
        self.baseurlend = ""
        self.visited = dict() # ALL VISITED LINKS INCLUDING NON-HTML Links
        self.tovisit = [] # LINKS on the list to visit
        self.filesmade = 0
        self.linksfound = 0
        self.rellinksfound = 0
        self.abslinksfound = 0
        self.phones = []
        self.nameslist = [] # list of names with titles found (ie Dr. Mr. Mrs. John Smith)
        return
    #Crawl will have the crawler find every link on the page, store the ones not visited in a list, then visit each page on the domain
    def crawl(self,site,limit=0):
        if limit==0:
            limited = False
            print("Crawling Full site")
        else:
            limited = True
            print("Crawing {0} pages".format(limit))
        #Sets a baseurl that can be compared to and adds the first URL on the list of places to visit
        self.baseurl = site
        self.tovisit.append(site)
        #Regular Expressions to parse page. Only want/need to make these objects once.
        #regex - a regular expression to parse the base URL for the name and extension ie muhlenberg and .edu
        regex = re.compile(r'https?:\/\/(www\.)?(.+)\.(.+)$')
        self.baseurlbegin = regex.match(self.baseurl).group(2) # for baseurl https://www.muhlenberg.edu this returns "muhlenberg"
        self.baseurlend = regex.match(self.baseurl).group(3)# for baseurl https://www.muhlenberg.edu this returns "edu"
        #regex1 - All links, as marked by href
        regex1 = re.compile(r'href=[\'"]?([^\'" >]+)')
        #regex2 - All relative links
        regex2 = re.compile(r'^\/.+[^pdf|css|pptx?|docx?|png|jpeg|gif]$')
        #regex3 - absolute links to the baseurl
        regex3 = re.compile(r'https?:\/\/(www\.)?'+self.baseurlbegin+'\.'+self.baseurlend+'(.+[^pdf|css|pptx?|docx?|png|jpeg|gif])$')
        #regex3_5 - absolute links to the baseurl
        regex3_5 = re.compile(r'https?:\/\/(www\.)?(.+)(.+[^pdf|css|pptx?|docx?|png|jpeg|gif])$')
        #regex4 - Phone Numbers
        #regex4 = re.compile(r'\([0-9]{3}\)|[0-9]{3}[-,.\s]?[0-9]{3}[-,.\s]?[0-9]{4}')
        #regex5 - First and Last names w/ Title (?)
        #regex5 = re.compile(r'(Dr\.|Mr\.|Mrs\.|Ms\.).?([A-Z]\w+)\s([A-Z]\w+).(.+Professor)?')
        #Heres where the actual crawiling starts!
        while len(self.tovisit) > 0:
            visiting = self.tovisit.pop(0)
            log("Going to {0}".format(visiting))
            #make a request object with the 'visiting' link and a header.
            #the header is not super necessary, but I was getting 403 errors and this was a suggested solution
            req = Request(visiting,headers={'User-Agent': 'Mozilla/5.0'}) 
            try:
                #Try to make a page request
                pagereq = urlopen(req)
            except HTTPError as e:
                log("Page {0} returned error {1}".format(visiting,e))
                self.visited[visiting] = 1
            else:
                #Page Request successful! read the page request as bytes
                bytepage = pagereq.read()
                try:
                    #Try to decode the bytepage in utf-8, this will only work if its a css or html page
                    page = bytepage.decode('utf-8')
                except UnicodeDecodeError as err:
                    log("link {0} returned {1} : probably because its not a page but a pdf or something".format(visiting,err))
                else:
                    #THE PAGE WAS DECODED!
                    #names = regex5.findall(page)
                    #for name in names:
                    #    tmpname = name[0] + name[1] + " " + name[2]
                    #    if tmpname not in self.nameslist:
                    #        self.nameslist.append(tmpname)
                    #Find Phone numbers
                    #phone_nums = regex4.findall(page)
                    #for number in phone_nums:
                    #    if not any(number in records for records in self.phones):
                    #        self.phones.append((number,visiting))
                    #Find Links:
                    #create initial list of links and make a filter list of all the links with slash
                    links = regex1.findall(page)
                    linksrel = list(filter(regex2.match,links))
                    linksabs = [m.group(2) for m in (regex3.match(a) for a in links) if m] #creates a list of the absolute links for this domain
                    #alllinksabs = [m.group(0) for m in (regex3_5.match(a) for a in links) if m] #creates a list of all absolute links
                    #Make Page and Add to visit:
                    #self.makepage(self.filesmade,visiting,len(linksrel),len(alllinksabs),page)
                    self.makepage(self.filesmade,visiting,page)
                    self.visited.update(visiting=1)
                    #End the program if the number of files made would exceed the limit
                    if limited and self.filesmade >= limit:
                        print("Reached specified limit:{0}".format(limit))
                        break
                    #Continue to search for links
                    for i in range(len(linksrel)):     
                        check = self.baseurl + linksrel[i] #relative links + base url for an absolute link
                        if check not in self.visited and check not in self.tovisit :
                            self.tovisit.append(check)
                            #log("adding {0} to visit".format(check))
                            self.linksfound += 1
                            self.rellinksfound += 1
                    #Add absolute links to tovisit if its not been visited or its not already on the list 
                    for j in range(len(linksabs)):     
                        check = self.baseurl + linksabs[j] #relative links + base url for an absolute link
                        if check not in self.visited and check not in self.tovisit :
                            self.tovisit.append(check)
                            log("adding {0} to visit".format(check))
                            self.linksfound +=1
                            self.abslinksfound += 1
        print("Finished Crawling\nCrawler found and recorded {0} pages on {1}".format(self.filesmade,site))
        print("There were {0} unique links, {1} of them relative and {2} of them absolute".format(self.linksfound,self.rellinksfound,self.abslinksfound))
        print("Found {0} phone numbers".format(len(self.phones)))
        print(self.phones)
        print("Found {0} names with titles".format(len(self.nameslist)))
        print(self.nameslist)
    #Makes page with the order visited, the number of links relative and absolute and the content of the html
    def makepage(self,num,site,content):
        if not os.path.exists(self.baseurlbegin):
            os.makedirs(self.baseurlbegin)
            print("Folder did not exist making Folder")
        else:
            pass
        title = self.baseurlbegin + "/" + self.baseurlbegin + "page#" + str(num) + ".txt"
        page = open(title,'w+')
        self.filesmade +=1
        page.write("URL[{0}]".format(site))
        page.write(content)
        page.close()
#main function to test
#def main():
#    webby = crawler()
#    webby.crawl("http://www.muhlenberg.edu",100)
#main()
