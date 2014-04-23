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

### Inital Database Load

To load the initial humor content to the database, first start up MySQL with the extra 	`--local-infile` parameter.

`mysql -u django -p --local-infile`

Now, switch to the `humor_genome` database and issue the following command. Make sure that your `WebPortal_humorcontent` table
is empty beforehand.

```
LOAD DATA LOCAL INFILE '/home/leonard/HumorGenomeWebApp/HumorGenomeWebApp/Humor_DB_Dump.sql' INTO TABLE
WebPortal_humorcontent FIELDS TERMINATED BY "," OPTIONALLY ENCLOSED BY '"' (url, message, contentType, title, 
createdBy_id, id, avgRating, numRatings, created, numFlags, flagRatio);
```

Replace the filepath above with the full absolute filepath to the .sql file in your directory. You can copy it over into /tmp
or something if you want to make it simple. Before doing this, you should also make sure you have your first user created. If
you've ran `./manage.py syncdb` before, you should have done this by creating the superuser. The first user in the DB will be
listed as the creator of the content.

### Notes

When you first start the application, the database will be empty (when the server is deployed, the database will persist).
To get around this, navigate to the admin portal and add a few objects to the database. After this, you can navigate to 
the main page (`http://localhost:8000/WebPortal/`). From here, you should be able to login, rate the humor content you just 
added, and navigate between each of them.

### Installing Numpy and Scikit-learn

In order to make the recommendation system work, you need to install Numpy and Scikit-learn. 
You can install them however you want it, but here is an easy reference for Linux users:
`http://scikit-learn.org/stable/install.html`

### About The Recommendation System

It is the best to illustrate with an example. Say Bob and Alice both rated 10 humors, and not Jihoon wants to rate the humor. 
He rates 7 humors and clicks the recommend button. The system finds an unrated humor that is close to Bob and Alice's favor.
Jihoon clicks the button again, the system finds the next unrated humor that is close to Bob and Alice's favor, and so on.

More technically, we are using the collaborative filtering algorithm, specifically non-negative matrix factorization with nearest neighbor, 
to recommend jokes. For more information about non-negative matrix factorization and its use, please refer to these documentations:
```
http://scikit-learn.org/stable/modules/decomposition.html#non-negative-matrix-factorization-nmf-or-nnmf 
http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.ProjectedGradientNMF.html#sklearn.decomposition.ProjectedGradientNMF
```
Currently, the system searches for 5 nearest neighbors. Using the transformed matrix (the result of non-negative matrix factorization),
it calculates averages of 5 neighbors, gets the maximum average rating, then recommends that humor to the current user.
It is important to note that we are filling missing ratings with 3's because our rating values range from 1 to 5 and 3's are the average of those.
There can be many tweaks to the algorithm such as filling in average ratings for missing ratings instead of 3's, using different number of neighbors,
and using different settings for non-negative matrix factorization. Customizing those will be included in the future work.

### MAC users

1. install virtualenvwrapper, django

2. brew install mysql

3. [Setting up mysql] (README.md#setting-up-mysql)

4. Add humor contents mannually before view the web portal

