# /usr/bin/env python

''' ORM module for afery

This is a simple encapsulation of database queries in the 'afery' app.

Due to half of the application developed using Flask/Bottle.py, and
the presentation app utilizing Django, all database queries MUST be
stored in this module and referenced using a name.

Django 'default' database is used for framework stuff, all queries
should go to the original app database, defined in Django settings.py
as alternative database named 'afery'.

'''

from django.db import connections

Q = { }

def query (query_name, parameter, db='afery'):

  pass
  
