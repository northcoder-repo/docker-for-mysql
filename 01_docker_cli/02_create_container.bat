@echo off

REM run the mysql container, exposing the server
REM on localhost's port 3376:

docker create ^
  --publish 3376:3306 ^
  --name imdb_test ^
  --env MYSQL_ROOT_PASSWORD=put_it_here ^
  imdb_test:Dockerfile
