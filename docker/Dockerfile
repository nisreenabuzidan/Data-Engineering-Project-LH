
FROM debian:latest 
WORKDIR /app/
RUN apt-get update && apt-get install python3-pip -y
RUN pip3 install requests
RUN pip3 install pandas
RUN pip3 install pymongo
RUN pip3 install utils
RUN pip install dash
RUN python3 -m pip install mysql-connector-python
RUN pip install matplotlib
RUN pip3 install fastapi uvicorn
#CMD python3 main.py


#FROM python:3.7
#WORKDIR /app/
#RUN apt-get update && apt-get install python3-pip -y
#RUN pip3 install fastapi uvicorn
#CMD ["uvicorn", "--host", "0.0.0.0", "--reload", "--reload-dir", "/app", "api:api"]
#CMD [-c 'while !</dev/tcp/lufthansa-airLines-sqldb/3306; do sleep 1; done; uvicorn", "--host", "0.0.0.0", "--reload", "--reload-dir", "/app", "api:api']
