# **Data-Engineering-Project-LH**

## **Purpose**
This Project aims to request data from Lufthansa API, save them localy and then show some statistics 
****

## **Case study**
 Some airports are selected to study latency on customer flights between them : on **Departure** and on **Arrival**

### **Selected airports**
>Frankfurt

>Hamburg

>Dusseldorf

>London Heathrow

>Madrid

>Paris/. Ch.de Gaulle
****
## **Process Overview**
- Register on Lufthansa API and get Client secret and Client ID
- Generate token to be used to request Lufthansa API 
- Get refernce data from Lufthansa API and store them localy
- get customer flights data daily between the differenct airports and store them localy
- build an API to retrieve data from load Database
- Show some statitics in a Dashboard

****
## **Process in Detail**
### 1.**Used Databases**
- Mongo DB
- Mysql DB
### 2.**Database Schema**
- Countries collection/table used to store data about countries of the studies airports
- Cities collection/table used to store data about cities of the studies airports
- Airports collection/table used to store data about selected airports 
- flights collection/table used to store data about flights between selected airports 
 The following diagram illustrates the relational DB :

    ![The following diagram illustrates the relational DB](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/blob/main/images/ERD.svg)


****
### 3.**Initial Step**
In this step the refernce data is requested from Lufthansa API using the following get requests :
- Countries :
https://api.lufthansa.com/v1/mds-references/countries/DE
- Cities :
https://api.lufthansa.com/v1/mds-references/cities/FRA
- Airports :
https://api.lufthansa.com/v1/mds-references/airports/FRA

then the data are stored in No SQL DB (Mongo DB) and relational DB (Mysql DB) 
****

### 4.**Daily Process**

Using Airflow a daily process is automated to do the following :
- generate a new token to be used for requesting Lufthansa API
- get customer flights info between the different airports from Lufthansa API on the prevoius day using the request (example):
https://api.lufthansa.com/v1/operations/customerflightinformation/route/FRA/HAM/2022-12-09

- store this data in Json file to be used in the next step
- parse the stored Json file and store the data in Mongo DB(**Flights** Collection)
- request Data from Mongo DB and store them in Mysql DB (**Flights** Table)
- the image below is a screenshot of the daily dag
![The following diagram illustrates the Daily Dag](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/blob/main/images/ERD.svg)

### 5.**Lufthansa Info API**
Using **fastapi** from **Python** an API with 2 end points is developed :
- http://.../8000/  : Check if the API is running healthy 
- http://.../8000//airport_latency_info?FRA
  > This endpoint accepts one Mandatory parameter which is the airport_code and tow optinal parameters :start_date and end_date

  > This end point returns a Json file containing Airport_code , the number of all flights departing from this airport and the number of delayed flights on the same day
  
  > The number of resuls depends on the duration requested from start_date to end_date 

- the image below is a screenshot of the Json response
![The following diagram is a screenshot of the Json response](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/blob/main/images/ERD.svg)

### 6.**Dashboard**
Using  **Dash** and **Python Pandas** from **Python** a Dashboard is developed to display the following bar charts : 

- Avergage Latency at Departure in minutes 
- Avergage Latency at Arrival in minutes
- Count of flights between airports
- Number of Delayed/Number of All flights in an airports 
![The following diagram is a screenshot dashboard](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/blob/main/images/ERD.svg)





