'''This file gets the news from https://newsapi.org and loads in all the images related to the news by filling up the widgets defined in newsgui.py'''

import urllib.request, json, newsgui
from tkinter import *
from PIL import Image

def news(country_code):
    newsapi_key = 'ea9935cfc536478dabb3e120b106f258'
    try:
        newsjson = json.loads(urllib.request.urlopen('https://newsapi.org/v2/top-headlines?country='+country_code+'&apiKey='+newsapi_key+'&sortBy=relevancy').read())
        #get request for most relevant news
    except:
        print ("Sorry, your country is not supported at the moment!")
        quit()
    return dict(newsjson)["articles"][:7] #limits the number of articles

def newsparse(framenews,bgcol,fgcol,country_code): #function to process all the news
    newsLabel = Label(framenews, text = "Latest News", font =("century gothic bold", 20), bg=bgcol, fg=fgcol) #sets heading
    newsLabel.grid(row = 0, column=0, columnspan=2, pady = (30,0), sticky="w")
    newscount=0
    newsimlist=[]
    imnum = 0
    for i in news(country_code): #calls news function which returns the newsjson
        rownum = 0 
        frametempNews = Frame(framenews, bg=bgcol) #creates a temp frame for news
        frametempNews.grid(column=0, sticky="w")
        opener = urllib.request.build_opener() #creates urllib3 object in order to download images from the news article
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        try:
            urllib.request.urlretrieve(i["urlToImage"], "assets/"+str(imnum)) #saves the asset into the assets folder
        except:
            continue
        newsrawim = Image.open("assets/"+str(imnum)) #opens the image within tkinter
        newsim = newsrawim.resize((150,75))
        #Use PIL to convert the arbitrary file type to png
        newsim.convert("RGB").save("assets/"+str(imnum)+".png", "png") #convers the assets to png
        newsimlist.append(PhotoImage(file="assets/"+str(imnum)+".png")) #adds the converted image to the list of images
        newsbutton  = Button(frametempNews, image=newsimlist[imnum], border=0, command = lambda url=i["url"]:newsgui.open_site(url)) #creates a button in order to open news links using the open_site function within newsgui
        newsbutton.image=newsimlist[imnum] #sets the image in tkinter
        newsbutton.grid(column=0, rowspan=3, pady = (20,0))
        imnum+=1

        titleLabel = Message(frametempNews, text= i["title"], width=800, font =("century gothic bold", 11), bg=bgcol, fg=fgcol) #sets the title of the news
        titleLabel.bind("<Button-1>", lambda e,url=i["url"]:newsgui.open_site(url)) #binds lambda function to open site on click
        titleLabel.grid(column = 1, row=rownum, pady = (20,0), sticky="w")
        rownum+=1

        pubatLabel = Label(frametempNews, text= i["publishedAt"].replace("T"," - ").replace("Z",""), font=("bahnschrift",9), bg=bgcol, fg=fgcol) #sets time published
        pubatLabel.grid(column = 1,row=rownum, sticky="nw", padx=(10,0))
        rownum+=1
        
        descLabel = Message(frametempNews, text= i["description"]+" ...READ MORE ➔", width=700, font =("Bahnschrift", 10), bg=bgcol, fg=fgcol) #shorthand description is set
        descLabel.bind("<Button-1>", lambda e,url=i["url"]:newsgui.open_site(url))
        descLabel.grid(column = 1,row=rownum, sticky="w")
        
        newscount+=1
        if newscount==5: #limits news to upto 5 elements
            break
