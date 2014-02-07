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
CREATE USER 'django'@'localhost' IDENTIFIED BY '<PASSWORD>';
GRANT ALL PRIVILEGES ON *.* TO 'django'@'localhost' WITH GRANT OPTION;
```

You now have a new user for the Django framework to use. The password and username don't matter here as long as they
match what's found in the settings.py file of the project.


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

### Example GUI
You can find an example GUI at the following location: http://www.prism.gatech.edu/~qguo8/
