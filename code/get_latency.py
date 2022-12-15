import mysql.connector
import pandas as pd
import datetime 
from datetime import date



mydb = mysql.connector.connect(
  #host="localhost",
  host="lufthansa-airLines-sqldb",
  user="root",
  password="root",
  database="lufthansadb"
)

df =pd.read_sql('SELECT * FROM flights  ', con=mydb)
df_airports =pd.read_sql('SELECT * FROM airports  ', con=mydb)


def validate_date_format(date_text):
        try:
            return datetime.datetime.strptime(date_text,'%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None


df["latency_at_departure"] = (df["departure_actual_date"].apply(lambda x: validate_date_format(x)) - df["departure_scheduled_date"].apply(lambda x: validate_date_format(x)))/60

df.loc[df['latency_at_departure'] < datetime.timedelta(minutes=0) , 'latency_at_departure'] =  datetime.timedelta(minutes=1)
df["latency_at_arrival"] = (df["arrival_actual_date"].apply(lambda x: validate_date_format(x)) - df["arrival_scheduled_date"].apply(lambda x: validate_date_format(x)))/60
df.loc[df['latency_at_arrival'] < datetime.timedelta(minutes=0) , 'latency_at_arrival'] =  datetime.timedelta(minutes=1)
df["departure_month"] = [datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S').month for i in df["departure_scheduled_date"]]
df["departure_day"] = [datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S').date() for i in df["departure_scheduled_date"]]


def get_latency(airport_code,from_date,to_date):
  try:
    df =pd.read_sql('SELECT * FROM flights  ', con=mydb)
    df_airports =pd.read_sql('SELECT * FROM airports  ', con=mydb)  

    df["latency_at_departure"] = (df["departure_actual_date"].apply(lambda x: validate_date_format(x)) - df["departure_scheduled_date"].apply(lambda x: validate_date_format(x)))/60

    df.loc[df['latency_at_departure'] < datetime.timedelta(minutes=0) , 'latency_at_departure'] =  datetime.timedelta(minutes=1)
    df["latency_at_arrival"] = (df["arrival_actual_date"].apply(lambda x: validate_date_format(x)) - df["arrival_scheduled_date"].apply(lambda x: validate_date_format(x)))/60
    df.loc[df['latency_at_arrival'] < datetime.timedelta(minutes=0) , 'latency_at_arrival'] =  datetime.timedelta(minutes=1)
    df["departure_month"] = [datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S').month for i in df["departure_scheduled_date"]]
    df["departure_day"] = [datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S').date() for i in df["departure_scheduled_date"]]

 
    
    filtered_df = df[df.departure_airport_code == airport_code]
    
    if (from_date != ""):
        filtered_df = filtered_df[filtered_df.departure_scheduled_date >= from_date] 
    if (to_date != ""):
        filtered_df = filtered_df[filtered_df.departure_scheduled_date <= to_date]

    

    merged_df = pd.merge(
    filtered_df,
    df_airports,
    how="left",
    left_on="departure_airport_code", right_on="code"
    )
  
    df_1 = merged_df.groupby(["departure_airport_code","departure_day"],as_index=False)["id"].count()
    df_2 = merged_df.groupby(["departure_airport_code","departure_day"],as_index=False,group_keys=True)["latency_at_departure"].apply(lambda x: (x > datetime.timedelta(minutes=1)).sum())
    new_df = df_1.merge(df_2,on =["departure_airport_code","departure_day"] )
    new_df["number_of_all_flights"]= new_df["id"]
    new_df["number_of_delayed_flights"]= new_df["latency_at_departure"]
    new_df["departure_day"] = new_df["departure_day"].astype(str)
    new_df = new_df.drop(columns = ["id","latency_at_departure"])
    return new_df
  except Exception:
        return pd.DataFrame()
        



