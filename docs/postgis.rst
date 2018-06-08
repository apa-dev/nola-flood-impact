#######
PostGIS
#######

.. highlight:: bash

We use `PostGIS <http://postgis.net/>`_ for storing and analyzing spatial data. The easiest way to start up a local instance is to use `Docker <https://www.docker.com/community-edition>`_. If you have that installed and working, then it's as easy as::

   $ docker run --name nola-postgis \
                 -e POSTGRES_USER=nola \
                 -e POSTGRES_DATABASE=nola \
                 -e POSTGRES_PASSWORD=nola \
                 -p 5432:5432 \
                 mdillon/postgis:10
