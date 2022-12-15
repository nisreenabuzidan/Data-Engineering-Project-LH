import mysql.connector

def create_mysqldb(host,password):
  try:
    connection = mysql.connector.connect(
          host=host,
          user="root",
          password=password
      )
    
    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS lufthansadb")
    connection.commit()
  except connection.connector.Error as error:
    print("Failed to create Database: {}".format(error))
  finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

  try:   
    mysqldb = mysql.connector.connect(
          host=host,
          user="root",
          password=password
          database ="lufthansadb"
      )
    mycursor = mysqldb.cursor()

    #create table countries
    sql ='''CREATE TABLE countries (
    code VARCHAR(50) NOT NULL, 
    name VARCHAR(100) NOT NULL, 
    PRIMARY KEY (code)
    )'''
    mycursor.execute(sql)
    mysqldb.commit()

    #create table cities
    sql = '''CREATE TABLE cities (
    code VARCHAR(50) NOT NULL, 
    name VARCHAR(100) NOT NULL, 
    country_code VARCHAR(50) NOT NULL,
    PRIMARY KEY (code),
    FOREIGN KEY (country_code) REFERENCES countries(code)
    )'''
    mycursor.execute(sql)
    mysqldb.commit()


    #create table airports
    sql = '''CREATE TABLE airports (
    code VARCHAR(50) NOT NULL, 
    name VARCHAR(100) NOT NULL, 
    city_code VARCHAR(50) NOT NULL,
    country_code VARCHAR(50) NOT NULL,
    Latitude DECIMAL(10,10),
    Longitude DECIMAL(10,10),
    PRIMARY KEY (code),
    FOREIGN KEY (country_code) REFERENCES countries(code),
    FOREIGN KEY (city_code) REFERENCES cities(code)
    )'''

    mycursor.execute(sql)
    mysqldb.commit()

    #create table aircrafts
    sql = '''CREATE TABLE aircrafts (
    code VARCHAR(50) NOT NULL, 
    name VARCHAR(100) NOT NULL, 
    PRIMARY KEY (code)
    )'''
    mycursor.execute(sql)
    mysqldb.commit()


    sql = '''CREATE TABLE flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    departure_airport_code VARCHAR(50) NOT NULL, 
    departure_scheduled_date VARCHAR(50)  NOT NULL, 
    departure_actual_date VARCHAR(50)  NOT NULL, 
    departure_terminal_name VARCHAR(100),
    departure_terminal_gate VARCHAR(50),
    departure_status_code VARCHAR(50),
    departure_status_desc VARCHAR(100),

    arrival_airport_code VARCHAR(50) NOT NULL,
    arrival_scheduled_date VARCHAR(50)  NOT NULL, 
    arrival_actual_date VARCHAR(50)  NOT NULL, 
    arrival_terminal_name VARCHAR(100),
    arrival_terminal_gate VARCHAR(50),
    arrival_status_code VARCHAR(50),
    arrival_status_desc VARCHAR(100),

    flight_number VARCHAR(50) NOT NULL,
    operating_carrier_airline_id VARCHAR(50) NOT NULL,
    aircraft_code VARCHAR(50) )'''

    mycursor.execute(sql)
    mysqldb.commit()
    
  except mysqldb.connector.Error as error:
    print("Failed to create tables : {}".format(error))
  finally:
    if mysqldb.is_connected():
        mycursor.close()
        mysqldb.close()
        print("MySQL connection is closed")


