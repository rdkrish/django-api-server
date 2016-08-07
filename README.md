# django-api-server
A sample django API server

### Setup from scratch
  ```apt-get update && apt-get -y upgrade```
#### Django Installation and postgresql-contrib for db connectivity
* Install python pip and other required modules
      
      ```apt-get -y install python-pip python-dev libpq-dev postgresql-contrib```
* Install django, virtualenv and django rest framework
    
      ```pip install django django_extensions djangorestframework psycopg2 virtualenv```

#### Postgresql Installation
  ```apt-get -y install postgresql```
  
#### Redis Installation
  ```
apt-get update
apt-get -y install build-essential
apt-get -y install tcl8.5
wget http://download.redis.io/releases/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable
make
make install
  ```
##### Redis comes with the script to run in daemon mode
  ```
cd utils
sudo ./install_server.sh
  ```

  Select all the default values by pressing enter

####Install redis pip module to access redis from django server
	pip install redis

####To store config in a separate file, we need configobj
	pip install configobj
	
####Setup django  project in virtualenv
	virtualenv apiserver
	
#### Setup postgresql
  ```
service postgresql start
su - postgres
psql
  ```
  * Create database
  
    `create database <db_name>;`
  * Create database user and grant permissions
  
    ```
CREATE USER <db_user> WITH PASSWORD '<db_password>';
ALTER ROLE <db_user> SET client_encoding TO 'utf8';
ALTER ROLE <db_user> SET default_transaction_isolation TO 'read committed';
ALTER ROLE <db_user> SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <db_user>;
\q
    ```
  * Download and restore the dump
    
    Download the database dump from https://gist.github.com/jaisonplivo/2e8557d5a1c89e070162dca00ec7cb56
      
        wget https://gist.githubusercontent.com/jaisonplivo/2e8557d5a1c89e070162dca00ec7cb56/raw/d5791948d0e033dc2c08d5006f5801435b01e37d/testdatadump.txt
        psql <db_name> < testdatadump.txt
  * Alter the owners of the tables being restored
  
    ```
psql
ALTER TABLE account owner to <db_user>;
ALTER TABLE account_id_seq owner to <db_user>;
ALTER TABLE phone_number owner to <db_user>;
ALTER TABLE phone_number_id_seq owner to <db_user>;
\q
    ```

####Django setup
We need to migrate the models
  	
    cd apiserver
    python manage.py makemigrations
    python manage.py migrate
    
####Start the django server

  Before starting the django server, we need to update the app.conf file.
  Update all the entries in app.conf file to suit your setup located at apiserver/app.conf
    
    cd apiserver
    python manage.py runserver 0.0.0.0:8000

### Test the API behavior
  Let us first create a test_db in postgresql

##### Create database

    su - postgres
    psql
    create database test_<db_name>;
    \q

#####Restore the postgresql dump using
    
    psql <db_name> < testdatadump.txt

##### Alter the table owners to the newly created user

    psql
    ALTER TABLE account owner to <db_user>;
    ALTER TABLE account_id_seq owner to <db_user>;
    ALTER TABLE phone_number owner to <db_user>;
    ALTER TABLE phone_number_id_seq owner to <db_user>;
    \q

#####Run the tests

    cd apiserver
    python manage.py test --keepdb
    
NOTE: The testcases have been designed based on the data dump provided at https://gist.github.com/jaisonplivo/2e8557d5a1c89e070162dca00ec7cb56
