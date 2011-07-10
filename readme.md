Como nos Sentimos
=================

This is a project made for the Data Visualization class at Universidade
Federal de Minas Gerais, thought by Raquel Cardoso de Melo Minardi.

It consists of a system that colects tweets filled with feelings in the
Portuguese language, proccesses them, store and visualize the result in
a joyful but yet informative and relevant visualization. What you see
here is the source code just for the visualization.

The whole project was heavily inspired by http://wefeelfine.org by
Jonathan Harris and Sep Kamvar.

Video Demo
----------

There is a video [live][youtubelink]. It is in Portuguese but you might
get the idea anyways.


System Configuration
--------------------

These instructions and the project itself were tested on Ubuntu Server
10.04.2 LTS

To start off, setup your basic dev system environment. Make sure you follow the on-screen instructions

    $ sudo apt-get install mysql-server python-setuptools subversion python-svn mercurial git-core python-git bzr python-dev libmysqlclient-dev python-mysqldb

Instal virtualenv and setup a clean environment

    $ sudo easy_intall virtualenv
    $ virtualenv --no-site-packages cns

Install the necessary python packages

    $ . cns/bin/activate
    $ pip install mysql-python ipython django django-tastypie twython geopy gunicorn south

Create a new database on MySQL

    $ mysql -uroot -p
    mysql> create database <name_of_the_db>;


Time to create the necessary tables for the Como nos Sentimos project and fill them with the necessary data.

    $ mysql -uroot -p <name_of_the_db_you_created> < helpfiles/twitter.sql
    $ mysql -uroot -p <name_of_the_db_you_created> < helpfiles/feelings.sql
    $ mysql -uroot -p <name_of_the_db_you_created> < helpfiles/states.sql
    $ mysql -uroot -p <name_of_the_db_you_created> < helpfiles/locations.sql


API Configuration
-----------------

Enter the `api` directory and edit your `local_settings.py`
according to your configurations

    $ cp local_settings.py.template local_settings.py

Make sure the Django Project sets itself on the DB

    $ ./manage.py syncdb

Finally, run the development server to see the API live!

    $ ./manage.py runserver 0.0.0.0:8000


Crawlers Configuration
----------------------

Enter the `backend` directory and edit both the `crawler_local_settings.py` and the `geocoder_local_settings.py` according to your system's configuration

    $ cp crawler_local_settings.py.template crawler_local_settings.py
    $ cp geocoder_local_settings.py.template geocoder_local_settings.py

Fetch sentimetal data from Twitter and get the locations of its authors!

    $ python crawler.py
    $ python geocoder.py


Processing Configuration
------------------------

The Processing code is located on the `processing` folder, and should run on major operating systems. To
download the Processing Sandbox please go to http://www.processing.org .

You need to download the SQLibrary by Florian Jenett at [this link][sqlibrary] and follow the
instructions on the same website.

You need to configure the file `mysql_settings.txt.template` to match
your database's configuration. Then simply rename the file:

    $ cp mysql_settings.txt.template mysql_settings.txt


[youtubelink]:http://www.youtube.com/watch?v=aKFtpb5e0ks
[sqlibrary]:http://bezier.de/processing/libs/sql/

