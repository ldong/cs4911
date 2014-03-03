HumorGenomeWebApp
=================
### Setting up MySQL
These instructions will assume that you're using a Linux-based OS (the process is much different on Windows). First,
you will need to install the `mysql-server` package:

`sudo apt-get install mysql-server`

Towards the end of the installation, you will be asked to provide a password for the root user. You can use any password
you'd like here. Once MySQL is installed, we now need to create a new user for the Django framework to use. First, start
up your new SQL server: `mysql -u root -p`. Then, create the new user.

```
CREATE USER 'django'@'localhost' IDENTIFIED BY 'python27';
GRANT ALL PRIVILEGES ON *.* TO 'django'@'localhost' WITH GRANT OPTION;
```

You now have a new user for the Django framework to use. The password and username don't matter here as long as they
match what's found in the settings.py file of the project. The last step here is simply to create the database.

`CREATE DATABASE humor_genome;`

Now you can exit MySQL (`\q`) and continue on to running the server.

### Running the Web Server
The first time you run the server, you should first make sure that your database is in sync with the web server models.
First, navigate to the root directory of the Django project.

`./manage.py syncdb`

This should add any addition tables or columns that you may be missing. Now that everything is in sync, you can run the
server.

`./manage.py runserver`

Now you can navigate to the URL given as output to view the web portal. To view the admin portal, navigate to the `/admin`
branch. (e.g. `http://localhost:8000/admin`). From here, you can access the administrator CRUD for all of the objects
in the database.

### Notes

When you first start the application, the database will be empty (when the server is deployed, the database will persist).
To get around this, navigate to the admin portal and add a few objects to the database. As of right now, the registration
page has not been added. So, you can add some users manually through the admin portal as well (the admin login itself
will work for the regular site too). After this, you can navigate to the main page (`http://localhost:8000/WebPortal/`).
From here, you should be able to login, rate the humor content you just added, and navigate between each of them.

### MAC users

1. install virtualenvwrapper, django

2. brew install mysql

3. [Setting up mysql] (README.md#setting-up-mysql)

4. Add humor contents mannually before view the web portal

