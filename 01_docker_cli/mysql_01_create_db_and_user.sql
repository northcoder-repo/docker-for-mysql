-- create a database
create database if not exists `imdb`;
-- set up a new user with all privs for remote access 
-- but NOT suitable for production!:
create user 'user'@'%' identified with mysql_native_password by 'pass_goes_here';
grant all privileges on *.* to 'user'@'%' with grant option;
flush privileges;
