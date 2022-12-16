#!/bin/bash
docker-compose up -d mongodb

MYSQL_ROOT_PASSWORD=root docker-compose up -d mySqldb

CLIENT_ID=n64t2zjtu69beyj8eth6fkr2 CLIENT_SECRET=CutaFC2cgvgHV4xXBmYh GRANT_TYPE=client_credentials docker-compose up -d main

docker-compose run -it main

CLIENT_ID=n64t2zjtu69beyj8eth6fkr2 CLIENT_SECRET=CutaFC2cgvgHV4xXBmYh GRANT_TYPE=client_credentials python3 main.py

exit

docker-compose down

CLIENT_ID=n64t2zjtu69beyj8eth6fkr2 CLIENT_SECRET=CutaFC2cgvgHV4xXBmYh GRANT_TYPE=client_credentials docker-compose up 
