import requests
import json 
import os
import pandas as pd


def get_access_token(client_id,client_secret,grant_type):
        # resquest
        url = "https://api.lufthansa.com/v1/oauth/token"
        params = { "client_id":client_id,
            "client_secret" : client_secret,
            "grant_type" : grant_type
        }
        
        # sending get request and saving the response as response object
        r = requests.post(url = url, data = params)
        
        # extracting data in json format
        if(r.status_code == 200):
                token_respone = r.json()
                access_token = token_respone["access_token"]
                token_type =  token_respone["token_type"]
                return {"access_token":access_token,"token_type" :token_type}
        else :
                return None   




