import pygsheets
import json
import os
import pandas as pd  
path1=os.path.abspath("creds.json").replace('\\',"/")
gc = pygsheets.authorize(service_file=path1[2:])

def write(twodData,date,site,supply,demand):
    addtoName=2
    if len(twodData) == 0:
        exit
    if supply == 1:
        sheetName="Supply"
    if demand == 1:
        sheetName="Demand"
    sh = gc.open(sheetName)
    try:
        wks = sh.add_worksheet(twodData[0][0][0]+"-"+str(date),rows=100,cols=6)
    except:
        while True:
            try:
                wks = sh.add_worksheet(twodData[0][0][0]+"-"+str(date)+"- V"+str(addtoName),rows=100,cols=6)
                break
            except:
                addtoName+=1
            
    if site == "T":
        df = pd.DataFrame(twodData, columns =["Site","Handle","Tweet","Link","Date and Time","Location"]) 

    elif site == "G":
        df = pd.DataFrame(twodData, columns =["Site","Title","Description","Location","Prices","Link"]) 
   
    wks.set_dataframe(df, (1, 1))
    
