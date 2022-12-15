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
if(exist == None):
    fill_reference_data_from_lufthansa_api(client,airports_list = airports_list ,headers = headers)



#create mysql DB
try:
    mysql_db = os.environ.get("MYSQL_DATABASE")
    mysql_db_password = os.environ.get("MYSQL_ROOT_PASSWORD")

    mysqldb = mysql.connector.connect(
    host="lufthansa-airLines-sqldb",
    user="root",
    password=mysql_db_password,
    database =mysql_db
    )
except:
    mysqldb = None

if(mysqldb == None):
    mysqldb = mysql.connector.connect(
    host="lufthansa-airLines-sqldb",
    user="root",
    password=mysql_db_password
    )
    create_mysqldb(mysqldb)


    #fill reference data
    try:
        mysqldb = mysql.connector.connect(
        host="lufthansa-airLines-sqldb",
        user="root",
        password=mysql_db_password,
        database =mysql_db
        )
    except:
        mysqldb = None
    if(mysqldb != None):
        fill_reference_data_in_mysqldb(client,mysqldb)
