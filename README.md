# NOLA Flood Impact

This is a continuation of a project that was started at a [Data Jam session at the 2018 National Planning Conference in New Orleans](https://planning.org/conference/datajam/), where the main topic was climate change and stormwater management in New Orleans. This is the main software repository for that DataJam.

## Getting Started

The project is written in [GeoDjango](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/), a geospatial extension to the Django web framework.

### Virtual Environment

Create a virtual environment using your preferred method. There is a `Pipfile`, so if you have [pipenv](https://docs.pipenv.org/) installed, you could do:

```bash
$ pipenv --three
$ pipenv install
```

to create and activate a virtual environment and install required Python packages. Most shell commands listed in this README from here on assume you have the virtual environment activated and all dependencies successfully installed.

### Database

The project uses [PostGIS](http://postgis.net) as the database. Installing PostGIS locally can be tricky, but if you have [Docker](https://www.docker.com/community-edition) installed and running, you can start a PostGIS container:

```bash
$ docker run --name nola-postgis \
              -e POSTGRES_USER=nola \
              -e POSTGRES_DATABASE=nola \
              -e POSTGRES_PASSWORD=nola
              -p 5432:5432 \
              mdillon/postgis:10
```

If all goes well, you should have a PostGIS instance accessible on your `localhost` at port 5432 and should be able to connect to it with the parameters specified above. These are also the default in `flood_impact/settings.py`, so you now should be able to run database migrations. Change into the `flood_impact` directory and type:

```bash
$ python manage.py migrate
```

### ETL required datasets

The project requires several datasets from [NOLA Open Data](https://data.nola.gov), specifically:

* [Site Address Point](https://data.nola.gov/d/awd4-9fzf)
* [Building Footprint](https://data.nola.gov/d/m3gg-u447)
* [Parcels](https://data.nola.gov/d/4tiv-n7fd)
* [Zoning Districts](https://data.nola.gov/d/25ka-xtj7)

The project includes an app called `etl` that should handle this for you (please open an issue if it does not!). This will eventually be turned into a [Django management command](https://docs.djangoproject.com/en/2.0/howto/custom-management-commands/), but until then you'll have to do it from an interactive shell:

```bash
$ python manage.py shell
```

```python
>>> from myimpact.load import load_all
>>> load_all()
```

It could take several minutes to finish, depending on your internet connection speed and computer processing power.

### Run Tests

TODO: write more of these

```bash
$ python manage.py test
```

### Run a Development Server

```bash
$ python manage.py runserver
```

You should now be able to access the proof-of-concept web form at http://localhost:8000/myimpact/ . That is the default, but you could change port or IP binding. For example, if you wanted to make it available to any device on your network on port 8181:

```bash
$ python manage.py runserver 0.0.0.0:8181
```
