#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
#echo estoy en el install
MYSQL_ROOT_PASSWORD='1234' # SET THIS! Avoid quotes/apostrophes in the password, but do use lowercase + uppercase + numbers + special chars

# Install MySQL
# Suggestion from @dcarrith (http://serverfault.com/a/830352/344471):
echo debconf mysql-server/root_password password $MYSQL_ROOT_PASSWORD | debconf-set-selections
echo debconf mysql-server/root_password_again password $MYSQL_ROOT_PASSWORD | debconf-set-selections
#sudo debconf-set-selections <<< "mysql-server-5.7 mysql-server/root_password password $MYSQL_ROOT_PASSWORD"
#sudo debconf-set-selections <<< "mysql-server-5.7 mysql-server/root_password_again password $MYSQL_ROOT_PASSWORD"

apt-get -qq install mysql-server > /dev/null # Install MySQL quietly

service mysql start

echo service mysql status
# Create a database and user for loading data!!!!!!!!!!!!!
#usertest='mydb'
#PASS='12345678'

apt-get -qq install expect > /dev/null

# Build Expect script
tee ~/secure_our_mysql.sh > /dev/null << EOF
spawn $(which mysql_secure_installation)

expect "Enter password for user root:"
send "$MYSQL_ROOT_PASSWORD\r"

expect "Press y|Y for Yes, any other key for No:"
send "y\r"

expect "Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG:"
send "0\r"

expect "Change the password for root ? ((Press y|Y for Yes, any other key for No) :"
send "n\r"

expect "Remove anonymous users? (Press y|Y for Yes, any other key for No) :"
send "y\r"

expect "Disallow root login remotely? (Press y|Y for Yes, any other key for No) :"
send "y\r"

expect "Remove test database and access to it? (Press y|Y for Yes, any other key for No) :"
send "y\r"

expect "Reload privilege tables now? (Press y|Y for Yes, any other key for No) :"
send "y\r"

EOF

# Run Expect script.
# This runs the "mysql_secure_installation" script which removes insecure defaults.
expect ~/secure_our_mysql.sh

# Cleanup
rm -v ~/secure_our_mysql.sh # Remove the generated Expect script
#sudo apt-get -qq purge expect > /dev/null # Uninstall Expect, commented out in case you need Expect

echo "MySQL setup completed. Insecure defaults are gone. Please remove this script manually when you are done with it (or at least remove the MySQL root password that you put inside it."

#mysqlcheck -uroot -p$MYSQL_ROOT_PASSWORD --repair --all-databases

mysql –version 

sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mysql/mysql.conf.d/mysqld.cnf 
sed -i '/max_allowed_packet*/c\max_allowed_packet=1073741824' /etc/mysql/mysql.conf.d/mysqld.cnf 
sed -i '/key_buffer_size*/c\key_buffer_size=100M' /etc/mysql/mysql.conf.d/mysqld.cnf 
sed -i '/max_connections*/c\max_connections=400' /etc/mysql/mysql.conf.d/mysqld.cnf 
sed -i '/\[mysqld\]/a\# Skip reverse DNS lookup\nskip-name-resolve' /etc/mysql/mysql.conf.d/mysqld.cnf 

service mysql stop


