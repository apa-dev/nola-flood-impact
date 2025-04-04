# -*- coding: utf-8 -*-
"""
Django settings for flood_impact project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wb$x(a1ff8y843m7kgqwg0o)ny6ug1)j*78^5g2i9y=x=dzdl7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework_gis',
    'etl',
    'myimpact'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flood_impact.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'flood_impact.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'nola',
        'USER': 'nola',
        'PASSWORD': 'nola',
        'HOST': 'localhost',
        # to avoid host machine postgres install (port 5432) conflict. run docker postgis with external port 5442
        'PORT': 5442
        # 'PORT': 5432
    }
}


# Custom User model, for more flexibility if needed later
# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = 'myimpact.User'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# https://docs.djangoproject.com/en/2.0/topics/auth/passwords/
PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.Argon2PasswordHasher',
        'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        ]

# Get a token from
# https://dev.socrata.com/register
# Not strictly necessary, but a good idea
# Create a file called local_settings.py in the same directory
# as this settings.py file and add
# SOCRATA_APP_TOKEN = 'mytoken'
# to it
SOCRATA_APP_TOKEN = None


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'


# NAD83 / Louisiana South (ft US) EPSG Code
LOUISIANA_SOUTH_EPSG = 3452

COVER_TYPES = (
        # (IDENTIFIER, Title, Runnoff curve number)
        # see: https://en.wikipedia.org/wiki/Runoff_curve_number
        ('IMPERVIOUS'         , 'Impervious Area'                 , 98) ,
        ('OPEN_SPACE'         , 'Open Space - Average'            , 85) ,
        ('COMMERCIAL'         , 'Commercial / Business'           , 95) ,
        ('INDUSTRIAL'         , 'Industrial'                      , 93) ,
        ('URBAN_RES'          , 'Urban Residential: <1/8 acre'    , 92) ,
        ('SUBURBAN_RES_SMALL' , 'Suburban Residential: <1/4 acre' , 87) ,
        ('SUBURBAN_RES_LARGE' , 'Suburban Residential: 1/3 acre'  , 86) ,
        ('RURAL_RES_SMALL'    , 'Rural Residential: 1/2 acre'     , 85) ,
        ('RURAL_RES_MID'      , 'Rural Residential: 1 acre'       , 84) ,
        ('RURAL_RES_LARGE'    , 'Rural Residential: 2 acre'       , 82) ,
        )

# Mapping models.ZoningDistrict.zone_description to a COVER_TYPE Identifier
# FIXME: The question marks in Trem? and Carr? should be an acute-accented e (é) but the
# zoning shapefile uses some weird character encoding (seemingly neither the shapefile standard
# of iso-8859-1 nor utf-8)
NOLA_ZONING_COVER_TYPE_MAPPING = {
        "Auto-Oriented Commercial District"                                             : "COMMERCIAL",
        "Business-Industrial Park District"                                             : "INDUSTRIAL",
        "CBD-1 Core Central Business District"                                          : "COMMERCIAL",
        "CBD-2 Historic Commercial and Mixed-Use District"                              : "COMMERCIAL",
        "CBD-3 Cultural Arts District"                                                  : "COMMERCIAL",
        "CBD-4 Exposition District"                                                     : "COMMERCIAL",
        "CBD-5 Urban Core Neighborhood Lower Intensity Mixed-Use District"              : "URBAN_RES",
        "CBD-6 Urban Core Neighborhood Mixed-Use District"                              : "URBAN_RES",
        "CBD-7 Bio-Science District"                                                    : "INDUSTRIAL",
        "Educational Campus District"                                                   : "SUBURBAN_RES_LARGE",
        "General Commercial District"                                                   : "COMMERCIAL",
        "General Planned Development District"                                          : "COMMERCIAL",
        "Greenway Open Space District"                                                  : "OPEN_SPACE",
        "Heavy Commercial District"                                                     : "COMMERCIAL",
        "Heavy Industrial District"                                                     : "INDUSTRIAL",
        "High Intensity Mixed-Use"                                                      : "COMMERCIAL",
        "High Intensity Mixed-Use District"                                             : "COMMERCIAL",
        "Historic Marigny/Trem?/Bywater Commercial District"                            : "COMMERCIAL",
        "Historic Marigny/Trem?/Bywater Mixed-Use District"                             : "COMMERCIAL",
        "Historic Marigny/Trem?/Bywater Residential District"                           : "URBAN_RES",
        "Historic Urban Multi-Family Residential District"                              : "URBAN_RES",
        "Historic Urban Neighborhood Business District"                                 : "COMMERCIAL",
        "Historic Urban Neighborhood Mixed-Use District"                                : "COMMERCIAL",
        "Historic Urban Single-Family Residential District"                             : "URBAN_RES",
        "Historic Urban Two-Family Residential District"                                : "URBAN_RES",
        "Life Science Mixed-Use District"                                               : "INDUSTRIAL",
        "Light Industrial District"                                                     : "INDUSTRIAL",
        "Maritime Industrial District"                                                  : "INDUSTRIAL",
        # The "MIxed" is how it is in the shapefile
        "Maritime MIxed-Use District"                                                   : "COMMERCIAL",
        "Medical Campus District"                                                       : "INDUSTRIAL",
        "Medical Service District"                                                      : "INDUSTRIAL",
        "Medium Intensity Mixed-Use District"                                           : "COMMERCIAL",
        "Natural Areas District"                                                        : "OPEN_SPACE",
        "Neighborhood Open Space District"                                              : "OPEN_SPACE",
        "Regional Open Space District"                                                  : "OPEN_SPACE",
        "Rural Residential Estate District"                                             : "RURAL_RES_MID",
        "Suburban Business District"                                                    : "COMMERCIAL",
        "Suburban Lake Area General Commercial District"                                : "COMMERCIAL",
        "Suburban Lake Area High-Residential District"                                  : "SUBURBAN_RES_SMALL",
        "Suburban Lake Area High-Rise Multi-Family Residential District"                : "SUBURBAN_RES_SMALL",
        "Suburban Lake Area Low-Rise Multi-Family Residential District"                 : "SUBURBAN_RES_SMALL",
        "Suburban Lake Area Marina District"                                            : "COMMERCIAL",
        "Suburban Lake Area Neighborhood Business District"                             : "COMMERCIAL",
        "Suburban Lake Area Neighborhood Park District"                                 : "OPEN_SPACE",
        "Suburban Lake Vista Two-Family Residential District"                           : "SUBURBAN_RES_SMALL",
        "Suburban Lake Vista and Lake Shore Single-Family Residential District"         : "SUBURBAN_RES_LARGE",
        "Suburban Lakeview Single-Family Residential District"                          : "SUBURBAN_RES_LARGE",
        "Suburban Lakewood and Country Club Gardens Single-Family Residential District" : "SUBURBAN_RES_LARGE",
        "Suburban Lakewood/Parkview Two-Family Residential District"                    : "SUBURBAN_RES_LARGE",
        "Suburban Multi-Family Residential District"                                    : "SUBURBAN_RES_SMALL",
        "Suburban Neighborhood Mixed-Use District"                                      : "COMMERCIAL",
        "Suburban Pedestrian-Oriented Corridor Business District"                       : "COMMERCIAL",
        "Suburban Single-Family Residential District"                                   : "SUBURBAN_RES_LARGE",
        "Suburban Two-Family Residential District"                                      : "SUBURBAN_RES_LARGE",
        "Vieux Carr? Commercial District"                                               : "COMMERCIAL",
        "Vieux Carr? Entertainment District"                                            : "COMMERCIAL",
        "Vieux Carr? Park District"                                                     : "OPEN_SPACE",
        "Vieux Carr? Residential District"                                              : "URBAN_RES",
        "Vieux Carr? Service District"                                                  : "INDUSTRIAL"
        }

# Include local_settings if present
try:
    from .local_settings import *
except ImportError:
    pass
