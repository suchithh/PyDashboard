from geopy import Nominatim
import requests

geolocator = Nominatim(user_agent="newspy")
def location():
    # Location through IP Address of the user 
    try:
        ip_loc = requests.get('https://api.ipdata.co?api-key=6a85222c3951b4c28444821f6cc8c6bc21b04b761589662b723e29f5').json() #get request to make ip request
    except:
        print ("You are either not connected to the internet or your IP address is not recognised. Please try again later!")
        quit()
    city_name, country_name, country_code = ip_loc['city'],ip_loc['country_name'],ip_loc['country_code']
    return(city_name,country_name,country_code)

def geocode_loc(city):
    #Location through geocoding user input (currently unused function)
    location = geolocator.geocode(city, addressdetails=True)
    city_name = (location.raw['address']['city'])
    country_name = (location.raw['address']['country'])
    country_code = (location.raw['address']['country_code'])
    return(city_name,country_name,country_code)