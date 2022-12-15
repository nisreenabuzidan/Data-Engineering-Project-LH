#!/bin/bash


docker-compose up -d mongodb

MYSQL_ROOT_PASSWORD=root docker-compose up -d mySqldb

CLIENT_ID=n64t2zjtu69beyj8eth6fkr2 CLIENT_SECRET=CutaFC2cgvgHV4xXBmYh GRANT_TYPE=client_credentials docker-compose up main

docker exec -it main bash




docker image build ./docker -t main:latest


docker container run -it --name main --mount type=volume,src=app,dst=./code 
docker container run -it main:latest