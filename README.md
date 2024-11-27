# NOLA Flood Impact

![screenshot of city hall in app](https://raw.githubusercontent.com/apa-dev/nola-flood-impact/my-impact-calculator/screenshots/city_hall.png)

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
              -e POSTGRES_PASSWORD=nola \
              -p 5432:5432 \
              mdillon/postgis:10
```

If all goes well, you should have a PostGIS instance accessible on your `localhost` at port 5432 and should be able to connect to it with the parameters specified above. These are also the default in `flood_impact/settings.py`, so you now should be able to run database migrations. Change into the `flood_impact` directory and type:

```bash
$ python manage.py migrate
```

### ETL required datasets

The project requires several datasets from [NOLA Open Data](https://data.nola.gov), specifically:

* [Site Address Point](https://data.nola.gov/Geographic-Base-Layers/Site-Address-Point/hfvu-md72/about_data)
* [Building Footprint](https://data.nola.gov/Real-Estate-Land-Records/Building-Footprint/prh5-qsuf/about_data)
* [Parcels](https://data.nola.gov/dataset/Parcels/v9q5-fz7t/about_data)
* [Zoning Districts](https://data.nola.gov/Planning-Zoning/Zoning-Districts/bizp-xi7c/about_data)

The project includes an app called `etl` that should handle this for you (please open an issue if it does not!). This will eventually be turned into a [Django management command](https://docs.djangoproject.com/en/2.0/howto/custom-management-commands/), but until then you'll have to do it from an interactive shell:

```bash
$ python manage.py shell
```

```python
>>> from myimpact.load import load_all
>>> load_all()
```

It could take several minutes to finish, depending on your internet connection speed and computer processing power.

If you are re-running the data load you will need to purge the db first:

```python
>>> from myimpact.models import *
>>> SiteAddressPoint.objects.all().delete()
>>> BuildingFootprint.objects.all().delete()
>>> Parcel.objects.all().delete()
>>> ZoningDistrict.objects.all().delete()
```

### Run Tests

TODO: write more of these - *Not currently functional. Uses outdated endpoints.*

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

## Changelog

* Nov. 2024: Django and all packages updated. ETL changed to accomodate new nola.gov format (csv, no longer offering shapefiles).


## Known Issues

### Performance

* The autocomplete address dropdown [datalist](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/datalist) that suggests addresses as the user types could use some performance optimization. It uses the `full_address` field on the `SiteAddressPoint` model, which contains condominium units, if present, in one building. Those are unnecessary given that we only need the parcel and the building footprint. Using a combination of the `address_number` and `full_name` fields would reduce the amount of rows the ORM has to [search with PostgreSQL full text search](https://docs.djangoproject.com/en/2.0/ref/contrib/postgres/search/) 

### Usability

* The address entered in the search form must be an exact match to a `full_address` value in `SiteAddressPoint` - there is no fuzzy string matching or ranking. That is one reason for the autosuggset drop down. A user could enter a valid address, but if the `full_address` has "South" for an address direction and the user simply enters "S" it would not match
* Speaking of, the front-end currently does not display any error message if there is no exact match, it simply does nothing.

### Security

* [CSRF protection](https://docs.djangoproject.com/en/2.0/ref/csrf/) was disabled on the view for `/myimpact/address`, as Django was occasionally not setting a `document.cookie` during development, making it impossible to include a CSRF token with the `POST` request.
* The [Mapbox access token](https://www.mapbox.com/help/define-access-token/) is exposed. It's a public, read-only token associated with an account on the free tier, [limited to 50,000 views per month](https://www.mapbox.com/pricing/)
* Speaking of security, it is highly recommended to go through the [Django deployment checklist](https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/) before even considering deploying this on a public-facing site.
