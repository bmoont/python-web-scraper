import twitter
from  geopy.geocoders import Nominatim
creds=[]
file=open("TCreds.json","r")
for line in file:
    creds.append(line.replace("\n",""))

api = twitter.Api(consumer_key=creds[0],
                  consumer_secret=creds[1],
                  access_token_key=creds[2],
                  access_token_secret=creds[3])

def fetchdata(supply,demand,location,date):
    #call on functions to find the exact terms needed to perform a search with the given parameters
    tweetsArray=[]
    finalDate=convertDate(date)
    searchTerm=what2Search(supply,demand)
    locationArray=longLat(location)
    if locationArray == False:
        tweets=api.GetSearch(term=searchTerm,count=50,since=finalDate,result_type="recent")
    else:
        tweets=api.GetSearch(term=searchTerm,count=50,since=finalDate,geocode=locationArray,result_type="recent")
    for i in range (0,len(tweets)):
        tweetsArray.append(["Twitter","@"+str(tweets[i].user.screen_name),tweets[i].text,"https://twitter.com/user/status/"+str(tweets[i].id),tweets[i].created_at,tweets[i].user.location])
    if len(tweetsArray)==0:
        return "popup"
    return tweetsArray
def convertDate(date):
    newDate=date[6:]+"-"+date[3:5]+"-"+date[0:2]
    return newDate
def what2Search(supply,demand):
    defaults=[]
    file=open("DefaultSearches.txt","r")
    for line in file:
        defaults.append(line.replace("\n",""))
    if supply==1:
        return defaults[0]
    elif demand ==1:
        return defaults[1]
def longLat(location):
    if location == "":
        return False
    locationInputs=[]
    geolocator = Nominatim(user_agent="Ofixu")
    loc=geolocator.geocode(location)
    locationInputs.append(loc.latitude)
    locationInputs.append(loc.longitude)
    locationInputs.append("15km")
    return locationInputs
