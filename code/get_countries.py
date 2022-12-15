import requests
import json 

def get_countries(country_code,limit=100,offset=0,headers={}):
    
    url = "https://api.lufthansa.com/v1/mds-references/countries/{country_code}?llang=EN&limit={limit}&offset={offset}".format(country_code=country_code,limit=limit,offset=offset)
    # sending get request and saving the response as response object
    r = requests.get(url = url, headers=headers)
    if(r.status_code==200):
        return r.json()
