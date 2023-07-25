import urllib.request, json

weather_key='56696014b1b0f79692a93ba0ec757061'
def weather(city_name):
    try:
        #get request to receive weather info
        weatherjson = json.loads(urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city_name.replace(" ","%20")+'&appid='+weather_key+'&units=metric').read())
    except:
        print ("You are either not connected to the internet or weather services is unavailable. Please try again later!")
        quit()
    weatherdata = dict(weatherjson)
    weatherstring = weatherdata["weather"][0]["main"]+", "+str(round(weatherdata["main"]["temp"]))+u"\N{DEGREE SIGN}"
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener) #creates a urllib instance to download the image of weather
    try:
        #downloads the weather image into assets
        urllib.request.urlretrieve("https://openweathermap.org/img/wn/"+weatherdata["weather"][0]['icon']+".png", "assets/weather.png")
    except:
        print ("You are either not connected to the internet or one of the services is unavailable. Please try again later!")
        quit()
    return weatherstring