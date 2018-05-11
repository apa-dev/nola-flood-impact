import requests

from etl.data_config import socrata as socrata_config
from etl.models import SocrataCatalogItem


def get_nola_catalog():
    """Get the NOLA open data catalog

    Returns:
        dict
    """
    url = 'http://{}'.format(socrata_config.NOLA_OPENDATA_DOMAIN)
    if url.endswith('/'):
        url += 'data.json'
    else:
        url += '/data.json'
    req = requests.get(url)
    req.raise_for_status()
    return req.json()


def save_nola_catalog():
    """Main entrypoint. Get the catalog, and save them to the database,
    if they don't already exist.

    TODO: Adjust logic to archive old and save new if modified date
    newer than original modified date.
    """

    catalog = get_nola_catalog()
    for dataset in catalog['dataset']:
        existing = SocrataCatalogItem.objects.filter(identifier=dataset['identifier'])
        if existing.count() == 0:
            catalog_item = SocrataCatalogItem(
                    access_level=dataset.get('accessLevel'),
                    contact_point=dataset.get('contactPoint'),
                    description=dataset.get('description'),
                    distribution=dataset.get('distribution'),
                    identifier=dataset['identifier'],
                    issued=dataset.get('issued'),
                    landing_page=dataset.get('landingPage'),
                    modified=dataset.get('modified'),
                    publisher=dataset.get('publisher'),
                    title=dataset.get('title')
                    )
            catalog_item.save()
