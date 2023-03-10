import os
import datetime

from pymongo import MongoClient
import mysql.connector

from get_token import get_access_token
from fill_data_in_mongoDB import fill_reference_data_from_lufthansa_api
from fill_data_in_mysqlDB import fill_reference_data_in_mysqldb
from create_mysql_db import create_mysqldb

airports_list = ["FRA","HAM","LHR","LTN","MAD","CDG","DUS"]


client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
grant_type = os.environ.get("GRANT_TYPE")

access_token_dict =get_access_token(client_id,client_secret,grant_type)

access_token = access_token_dict.get("access_token")
token_type = access_token_dict.get("token_type")

headers = {"Authorization":token_type+" "+access_token}

mongo_db_username = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
mongo_db_password = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")


#Connect to Mongo DB Database
client = MongoClient(
    host='lufthansa-airLines-mongodb',
    port=27017,
    username = mongo_db_username,
    password = mongo_db_password,
    authSource='admin'
)


databases_list = client.list_database_names()
try:
   exist = databases_list.index("LufthansaDB")
except:
    exist = None

print("databases_list ",databases_list)
print("exist ",exist)

if(exist == None):
    try:
        fill_reference_data_from_lufthansa_api(client,airports_list = airports_list ,headers = headers)
        print("fill_reference_data_from_lufthansa_api is done")
    except:
        print("fill_reference_data_from_lufthansa_api throws Exception")


#create mysql DB
mysql_host="lufthansa-airLines-sqldb"
mysql_password =os.environ.get("MYSQL_ROOT_PASSWORD")

try:
    print("hi")
    create_mysqldb(mysql_host,mysql_password)
except:
    print("create_mysqldb throws Exception")


#fill reference data
try:
    fill_reference_data_in_mysqldb(client,mysql_host,mysql_password)
    print("fill_reference_data_in_mysqldb is done")
except:
    print("fill_reference_data_in_mysqldb throws Exception")

    
