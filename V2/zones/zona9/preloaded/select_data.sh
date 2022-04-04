 #! bin/bash
#service mysql start
#/etc/init.d/mysql start
service mysql start
rootpsw='1234'
usertest='rodrigo_docker9'
passtest='Password123#@!'
tabletest='locations'

#usertest='mydb'
#passtest='#1A2b%3C4d5E!'
#tabletest='mytab'

mysql -u$usertest -p$passtest -D$usertest -h 127.0.0.1 <<MYSQL_SCRIPT 
SELECT * FROM $tabletest;
MYSQL_SCRIPT

tail -F /var/log/mysql/error.log

