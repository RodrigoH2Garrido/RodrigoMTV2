 #! bin/bash
service mysql start

rootpsw='1234'
usertest='rodrigo_docker8'
passtest='Password123#@!'
tabletest='locations'

mysql -uroot -p$rootpsw <<MYSQL_SCRIPT
CREATE DATABASE $usertest;
CREATE USER '$usertest'@'localhost' IDENTIFIED BY '$passtest';
CREATE USER '$usertest'@'%' IDENTIFIED BY '$passtest';
GRANT ALL PRIVILEGES ON *.* TO '$usertest'@'localhost' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO '$usertest'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
MYSQL_SCRIPT

echo "MySQL user created."
echo "Username:"   $usertest
echo "Password:"   $passtest

#********************************************
# Now we connect to the MySQL database
# and execute the query from the shell script
#********************************************

#mysql -u$usertest -p$passtest -D$usertest <<MYSQL_SCRIPT 
#CREATE TABLE $tabletest (id int, name int, address int);
#INSERT INTO $tabletest (id, name, address) VALUES (1,2,3);
#MYSQL_SCRIPT

mysql -u$usertest -p$passtest -D$usertest <<MYSQL_SCRIPT
CREATE TABLE $tabletest (
id int primary key auto_increment,
place text,
points int,
lat text,
lng text,
zoom int);

LOAD DATA LOCAL INFILE 'zona8.txt' INTO TABLE locations CHARACTER SET utf8 FIELDS TERMINATED BY ',' LINES TERMINATED BY '|' ;

MYSQL_SCRIPT

service mysql stop
