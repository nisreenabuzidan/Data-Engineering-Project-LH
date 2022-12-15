from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
import datetime
import os
import sys
from pymongo import MongoClient
import mysql.connector
 
# adding code to the system path
sys.path.insert(0, './code')
from get_token import get_access_token
from get_customer_flight_information_on_route import get_customer_flight_information_between_airports
from fill_data_in_mongoDB import fill_customer_flight_information_from_json
from fill_data_in_mysqlDB import fill_customer_flights_data_in_mysqldb

airports_list = ["FRA","HAM","LHR","LTN","MAD","CDG","DUS"]
headers ={}

# to get valid response from Lufthansa API the date muns not be greater than 7 days ago 
departure_time = days_ago(1).date()

mongo_db_username = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
mongo_db_password = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")


mysql_db = os.environ.get("MYSQL_DATABASE")
mysql_db_password = os.environ.get("MYSQL_ROOT_PASSWORD")
#connect to mysql DB
mysqldb = mysql.connector.connect(
    host="lufthansa-airLines-sqldb",
    user="root",
    password=mysql_db_password,
    database =mysql_db
)


daily_dag = DAG(
    dag_id='daily_dag',
    description='This DAG is used to get data from Lufthansa API on daily basis',
    schedule_interval=None,#'00 18 * * *',
    doc_md="""# Documented DAG
    This DAG is used to get data from Lufthansa API

    This DAG has been made:

    * by Nisreen Abu Zidan
    * with documentation
    * with caution
    """,
    start_date=days_ago(0)
)
    

def generate_access_token_and_fill_flights_data_in_json():
    #get enviornment variables
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    grant_type = os.environ.get("GRANT_TYPE")

    access_token_dict = get_access_token(client_id,client_secret,grant_type)
    print("access_token_dict = " ,access_token_dict)
    if(access_token_dict != None):
        access_token = access_token_dict.get("access_token")
        token_type = access_token_dict.get("token_type")

        headers = {"Authorization":token_type+" "+access_token} 
        get_customer_flight_information_between_airports(airports_list,departure_time,headers)


task1 = PythonOperator(
    task_id='generate_access_token_and_fill_flights_data_in_json',
    python_callable=generate_access_token_and_fill_flights_data_in_json,
    dag=daily_dag
)


def fill_flight_data_in_mongodb():
    client = MongoClient(
    host='lufthansa-airLines-mongodb',
    port=27017,
    username = mongo_db_username,
    password = mongo_db_password,
    authSource='admin'
    )
    fill_customer_flight_information_from_json(client,departure_time)
    client.close()


task2 = PythonOperator(
    task_id='fill_flight_data_in_mongodb',
    python_callable=fill_flight_data_in_mongodb,
    dag=daily_dag
)


def fill_flights_data_in_mysqldb():
    client = MongoClient(
    host='lufthansa-airLines-mongodb',
    port=27017,
    username = mongo_db_username,
    password = mongo_db_password,
    authSource='admin'
    )
    departure = str(departure_time)
    fill_customer_flights_data_in_mysqldb(client,mysqldb,departure)
    client.close()


task3 = PythonOperator(
    task_id='fill_flights_data_in_mysqldb',
    python_callable=fill_flights_data_in_mysqldb,
    dag=daily_dag
)


task1 >> task2 >> task3