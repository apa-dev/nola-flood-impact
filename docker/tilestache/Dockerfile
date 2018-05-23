FROM python:2.7

WORKDIR /usr/src/TileStache

RUN pip install pillow modestmaps werkzeug uuid mapbox-vector-tile mapnik

RUN git clone https://github.com/TileStache/TileStache /usr/src/TileStache

RUN python setup.py install

EXPOSE 8080

ENTRYPOINT ./scripts/tilestache-server.py
