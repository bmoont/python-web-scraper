# python-web-scraper
Searches Twitter and Gumtree for required information. Currently set up to search for office space.

You will need the required keys to be able to use this to its full potential. These are saved as .json files. The keys are:

creds.json = Google Sheets Keys to save results

TCreds.json = Twitter API keys

wintrKey.json = Wintr API keys

You can change the output spreadsheet in the writeSheets.py file and the search terms in the settings of the GUI.

Required libraries are twitter, geopy, tkinter, re, sys, os, requests, json, BeautifulSoup, pygsheets, pandas.
