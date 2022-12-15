from pymongo import MongoClient


client = MongoClient(
    host='localhost',
    port=27017,
    username = "root",
    password = "root",
    authSource='admin'
    )
import mysql.connector

try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database ="lufthansadb"
    )
except:
    mydb=  None

print(mydb)
#mycursor = mydb.cursor()
#print(mycursor)



def fill_reference_data_from_lufthansa_api(mydb):
    print("dddddd")
        
       
        
        
#fill_reference_data_from_lufthansa_api(mydb)
