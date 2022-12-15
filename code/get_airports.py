import requests
import json 

def get_airports(airport_code,limit=100,LHoperated=0,headers={}):
    url = "https://api.lufthansa.com/v1/mds-references/airports/{airport_code}?lang=EN&limit={limit}&LHoperated={LHoperated}".format(airport_code=airport_code,limit=limit,LHoperated=LHoperated)
    # sending get request and saving the response as response object
    r = requests.get(url = url, headers=headers)
    if(r.status_code==200):
        return r.json()