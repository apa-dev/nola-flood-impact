Socrata Integration
===================

Get a token from https://dev.socrata.com/register

.. highlight:: python

Create a file in ``flood_impact/flood_impact`` called ``local_settings.py`` (should be in the same directory as the existing ``settings.py``), and add your token to it::

   SOCRATA_APP_TOKEN = 'mytoken'
