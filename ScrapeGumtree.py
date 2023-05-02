import requests
import json
from bs4 import BeautifulSoup
import re
gumtreeFinal=[]
url=''
titles=[]
descriptions=[]
locations=[]
prices=[]
links=[]
file=open("wintrKey.json","r")
apikey=file.read()    
def getGumtree(supply,demand):
    global gumtreeFinal
    global url
    global titles
    global descriptions
    global locations
    global prices
    global links
    global apikey
    defaults=[]
    file=open("DefaultSearches.txt","r")
    for line in file:
        defaults.append(line.replace("\n",""))
    if supply == 1:
        url =defaults[2]
    if demand==1:
        url=defaults[3]
    req = requests.post('https://api.wintr.com/fetch', data = json.dumps({
    'url': url,
    'apikey': apikey,
    'countrycodes': ['uk']
    }), headers = {
    'content-type': 'application/json',
    'accept': 'text/plain'
    })    
    content = json.loads(req.content)
    file=open("HTMLRESULT.txt","w")
    file.write(str(content))
    file=open("HTMLRESULT.txt","r")
    data=file.read()
    soup=BeautifulSoup(data,"html.parser")
    soup=soup.find_all("li", {"class": "natural"})
    begin=[m.start() for m in re.finditer('class="listing-title">', str(soup))]
    end=[m.start() for m in re.finditer('div class="listing-location"', str(soup))]
    for i in range (1,len(begin)):
        titles.append(str(soup)[begin[i]+24:(end[i]-10)])
    begin=[m.start() for m in re.finditer('data-toggler="channel:toggleDescription0,selfBroadcast:false">', str(soup))]
    end=[m.start() for m in re.finditer('<ul class="listing-attributes', str(soup))]
    for i in range (1,len(begin)):
        descriptions.append((str(soup)[begin[i]+64:(end[i]-8)]))
    begin=[m.start() for m in re.finditer('span class="truncate-line">', str(soup))]
    end=[m.start() for m in re.finditer('<p class="listing-description txt-sub txt-tertiary', str(soup))]
    for i in range (1,len(begin)):
        locations.append((str(soup)[begin[i]+29:(end[i]-19)]))
    begin=[m.start() for m in re.finditer('class="h3-responsive">', str(soup))]
    end=[m.start() for m in re.finditer('<span class="txt-tertiary txt-micro', str(soup))]
    for i in range (1,len(begin)):
        prices.append((str(soup)[begin[i]+22:(end[i]-11)]))

    begin=[m.start() for m in re.finditer('href="/p/', str(soup))]
    end=[m.start() for m in re.finditer('class="listing-side', str(soup))]
    for i in range (1,len(begin)):
        links.append("www.gumtree.com"+(str(soup)[begin[i]+6:(end[i]-30)]))
    if supply == 1:
        url=url.replace('1', '2', 1)
        getGumtree1(2,0)
        url=url.replace('2', '3', 1)
        getGumtree1(3,0)
        url=url=url.replace('3', '4', 1)
        getGumtree1(0,0)
    packArray(supply,demand)
    return gumtreeFinal
def getGumtree1(supply,demand):
    global gumtreeFinal
    global url
    global titles
    global descriptions
    global locations
    global prices
    global links
    global apikey
    req = requests.post('https://api.wintr.com/fetch', data = json.dumps({
    'url': url,
    'apikey': apikey,
    'countrycodes': ['uk']
    }), headers = {
    'content-type': 'application/json',
    'accept': 'text/plain'
    })    
    content = json.loads(req.content)
    file=open("HTMLRESULT.txt","w")
    file.write(str(content))
    file=open("HTMLRESULT.txt","r")
    data=file.read()
    soup=BeautifulSoup(data,"html.parser")
    soup=soup.find_all("li", {"class": "natural"})
    begin=[m.start() for m in re.finditer('class="listing-title">', str(soup))]
    end=[m.start() for m in re.finditer('div class="listing-location"', str(soup))]
    for i in range (1,len(begin)):
        titles.append(str(soup)[begin[i]+24:(end[i]-10)])
    begin=[m.start() for m in re.finditer('data-toggler="channel:toggleDescription0,selfBroadcast:false">', str(soup))]
    end=[m.start() for m in re.finditer('<ul class="listing-attributes', str(soup))]
    for i in range (1,len(begin)):
        descriptions.append((str(soup)[begin[i]+64:(end[i]-8)]))
    begin=[m.start() for m in re.finditer('span class="truncate-line">', str(soup))]
    end=[m.start() for m in re.finditer('<p class="listing-description txt-sub txt-tertiary', str(soup))]
    for i in range (1,len(begin)):
        locations.append((str(soup)[begin[i]+29:(end[i]-19)]))
    begin=[m.start() for m in re.finditer('class="h3-responsive">', str(soup))]
    end=[m.start() for m in re.finditer('<span class="txt-tertiary txt-micro', str(soup))]
    for i in range (1,len(begin)):
        prices.append((str(soup)[begin[i]+22:(end[i]-11)]))

    begin=[m.start() for m in re.finditer('href="/p/', str(soup))]
    end=[m.start() for m in re.finditer('class="listing-side', str(soup))]
    for i in range (1,len(begin)):
        links.append("www.gumtree.com"+(str(soup)[begin[i]+6:(end[i]-30)]))

def packArray(supply,demand):
    global gumtreeFinal
    global url
    global titles
    global descriptions
    global locations
    global prices
    global links
    if demand == 1:
        prices=[]
        for i in range (0,len(titles)):
            prices.append("")
    for i in range (0,len(titles)):
        gumtreeFinal.append(["Gumtree",titles[i],descriptions[i],locations[i],prices[i],links[i]])
