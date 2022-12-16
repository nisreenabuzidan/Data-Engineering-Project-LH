import mysql.connector
import pandas as pd
import datetime 
from datetime import date
import os
import dash 
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
import plotly.express as px 

mysql_db = os.environ.get("MYSQL_DATABASE")
mysql_db_password = os.environ.get("MYSQL_ROOT_PASSWORD")

mydb = mysql.connector.connect(
  host="lufthansa-airLines-sqldb",
  user="root",
  password=mysql_db_password,
  database = mysql_db
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



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



df_1 = df.groupby("departure_airport_code",as_index=False)['latency_at_departure'].mean()
df_1 = pd.merge(
    df_1,
    df_airports,
    how="left",
    left_on="departure_airport_code", right_on="code"

)
print(df_1)
df_1.rename(columns = {"name":"Airport Name","latency_at_departure":"minutes"}, inplace = True)

fig1 = px.bar(df_1, x="Airport Name",
                        y="minutes",
                        color="Airport Name",
                        hover_name="departure_airport_code",
                        title="Average Latency at Departure in minutes",
                        text_auto=True,template='plotly_dark')

"=============================="
df_1 = df.groupby("arrival_airport_code",as_index=False)['latency_at_arrival'].mean()
df_1 = pd.merge(
    df_1,
    df_airports,
    how="left",
    left_on="arrival_airport_code", right_on="code"
    )

df_1.rename(columns = {"name":"Airport Name","latency_at_arrival":"minutes"}, inplace = True)
fig2 = px.bar(df_1, x="Airport Name",
                        y="minutes",
                        color="Airport Name",
                        hover_name="arrival_airport_code",
                        title="Average Latency at Arrival in minutes",
                        text_auto=True,template='plotly_dark')


"=============================="

df_1 = df.groupby(["departure_airport_code","arrival_airport_code"],as_index=False)["id"].count()
df_1 = pd.merge(
    df_1,
    df_airports,
    how="left",
    left_on="departure_airport_code", right_on="code"
    )
df_1 = pd.merge(
    df_1,
    df_airports,
    how="left",
    left_on="arrival_airport_code", right_on="code"
    )

df_1.rename(columns = {"name_x":"Departure Airport","name_y":"Destination Airport","id":"number of Flights"}, inplace = True)
    # Creating the plotly figure
fig3 = px.bar(df_1, x="Departure Airport",
                        y="number of Flights",
                        color="Destination Airport",
                        title="Count of flights between airports",
                        barmode = "group",
                        text_auto=True,template='plotly_dark')


"=============================="
app.layout = html.Div([
  html.H1('General Infos about Customer Flights', style={'textAlign': 'center', 'color': 'brown'}),
  
  html.Div(style={'display': 'flex'},
  children=[
    html.Div(dcc.Graph(id='graph_1',figure = fig1),style={'width': '50%', 'padding': '0px 20px 20px 20px'}),
    html.Div(dcc.Graph(id='graph_2',figure = fig2),style={'width': '50%', 'padding': '0px 20px 20px 20px'}),
    ]),

  
  html.Div(dcc.Graph(id='graph_3',figure = fig3)),

  html.Div(dcc.Graph(id='graph_6')),
  html.Div(dcc.Dropdown(
                df_airports["code"].unique(),
                '',
                id='Dropdown_6'
            ))
    ,
  
  
], style = {'background' : 'light gray'})


"==================================="
@app.callback(Output(component_id='graph_6', component_property='figure'),
            [Input(component_id='Dropdown_6', component_property='value')])
def update_graph(airport_code):
  if airport_code =="":
    airport_code = "FRA"
  filtered_df = df[df.departure_airport_code == airport_code]
  merged_df = pd.merge(
    filtered_df,
    df_airports,
    how="left",
    left_on="departure_airport_code", right_on="code"
  )
  
  
  df_1 = merged_df.groupby(["departure_airport_code","departure_day"],as_index=False)["id"].count()
  df_1["count"]=df_1["id"]
  
  
  df_2 = merged_df.groupby(["departure_airport_code","departure_day"],as_index=False,group_keys=True)["latency_at_departure"].apply(lambda x: (x > datetime.timedelta(minutes=1)).sum())
  df_2["count"]=df_2["latency_at_departure"]
  
  new_df = pd.concat([df_1, df_2], axis=0)
  new_df.rename(columns = {"count":"N.delayed/N.all"}, inplace = True)

  fig = px.bar(new_df, x="departure_day", y="N.delayed/N.all", color="N.delayed/N.all", title="Delayed to All Flights in "+airport_code + " Airport",
             text_auto=True,template='plotly_dark',barmode="stack")                    

  return fig


"==================================="
"""@app.callback(Output(component_id='graph_4', component_property='figure'),
            [Input(component_id='Dropdown_4', component_property='value')])
def update_graph(month):
  filtered_df = df[df.departure_month == month]
  df_1 = filtered_df.groupby(["departure_airport_code","departure_month"],as_index=False)["id"].count()
  df_1 = pd.merge(
    df_1,
    df_airports,
    how="left",
    left_on="departure_airport_code", right_on="code"
    )
  df_1.rename(columns = {"name":"Airport Name","id":"number of flights per month"}, inplace = True)
  fig = px.scatter(df_1, x="Airport Name",
                        y="number of flights per month",
                        color="Airport Name",
                        hover_name="departure_airport_code",
                        size="number of flights per month",
                        title="number of flights per month")

  return fig
"""
"==================================="
"""@app.callback(Output(component_id='graph_5', component_property='figure'),
            [Input(component_id='Dropdown_5', component_property='value')])
def update_graph(airport_code):
    df_1 = df.groupby(["departure_airport_code"],as_index=False)["id"].count()
    df_1 = pd.merge(
    df_1,
    df_airports,
    how="left",
    left_on="departure_airport_code", right_on="code"
    )
    fig = px.scatter_geo(df_1, size="id",lat="Latitude",lon="Longitude",scope='europe',center=dict(lat=51.0057, lon=13.7274))
    return fig


"""


if __name__ == '__main__':
  app.run_server(debug=True, host='0.0.0.0',port=8050)









