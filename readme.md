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


Requirements
------------

This is Processing code, and should run on major operating systems. To
download the Processing Sandbox please go to http://www.processing.org .

The visualization gets its data from a MySQL database. More information
on that is yet to come. Therefore, you need to download the SQLibrary by
Florian Jenett at [this link][sqlibrary] and follow the
instructions on the same website.


Configuration
-------------

You need to configure the file `mysql_settings.txt.template` to match
your database's configuration. Then simply rename the file:

    mv mysql_settings.txt.template mysql_settings.txt


Video Demo
----------

There is a video [live][youtubelink]. It is in Portuguese but you might
get the idea anyways.


[youtubelink]:http://www.youtube.com/watch?v=aKFtpb5e0ks
[sqlibrary]:http://bezier.de/processing/libs/sql/
