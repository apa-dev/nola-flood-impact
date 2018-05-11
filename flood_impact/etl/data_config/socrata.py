import os

from django.conf import settings


# DO NOT include the http(s)://
NOLA_OPENDATA_DOMAIN = 'data.nola.gov'

# A dict of `title`: `slug` of key datasets from data.nola.gov that we
# are interested in
NOLA_DATASETS = [
        ('311 Calls (2012-Present)'                               , '3iz8-nghx') ,
        ('Boundary'                                               , 'g5g3-55cx') ,
        ('Building Footprint'                                     , 'm3gg-u447') ,
        ('Calls for Service 2018'                                 , '9san-ivhk') ,
        ('Census - 2010'                                          , 'u4yh-3wk9') ,
        ('Census 2010 - New Orleans Regional Planning Commission' , 'aird-4z7g') ,
        ('City Council Districts'                                 , 'dc69-ed6k') ,
        ('Code Enforcement All Cases'                             , 'u6yx-v2tw') ,
        ('Code Enforcement All Inspections'                       , 'uh5a-f7uw') ,
        ('Code Enforcement All Violations'                        , '3ehi-je3s') ,
        ('Council Districts Pre-2014'                             , 'rc5i-5hwb') ,
        ('DPW Projects'                                           , 't73j-rfp6') ,
        ('Dept. of Public Works RoadWork Projects'                , 'gbxh-56wk') ,
        ('Edge of Pavement (Line and Polygon)'                    , 'igww-2uzd') ,
        ('Evacuspots'                                             , 'ys6n-yuem') ,
        ('Festival Grounds'                                       , 's4g3-ky2w') ,
        ('Future Land Use'                                        , '66ys-xxcg') ,
        ('Lot'                                                    , '54dz-ss9h') ,
        ('Lot'                                                    , '92sr-5bi9') ,
        ('Master Street Name Table'                               , 'xizv-ihxa') ,
        ('NORA Sold Properties'                                   , 'hpm5-48nj') ,
        ('NORA Uncommitted Property Inventory'                    , '5ktx-e9wc') ,
        ('National Register of Historic Places Districts'         , 'x2jv-vjh6') ,
        ('Neighborhood Area Boundary'                             , '7svi-kqix') ,
        ('Neighborhood Conservation District'                     , 'w6ee-uym2') ,
        ('Neighborhood Statistical Areas'                         , 'c2j2-5qdf') ,
        ('Orleans Parish - Center of Waterway'                    , '2ytt-c2d9') ,
        ('Orleans Parish Boundary'                                , '5jjm-ygfn') ,
        ('Orleans Parish Landmass'                                , 'eqn9-sfv5') ,
        ('Overlay'                                                , 'ks2a-e4m8') ,
        ('Overlay Zoning Districts'                               , '4kce-8gm5') ,
        ('Parcels'                                                , '4tiv-n7fd') ,
        ('Permits'                                                , 'rcm3-fn58') ,
        ('Permits - BLDS'                                         , '72f9-bi28') ,
        ('Place Based Planning'                                   , 'ssw4-9pg7') ,
        ('Planning Districts'                                     , '3kp4-ecpw') ,
        ('Road Centerline'                                        , '3wh2-z5dr') ,
        ('Route Names'                                            , 'k6k3-kaiv') ,
        ('S&WB Projects'                                          , 'm6sf-i3xf') ,
        ('Sewerage & Water Board Projects'                        , 'jg5k-uvi2') ,
        ('Site Address Point'                                     , 'awd4-9fzf') ,
        ('Squares'                                                , 't5du-prgx') ,
        ('Urban Gardens'                                          , '6b2p-nf9y') ,
        ('Zip Code Tabulation Areas - 2010'                       , 'rgeq-44vf') ,
        ('Zone Area'                                              , 'eyjv-kpjj') ,
        ('Zoning Class'                                           , 'cy68-n8cp') ,
        ('Zoning District'                                        , '25ka-xtj7') ,
        ('Zoning Districts'                                       , 'iz3t-uee6') ,
        ('Zoning Overlay'                                         , 'yi5p-wwpg')
    ]


# TODO: Have option of using a S3 bucket or some other cloud object storage
# The directory to store downloaded distribution files
DATASTORE = os.path.join(settings.BASE_DIR, 'etl', 'datastore')

# The name of the directory in DATASTORE where original downloaded distribution
# files will be stored
DATASTORE_ORIG_NAME = 'orig'

# The name of the directory in DATASTORE where staged downloaded distribution
# files will be stored (e.g., unzipped contents of a zip file or some other
# alteration of an original downloaded file before further processing, such as
# loading into a database
DATASTORE_STAGING_NAME = 'staging'


# Mapping of mime types (`mediaType` from Socrata) to file extensions
MIME_EXTENSIONS = {
        'application/json': 'json',
        'application/zip': 'zip',
        'application/vnd.google-earth.kml+xml': 'kml',
        'application/vnd.google-earth.kmz': 'kmz',
        'text/csv': 'csv'
        }
