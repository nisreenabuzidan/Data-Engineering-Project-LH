import json
import datetime
import pandas as pd
from pandas import DataFrame
import sys
import mysql.connector


def fill_reference_data_in_mysqldb(mongo_client,mysql_host,mysql_password):
    try:
         
        mysqldb = mysql.connector.connect(
          host=mysql_host,
          user="root",
          password=mysql_password,
          database ="lufthansadb"
        )
        sqlcursor = mysqldb.cursor()
        

        mongo_db = mongo_client["LufthansaDB"]
        
        #fill Countries
        counties_col = mongo_db["countries"]
        mongo_cursor = counties_col.find()
        mongo_cursor_list = list(mongo_cursor)
        df_countries = DataFrame(mongo_cursor_list)
        
        
        country_codes = df_countries["CountryCode"]
        country_names = df_countries["Names"]

        for country_code,country_name in zip(country_codes,country_names):
            
            val = (country_code,country_name.get("Name")[2].get("$"))
            sql = "INSERT INTO `countries` (code,name) VALUES (%s, %s)"
            sqlcursor.execute(sql, val)
            mysqldb.commit()

        sql = "select * from countries"
        myresult = sqlcursor.fetchall()
        for x in myresult:
            print(x)
        """============================="""

        #fill Cities
        cities_col = mongo_db["cities"]
        mongo_cursor = cities_col.find()
        mongo_cursor_list = list(mongo_cursor)
        df_cities = DataFrame(mongo_cursor_list)

        
        
        city_codes = df_cities["CityCode"]
        city_names = df_cities["Names"]

        country_codes = df_cities["CountryCode"]
        

        for city_code,city_name ,country_code in zip(city_codes,city_names,country_codes):
            val = (city_code,city_name.get("Name").get("$"),country_code)
            sql = "INSERT INTO `cities` (code,name,country_code) VALUES (%s, %s, %s)"
            sqlcursor.execute(sql, val)
            mysqldb.commit()

        sql = "select * from cities"
        myresult = sqlcursor.fetchall()
        for x in myresult:
            print(x)
        """============================="""

        #fill Airports
        airports_col = mongo_db["airports"]
        
        mongo_cursor = airports_col.find()
        mongo_cursor_list = list(mongo_cursor)
        df_airports = DataFrame(mongo_cursor_list)
      
        
        airport_codes = df_airports["AirportCode"]
        airport_names = df_airports["Names"]

        city_codes = df_airports["CityCode"]
        country_codes = df_airports["CountryCode"]
        positions = df_airports["Position"]
    
        for airport_code,airport_name ,country_code,city_code,position in zip(airport_codes,airport_names,country_codes,city_codes,positions):
            latitude = position.get("Coordinate").get("Latitude")
            longitude = position.get("Coordinate").get("Longitude")
        
            try:
                val = (airport_code,airport_name.get("Name").get("$"),country_code,city_code,latitude,longitude)
                sql = "INSERT INTO `airports` (code,name,country_code,city_code,Latitude,Longitude) VALUES (%s, %s, %s, %s, %s, %s)"
                sqlcursor.execute(sql, val)
                mysqldb.commit()
            except mysqldb.connector.Error as error:
                print("Failed insert airports data: {}".format(error), sql)
        
        sql = "select * from airports"
        myresult = sqlcursor.fetchall()
        for x in myresult:
            print(x)

    except mysqldb.connector.Error as error:
        print("Failed insert data: {}".format(error))
    finally:
        if mysqldb.is_connected():
            sqlcursor.close()
            mysqldb.close()
            print("MySQL connection is closed")


def validate_key(x_dict ,x_key ):
    if(x_dict != None):
        if x_key  in x_dict.keys():
            return(x_dict.get(x_key))
        else:
            return " "
    else:
        return " "

def parse_customer_flights_dict(flight):
                departure_airport_code = flight.get("Departure").get("AirportCode")
                departure_scheduled_date  = flight.get("Departure").get("Scheduled").get("Date")+" "+flight.get("Departure").get("Scheduled").get("Time")+":00"
                departure_actual_date    = validate_key(flight.get("Departure").get("Actual"),"Date")+" "+validate_key(flight.get("Departure").get("Actual"),"Time")+":00"
                departure_terminal_name  = validate_key(flight.get("Departure").get("Terminal"),"Name")
                departure_terminal_gate  = validate_key(flight.get("Departure").get("Terminal"),"Gate")
                departure_status_code  = flight.get("Departure").get("Status").get("Code")
                departure_status_desc  = flight.get("Departure").get("Status").get("Description")

                arrival_airport_code = flight.get("Arrival").get("AirportCode")
                arrival_scheduled_date    = flight.get("Arrival").get("Scheduled").get("Date")+" "+flight.get("Arrival").get("Scheduled").get("Time")+":00" 
                arrival_actual_date    = validate_key(flight.get("Arrival").get("Actual"),"Date")+" "+validate_key(flight.get("Arrival").get("Actual"),"Time")+":00" 
                arrival_terminal_name  =  validate_key(flight.get("Arrival").get("Terminal"),"Name")
                arrival_terminal_gate  = validate_key(flight.get("Arrival").get("Terminal"),"Gate")
                arrival_status_code  = flight.get("Arrival").get("Status").get("Code")
                arrival_status_desc  = flight.get("Arrival").get("Status").get("Description")

                flight_number  = flight.get("OperatingCarrier").get("FlightNumber")
                operating_carrier_airline_id  = flight.get("OperatingCarrier").get("AirlineID")
                aircraft_code  = flight.get("Equipment").get("AircraftCode")

                return  (
                departure_airport_code ,
                departure_scheduled_date ,
                departure_actual_date , 
                departure_terminal_name,
                departure_terminal_gate ,
                departure_status_code ,
                departure_status_desc ,

                arrival_airport_code ,
                arrival_scheduled_date , 
                arrival_actual_date , 
                arrival_terminal_name ,
                arrival_terminal_gate ,
                arrival_status_code ,
                arrival_status_desc ,

                flight_number,
                operating_carrier_airline_id ,
                aircraft_code)

def fill_customer_flights_data_in_mysqldb(mongo_client,mysqldb,date):
    sqlcursor = mysqldb.cursor()
    mongo_db = mongo_client["LufthansaDB"]
    col = mongo_db["flights"]

    sql = '''INSERT INTO `flights` (
            departure_airport_code ,
            departure_scheduled_date ,
            departure_actual_date , 
            departure_terminal_name,
            departure_terminal_gate ,
            departure_status_code ,
            departure_status_desc ,

            arrival_airport_code ,
            arrival_scheduled_date , 
            arrival_actual_date , 
            arrival_terminal_name ,
            arrival_terminal_gate ,
            arrival_status_code ,
            arrival_status_desc ,

            flight_number,
            operating_carrier_airline_id ,
            aircraft_code) 
            VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s)'''

    results =list(col.find(filter={"FlightInformation.Flights.Flight.Departure.Scheduled.Date":date},
                           projection = { '_id': 0}
                           ))
    
    i=0
    for flights in  results:
        flights = flights.get("FlightInformation").get("Flights").get("Flight")
        if(type(flights)==list):
            for flight in flights:
                val = parse_customer_flights_dict(flight)
                sqlcursor.execute(sql, val)
        else:  
            val = parse_customer_flights_dict(flights)
            sqlcursor.execute(sql, val)

    mysqldb.commit()
    


