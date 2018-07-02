# Search Engine
This is a search engine, written in python

When given a domain and a search term, the search engine will produce the 5 most relavent links to that term within that domain.
The Search Engine has 5 parts:

Crawler
  -Gathers files from a domain
Pre-Processor
  -Takes the files from the crawler, and cleans them to be analyzed
Reverse Index
  -Takes key terms and files them in a revese index
Search (weights added)
  -Adds weights to terms for relavency
GUI
  -the face of the project
