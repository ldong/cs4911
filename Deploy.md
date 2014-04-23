HumorGenomeWebApp
=========

## This project is powered by Django.

### Instruction steps
1. Must have python installed.

2. [Install virtualenv for python](https://github.storm.gatech.edu/jlee850/HumorGenomeWebApp/wiki/Setup-django-projects).

3. create a virtualenv directory for HumorGenome Project

4. Install django for humorGenome project `pip install django`

5. Run `git clone https://github.storm.gatech.edu/jlee850/HumorGenomeWebApp.git`

6. Setup MySQL database

    ```
    Install MySQL by the following command:
    shell> sudo yum install mysql-server 
    
    Starting and Stopping the MySQL Server
    Start the MySQL server with the following command:
    
    shell> sudo service mysqld start
    This is a sample output of the above command:
    
    Starting mysqld:[ OK ]
    You can check the status of the MySQL server with the following command:
    
    shell> sudo service mysqld status
    This is a sample output of the above command:
    
    mysqld (pid 3066) is running.
    Stop the MySQL server with the following command:
    
    shell> sudo service mysqld stop
    ```
    
    Any specific setup of the MySQL database please refer [setting up mysql](https://github.storm.gatech.edu/jlee850/HumorGenomeWebApp/raw/master/README.md/README.md#setting-up-mysql).

7. run `./manage.py syncdb`

8. run ./manage.py runserver

9. Route 80 port to HumorGenome django project using apache

### Steps runned in humor.vip.gatech.edu (aka Log file)
1. install apache `sudo yum install httpd `

2. install wsgi for django `sudo yum install mod_wsgi`

3. Config apache
    1. Edit /etc/httpd/conf/httpd.conf
    2. service httpd restart
4. 
```
django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named MySQLdb
```
solved by 'deactivate' from virtualenv, `yum install MySQL-python`, then run `python ../manage.py collectstatic`


#### References:
1. http://dev.mysql.com/doc/mysql-repo-excerpt/5.6/en/linux-installation-yum-repo.html
2. http://dev.antoinesolutions.com/apache-server
3. https://library.linode.com/frameworks/django-apache-mod-wsgi/centos-5#sph_configure-django-applications-for-wsgi
4. http://thecodeship.com/deployment/deploy-django-apache-virtualenv-and-mod_wsgi/
5. https://docs.djangoproject.com/en/1.4/howto/deployment/wsgi/modwsgi/

