from pymongo import MongoClient
client = MongoClient(
    host='lufthansa-airLines-mongodb',
    port=27017,
    username = "root",
    password = "root",
    authSource='admin'
)
import mysql.connector
mysqldb = mysql.connector.connect(
          host="lufthansa-airLines-sqldb",
          user="root",
          password="root",
          database ="lufthansadb"
        )
sqlcursor = mysqldb.cursor()

"""sql = "select * from airports"
sqlcursor.execute(sql)
myresult = sqlcursor.fetchall()
for x in myresult:
    print(x)"""




from pandas import DataFrame

mongo_db = client["LufthansaDB"]
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
    #print(latitude)
    val = (airport_code,airport_name.get("Name").get("$"),country_code,city_code,latitude,longitude)
    sql = "INSERT INTO `airports` (code,name,country_code,city_code,Latitude,Longitude) VALUES (%s, %s, %s, %s, %s, %s)"
    print(sql)
    sqlcursor.execute(sql, val)
    #mysqldb.commit()"""
    
    