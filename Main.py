import tkinter as tk
from tkinter import ttk
import re
import APITwitter
import sys
import writeSheets
import ScrapeGumtree
import os
#create window
root=tk.Tk()
root.title('PropSearch V1.0')
siteTickGumtree = tk.IntVar()
siteTickTwitter = tk.IntVar()
warnedLocation=False
supply=tk.IntVar()
demand=tk.IntVar()
click_btn=tk.PhotoImage(file="settings.gif")
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=os.path.abspath("logo.png")))
def settings():
    defaults=[]
    file=open("DefaultSearches.txt","r")
    for line in file:
        defaults.append(line.replace("\n",""))
    settingsPage = tk.Tk()
    settingsPage.wm_title("Settings")
    label = tk.Label(settingsPage, text="Settings\nThis allows you to change the\nsearch terms or URL used to gather the data.", font=("Helvetica", 10))
    label.grid(row="0",column="1")
    tSupplyLabel=tk.Label(settingsPage, text="Twitter Supply Search Term")
    tSupplyLabel.grid(row="1",column="0")
    tDemandLabel=tk.Label(settingsPage, text="Twitter Demand Search Term ")
    tDemandLabel.grid(row="1",column="2")
    twitterSupply=tk.Entry(settingsPage)
    twitterSupply.grid(row="2",column="0")
    twitterSupply.insert(0, defaults[0])
    twitterDemand=tk.Entry(settingsPage)
    twitterDemand.grid(row="2",column="2")
    twitterDemand.insert(0, defaults[1])
    space1=tk.Label(settingsPage,text="      ")
    space1.grid(row="3",column="1")
    gSupplyLabel=tk.Label(settingsPage, text="Gumtree Supply URL ")
    gSupplyLabel.grid(row="4",column="0")
    gDemandLabel=tk.Label(settingsPage, text="Gumtree Demand URL ")
    gDemandLabel.grid(row="4",column="2")
    gumtreeSupply=tk.Entry(settingsPage)
    gumtreeSupply.grid(row="5",column="0")
    gumtreeSupply.insert(0, defaults[2])
    gumtreeDemand=tk.Entry(settingsPage)
    gumtreeDemand.grid(row="5",column="2")
    gumtreeDemand.insert(0, defaults[3])
    space2=tk.Label(settingsPage,text="      ")
    space2.grid(row="6",column="1")
    B1 = tk.Button(settingsPage, text="SAVE", command = lambda:save(twitterSupply.get(),twitterDemand.get(),gumtreeSupply.get(),gumtreeDemand.get()))
    B1.grid(row="7",column="1")
    space3=tk.Label(settingsPage,text="      ")
    space3.grid(row="8",column="1")
    B2 = tk.Button(settingsPage, text="RESET TO DEFAULT", command = lambda:default1(settingsPage))
    B2.grid(row="9",column="1")
    space4=tk.Label(settingsPage,text="      ")
    space4.grid(row="10",column="1")
    B3 = tk.Button(settingsPage, text="EXIT", command = settingsPage.destroy)
    B3.grid(row="11",column="1")
def save(ts,td,gs,gd):
    defaults=[ts,td,gs,gd]
    file=open("DefaultSearches.txt","w")
    for i in range (0,len(defaults)):
        file.write(defaults[i]+"\n")
    file.close()
    popup("Saved!")
def default1(settingsPage):
    file=open("DefaultSearches.txt","w")
    default=open("ResetSearches.txt","r")
    defaults=[]
    for line in default:
        defaults.append(line.replace("\n",""))
    for i in range (0,len(defaults)):
        file.write(defaults[i]+"\n")
    file.close()
    settingsPage.destroy()
    popup("Reset!")

def popup(msg):
    warned=True
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text=msg, font=("Helvetica", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
def quitProgram():
    root.destroy()
    sys.exit()

def search():
    global warnedLocation
    #warn if both supply and demand are picked
    if supply.get() == 1 and demand.get() == 1:
        popup("Warning! You can only pick one of supply or demand at once")
    #warn if neither supply and demand are picked
    if supply.get() == 0 and demand.get() == 0:
        popup("Warning! You need to pick either supply or demand")
    #warn if no site is picked
    if siteTickGumtree.get() == 0 and siteTickTwitter.get()== 0:
        popup("Warning! You need to select a site to search")
    #warn if no date selected
    if dateSince.get()=="":
        popup("Warning! You must enter a date")
    #warn if date not in correct format
    if bool(re.match(r"\d\d-\d\d-\d\d\d\d",dateSince.get())) == False:
            popup("Please input a date in the correct format")
    #warn if location inputted incorrectly
    if bool(re.match(r".*,.*",location.get())) == False and location.get() != "":
        popup("Warning! Pleas input a valid location in the correct format")
    #warn once if there is anything in the location box and gumtree is also selected
    if siteTickGumtree.get() == 1 and location.get() != "" and warnedLocation == False:
        warnedLocation=True
        popup("Warning! Locations does not work when using Gumtree.\nOnly results in the UK will be returned.")
        
    if siteTickGumtree.get() == 1:
        progress.step(33)
        allGumtree=ScrapeGumtree.getGumtree(supply.get(),demand.get())
        progress.step(66)
        writeSheets.write(allGumtree,dateSince.get(),"G",supply.get(),demand.get())
        progress.step(100)
    if siteTickTwitter.get() == 1:
        progress.step(33)
        allTweets=APITwitter.fetchdata(supply.get(),demand.get(),location.get(),dateSince.get())
        progress.step(66)
        writeSheets.write(allTweets,dateSince.get(),"T",supply.get(),demand.get())
        progress.step(99)
    
#create checkboxes of sites to search
tk.Label(root, text="            ").grid(row=0,column=0,)
tk.Label(root, text="Sites to search\n(tick multiple)").grid(row=0,column=1)
tk.Checkbutton(root, text="Gumtree", variable=siteTickGumtree).grid(row=1,column=1,sticky="W")
tk.Checkbutton(root, text="Twitter", variable=siteTickTwitter).grid(row=2,column=1,sticky="W")

#create date since text input
tk.Label(root, text="            ").grid(row=0,column=2, sticky="W")
tk.Label(root, text="Date since\n(DD-MM-YYYY)").grid(row=0,column=3,)
dateSince=tk.Entry(root)
dateSince.grid(row=1,column=3,sticky="W")

#create location text input
tk.Label(root, text="            ").grid(row=0,column=4,)
tk.Label(root, text="Location\n(City, Country)").grid(row=0,column=5,)
location=tk.Entry(root)
location.grid(row=1,column=5)
tk.Label(root, text="            ").grid(row=0,column=6,)

#create supply or demand checkboxes
tk.Label(root, text="Supply or Demand\n(tick one)").grid(row=4,column=3)
tk.Checkbutton(root, text="Supply", variable=supply).grid(row=5,column=3,sticky="W")
tk.Checkbutton(root, text="Demand", variable=demand).grid(row=6,column=3,sticky="W")

#create search button
tk.Label(root, text="            ").grid(row=7,column=6,)
tk.Button(root, text='SEARCH', command=search).grid(row=8,column=3)
tk.Label(root, text="            ").grid(row=9,column=6,)
tk.Button(root, text='QUIT', command=quitProgram).grid(row=10,column=3)
tk.Button(root,image=click_btn,command=settings).grid(row=10,column=5,sticky="E")
progress=ttk.Progressbar(root,orient="horizontal")
progress.grid(row=11,column=3)
root.mainloop()
