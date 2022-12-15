import datetime
import requests
import json 



def get_customer_flight_information_on_route(origin_airport_code,destination_airport_code,departure_time=None,headers={}):
        if(departure_time==None):
            departure_time = datetime.datetime.now().strftime("%Y-%m-%d")
            
        url = "https://api.lufthansa.com/v1/operations/customerflightinformation/route/{origin_airport_code}/{destination_airport_code}/{departure_time}".format(origin_airport_code=origin_airport_code,destination_airport_code=destination_airport_code,departure_time=departure_time)
       
        # sending get request and saving the response as response object
        r= requests.get(url = url, headers=headers)
        json_object= r.json()
        print("r.status_code , " ,r.status_code)
        if(r.status_code==200):
            return json_object
       
   
def get_customer_flight_information_between_airports(airports_list=[],departure_time=None,headers={}):
    result_list=[]
    if(departure_time==None):
            departure_time = datetime.datetime.now().strftime("%Y-%m-%d")
    
    for origin_airport_code in airports_list:
        for detination_airport_code in airports_list:
            if(origin_airport_code != detination_airport_code):
                time.sleep(1)
                json_object = get_customer_flight_information_on_route(origin_airport_code,detination_airport_code,departure_time,headers)
                if(json_object):
                    result_list.append(json_object)
        
    with open("./data/json/{departure_time}.json".format(departure_time=departure_time), "w") as outfile:
            json.dump(result_list, outfile,indent=4)

 





