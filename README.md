# **Data-Engineering-Project-LH**

## **Purpose**
This Project aims to request data from Lufthansa API, save them localy and then show some statistics 
****

## **Case study**
 - Some airports are selected to study latency on customer flights between them : on **Departure** and on **Arrival**
- Study latency in an airport in a time range
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
- Get customer flights data daily between the differenct airports and store them localy
- Build an API to retrieve data from load Database
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
- Flights collection/table used to store data about flights between selected airports 
 The following diagram illustrates the relational DB :

    ![The following diagram illustrates the relational DB](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/blob/main/images/ERD.svg)


****
### 3.**Initial Step**
- Run Database conatiners to establish connections to databases
- Run the main container to install all requirments and create databases
- Get refernce data from Lufthansa API using the following get requests :
    > Countries :
https://api.lufthansa.com/v1/mds-references/countries/DE

    >  Cities :
https://api.lufthansa.com/v1/mds-references/cities/FRA

    > Airports :
https://api.lufthansa.com/v1/mds-references/airports/FRA

then the data are stored in No SQL DB (Mongo DB) and relational DB (Mysql DB) 
****

### 4.**Daily Process**

Using Airflow a daily process is automated to do the following :
- Generate a new token to be used for requesting Lufthansa API
- Get customer flights info between the different airports from Lufthansa API on the prevoius day using the request (example):
https://api.lufthansa.com/v1/operations/customerflightinformation/route/FRA/HAM/2022-12-09

- Store this data in Json file to be used in the next step
- Parse the stored Json file and store the data in Mongo DB(**Flights** Collection)
- Request Data from Mongo DB and store them in Mysql DB (**Flights** Table)
- The image below is a screenshot of the daily dag
![The following diagram illustrates the Daily Dag](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/blob/main/images/airflow-1.jpg)

### 5.**Lufthansa Info API**
Using **fastapi** from **Python** an API with 2 end points is developed :
- http://.../8000/  : Check if the API is running healthy 
- http://.../8000//airport_latency_info?FRA
  > This endpoint accepts one Mandatory parameter which is the airport_code and tow optinal parameters :start_date and end_date

  > This end point returns a Json file containing Airport_code , the number of all flights departing from this airport and the number of delayed flights on the same day
  
  > The number of resuls depends on the duration requested from start_date to end_date 

- The image below is a screenshot of the Json response
    ![The following diagram is a screenshot of the Json response](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/blob/main/images/API-1.jpg)

    ![The following diagram is a screenshot of the Json response](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/blob/main/images/API-2.jpg)

### 6.**API Test**i
Test the different end-points of the API and print the result in a log file **api_test.log**
The following screenshots are for different case of endpoints test:
![The following diagram is a screenshot of the Json response](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/blob/main/images/api_test_1.jpg)

![The following diagram is a screenshot of the Json response](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/blob/main/images/api_test_1.jpg)


### 7.**Dashboard**
Using  **Dash** and **Python Pandas** from **Python** a Dashboard is developed to display the following bar charts : 

- Avergage Latency at Departure in minutes 
- Avergage Latency at Arrival in minutes
- Count of flights between airports
- Number of Delayed/Number of All flights in an airports 
    ![The following diagram is a screenshot dashboard](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/blob/main/images/dashboard1.jpg)

    ![The following diagram is a screenshot dashboard](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/blob/main/images/dashboard2.jpg)

### 8.**Docker and Docker-compose**
Running the project consists of 2 phases:
#### 1- Initial phase
- Run mongo DB service 
    >docker-compose up -d mongodb 
- Run mysql DB service 
    >MYSQL_ROOT_PASSWORD=root docker-compose up -d mySqldb
- Run main Service which creates databases and fill reference data
    >CLIENT_ID={LH client ID } CLIENT_SECRET={LH client secret} GRANT_TYPE=client_credentials docker-compose up -d main

    >docker-compose run -it main
    CLIENT_ID={LH client ID } CLIENT_SECRET={LH client secret} GRANT_TYPE=client_credentials python3 main.py

- After that the docker container should be removed
    >exit

    >docker-compose down

#### 2- Continuous phase
Run the docker-compose 

- CLIENT_ID={LH client ID } CLIENT_SECRET={LH client secret} GRANT_TYPE=client_credentials docker-compose up 

This will run the following :
> Mongo DB service

> Mysql DB service

> api service

> api_test service

> dashboard service

> Airflow services


## **Possible Improvments**
- Organize the code in better way
- Allow the airflow to make the initial phase
- CI/CD 
- add more details to dashboard
- To study the latency in more details ,information about aircrafts should be collected .
- Machine learning model to find the relation between latency and aircraft type .







