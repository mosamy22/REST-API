# REST API
### Project Overview
>> A simple secure API for hosting some survies created by Python with Flask framework and SQLALCHEMY , the database for this API is postgresql.
## Steps to Run this App


##### 1. install SQLALCHEMY , Postgresql and python flask backages  . 
    $ sudo apt-get install python-pip
    $ sudo pip install Flask
    $ sudo pip install sqlalchemy psycopg2 sqlalchemy_utils
    $ sudo pip install httplib2 oauth2client requests
* Installing Postgresql python dependencies
    ```
    $ sudo apt-get install libpq-dev python-dev
    ```
* Installing PostgreSQL:
    ```
    $ sudo apt-get install postgresql postgresql-contrib
    ```
* Create a new database user named **survey** that has limited permissions to your API database.
    ```
    $ sudo su - postgres
    $ psql
   ```
    
    * Create a new database named *survey*:    `# CREATE DATABASE survey;`
    * Create a new user named *survey*:    `# CREATE USER survey;`
    * Set a password for survey user:    `#  ALTER ROLE survey with password 'password';`
    * Grant permission to survey user:    `# GRANT ALL PRIVILEGES ON DATABASE survey TO survey;`
    * Exit from psql:    `# \q`
    * Return to grader using: `$ exit`


##### 2. Follow the below instructons after configuring postgres database.
 
* Use the below command to create the database model:
    ` $ python model.py`

* Use the below command to put dummy data on the database:
    ` $ python dummy.py`

* Use the below command to RUN the server:
    ` $ python survey.py`

-- it will run on the http://localhost:5000/ 

##### 3. you should register before using this API by sending a post request as shown below to the http://localhost:5000/users :

-{"username" : "" , "password" : ""}

##### 4. Sending post requests by the below format to this url http://localhost:5000/survey:
-
{
	"name" : "name",
	"description : "description",
	"question" : ["question","body","note"],
	"start_date" : "YY/MM/DD HH:MM",
	"start_date" : "YY/MM/DD HH:MM"
}

##### 5. to get a specified survey you should enter its id on the url http://localhost:5000/survey/id.





