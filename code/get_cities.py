import requests
import json 

def get_cities(city_code,limit=100,offset=0,headers={}):
    
    url = "https://api.lufthansa.com/v1/mds-references/cities/{city_code}?lang=EN&limit={limit}&offset={offset}".format(city_code=city_code,limit=limit,offset=offset)
    # sending get request and saving the response as response object
    r = requests.get(url = url, headers=headers)
    if(r.status_code==200):
        return r.json()