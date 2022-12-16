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
## **Steps Overview**
- Register on Lufthansa API and get Client secret and Client ID
- Generate token to be used to request Lufthansa API 
- Get refernce data from Lufthansa API and store them localy
- get customer flights data daily between the differenct airports and store them localy
- build an API to retrieve data from load Database
- Show some statitics in a Dashboard

****
## **Steps in Details**
### 1.**Used Databases**
- Mongo DB
- Mysql DB
### 2.**Database Schema**
- Countries collection/table used to store data about countries of the studies airports
- Cities collection/table used to store data about cities of the studies airports
- Airports collection/table used to store data about selected airports 
- flights collection/table used to store data about flights between selected airports 

    ![The following diagram illustrates the relational DB](https://github.com/nisreenabuzidan/Data-Engineering-Project-LH/commit/fa7291b358ee5d515d0b7139d188dbb234f9e416#diff-900b4e5c33b5ca5c6876541982619d23ad46bb2a178b4a29923e32982b7a01dc)


****
### 3.**Initial Step**
In this step the refernce data is requested from Lufthansa API using the following get requests :
- Countries :
https://api.lufthansa.com/v1/mds-references/countries/DE
- Cities :
https://api.lufthansa.com/v1/mds-references/cities/FRA
- Airports :
https://api.lufthansa.com/v1/mds-references/airports/FRA








