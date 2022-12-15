import requests
import json 

def get_aircrafts(aircraft_code=None,limit=100,offset=0,headers={}):
    print(aircraft_code)
    url = "https://api.lufthansa.com/v1/mds-references/aircraft/{aircraft_code}?limit={limit}&offset={offset}".format(aircraft_code=aircraft_code,limit=limit,offset=offset)
    # sending get request and saving the response as response object
    r = requests.get(url = url, headers=headers)
    print(url)
    print(r.status_code)
    if(r.status_code==200):
        return r.json()

        