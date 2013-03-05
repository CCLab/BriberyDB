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

import types, settings

from django.db import connections

Q = {
  'event_actors': 'SELECT actor_id, name, types, roles FROM actors_events JOIN actors ON actor_id=actors.id WHERE event_id=%s;',

  'actors_like': 'SELECT * FROM actors WHERE name LIKE %s OR name LIKE %s ORDER BY name ASC;',

  'event' : 'SELECT * from events where id=%s;',

  'event_count': 'SELECT count(id) FROM events WHERE scandal_id=%s;',

  'refs':  'SELECT * FROM refs AS r WHERE r.id = ANY(%s);',

  'cases': 'SELECT id, name, description  FROM scandals;',

  'case_actors':  'SELECT DISTINCT actor_id, name FROM (actors_events JOIN events ON event_id=events.id) JOIN ACTORS ON actor_id=actors.id WHERE scandal_id=%s;',

  'actor': 'SELECT id,name,human FROM actors WHERE id=%s;', 
  
  }

def query (query_name, param, db='afery'):
  ''
  
  if type(param) in (types.ListType, types.TupleType):
    param = tuple(param)
  else:
    param = tuple((param,))
    
  cursor = connections[db].cursor()

  cursor.execute(Q[query_name], param)

  if settings.DEBUG:
    print cursor.query

  return cursor.fetchall()
