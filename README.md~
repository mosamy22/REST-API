# Linux Server Configuration-Project 3
### Project Overview
>> A baseline installation of a Linux server and prepare it to host web applications. Learning how to secure your server from a number of attack vectors, install and configure a database server, and deploy one of your existing web applications onto it.

### What did I learn?
>> I have learnt how to access, secure, and perform the initial configuration of a bare-bones Linux server. You will then learn how to install and conzfigure a web and database server and actually host a web application.

**Public IP Address:** 18.194.127.11 || **Accessible SSH port:** 2200

**[Find Live Project Here](http://www.18.194.127.11.xip.io)** 
_____________
To complete this project, you'll need a Linux server instance. I have used **[Amazon Lightsail](https://aws.amazon.com/lightsail)**. If you don't already have an Amazon Web Services account, you'll need to set one up. Once you've done that, Follow the steps to configure the server. Go through AWS tutorials if you feel need to.

## Steps to Configure Linux server
##### 1. Start a new Ubuntu Linux server instance on Amazon Lightsail. 
You can refer to the [documentation](https://aws.amazon.com/documentation/lightsail/) which will help you to get started. Also, you may want to have a look at [this](https://www.youtube.com/watch?v=hOAwg9jeRzg).
##### 2. Follow the instructions provided to SSH into your server.
There is a button on lightsail dashboard to directly SSH into your server.
You can also SSH into your machine using the private key.
* Download the private key provided in account section of AWS Lightsail.
* Use this command:
    ` $ ssh -i <privateKeyOfInstance.rsa> <Username>@<Public IP address>`
### Secure your server
##### 3. Update all currently installed packages.
```
$ sudo apt-get update
$ sudo apt-get upgrade
```
##### 4. Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).
```bash
$ sudo ufw default deny incoming
$ sudo ufw default allow outgoing
$ sudo ufw allow www
$ sudo ufw allow ntp
$ sudo ufw allow 2200/tcp
$ sudo ufw enable
```
##### 5. Change the SSH port from 22 to 2200.
Make sure to configure the **server firewall** before changing the port to 2200. Otherwise, you will lose your machine.
  * Locate the line **port 22** in the file */etc/ssh/sshd_config* and edit it to  **port 2200**, or any other desired port.
  * Restart the SSH service usign `$ sudo service ssh restart`.
##### 6. Creating a new user called `grader`, and generating a SSH key pair for `grader`.
* Add User grader
    ```
    $ sudo adduser grader
    ```
    Set its password if you want and fill other details.
* Give `Sudo` Access to grader
    ```
    $ sudo nano /etc/sudoers.d/grader
    ```
    * Edit and following line to this file
        ```
        grader ALL=(ALL)
        ```
* Generate a keypair and push it to server.
    Use your local machine to generate a key pair
    ```
    $ssh-keygen 
    ```
    Push it to server:
    Create `.ssh` directory in home of server machine. And follow the commands to       push and authorize the key for SSH login. 
    ```
    $ mkdir .ssh
    $ touch .ssh/authorized_keys
    ```
    Copy and paste the key from your local machine, usign vim editor:
    ```
    $ vim .ssh/authorized_keys
    ```
    Changing permission of `.ssh` and `.ssh/authorized_keys`
    ```
    $ chmod 700 .ssh
    $ chmod 644 .ssh/authorized_keys
    ```

### deploy your project :
##### 9. Configure the local timezone to UTC.
 * Change the timezone to UTC using following command: 
    ```
    $ sudo timedatectl set-timezone UTC
    ```
`You may need to take refrence from` [Digital ocean-Deploy a Flask App](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)`for furthur steps.`
##### 10. Install and configure Apache to serve a Python mod_wsgi application.
    $ sudo apt-get install apache2 libapache2-mod-wsgi
    
**Enable mod_wsgi:**
    ```
    $ sudo a2enmod wsgi
    ```
##### 11. Install and configure PostgreSQL:
* Installing Postgresql python dependencies
    ```
    $ sudo apt-get install libpq-dev python-dev
    ```
* Installing PostgreSQL:
    ```
    $ sudo apt-get install postgresql postgresql-contrib
    ```
* Create a new database user named **catalog** that has limited permissions to your     catalog application database.
    ```
    $ sudo su - postgres
    $ psql
   ```
    
    * Create a new database named *catalog*:    `# CREATE DATABASE catalog;`
    * Create a new user named *catalog*:    `# CREATE USER catalog;`
    * Set a password for catalog user:    `#  ALTER ROLE catalog with password 'password';`
    * Grant permission to catalog user:    `# GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;`
    * Exit from psql:    `# \q`
    * Return to grader using: `$ exit`

* Change the database connection to:
   ```
   engine = create_engine('postgresql://catalog:<password>@localhost/catalog')
   ```

##### 12. Install python-pip, Flask and other dependencies.
Find the package name: [Ubuntu Packages Search](https://packages.ubuntu.com)
   ```
    $ sudo apt-get install python-pip
    $ sudo pip install Flask
    $ sudo pip install sqlalchemy psycopg2 sqlalchemy_utils
    $ sudo pip install httplib2 oauth2client requests
   ```
##### 13. Install git and clone the project to /var/www/
* Make a *FlaskApp* named directory in /var/www/ and *catalog* in *FlaskApp*
    ```
      $ sudo mkdir /var/www/FlaskApp
      $ sudo mkdir /var/www/FlaskApp/catalog
    ```
* Make `grader` as ownner of that directory
    ```
     $ sudo chown -R grader:grader /var/www/FlaskApp
    ```
* Clone the **Item Catalog** and put them in the *FlaskApp/catalog* directory:
    ```
    $ git clone https://github.com/mosamy22/Item-Catalog.git
    ```
##### 14. Create the .wsgi file in *FlaskApp* to help apache to serve the FlaskApp
```
$ cd /var/www/FlaskApp/
$ sudo nano myapp.wsgi
```
* Add the following lines of code to the `.wsgi file`
```python
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp")

from catalog import app as application
```
**Now your directory structure should look like this:**
```
|--------/var/www/FlaskApp
|----------------catalog
|-----------------------static
|-----------------------templates
|---------------------- *other files*
|-----------------------__init__.py
|----------------myapp.wsgi
```
##### 16. Configure and Enable a New Virtual Host:
  ```
    $  sudo vim /etc/apache2/sites-available/000-default.conf
  ```
**Add the following lines of code to the file to configure the virtual host.**
This will also add path for server error logs and access error logs.
```xml
<virtualHost *:80>
    ServerName 'XXX.XXX.XXX.XXX'
    ServerAdmin mohamedsamyhasan486@gmail.com
    WSGIScriptAlias / /var/www/FlaskApp/myapp.wsgi
    <Directory /var/www/FlaskApp/catalog>
        Order allow,deny
        Allow from all
    </Directory>
    Alias /static /var/www/FlaskApp/catalog/static
    <Directory /var/www/FlaskApp/catalog/static/>
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>
```

Enable the virtual host with the following command:
```
$ sudo a2ensite 000-default
```
##### 17. Restart Apache to run the app on sever
```
$ sudo service apache2 reload
```

```
$ sudo service apache2 restart
```
   
### Refrences:
* [Digital Ocean - Deploy A Flask App on ubuntu Server](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
* [AWS documentation](https://aws.amazon.com/documentation/)
* [AWS Youtube Channel](https://www.youtube.com/user/AmazonWebServices)
* [Medium](https://medium.com/@manivannan_data/how-to-deploy-the-flask-app-as-ubuntu-service-399c0adf3606)
* [Ubuntu Forums](https://ubuntuforums.org)
* [Free Code Camp Radio - Chill tunes you can code to](https://www.youtube.com/watch?v=8gVrm3GtORY)
_____
🎩 Hat tip to everyone who helped me!
