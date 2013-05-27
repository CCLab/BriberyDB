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

import types, os

from psycopg2 import ProgrammingError

DJANGO = None

if 'DJANGO_SETTINGS_MODULE' in os.environ.keys():
  import settings
  from django.db import connections,transaction
  DJANGO = True

Q = {
  'event_actors': '''SELECT actor_id, name, types, roles, human, count(name)
    FROM actors_events
    JOIN actors ON actor_id=actors.id
    WHERE event_id=%s
    GROUP BY actors_events.actor_id,actors.name,actors_events.types,actors_events.roles,actors.human;''',

  'event_actors_count': '''SELECT count(name)
    FROM actors_events
    JOIN actors ON actor_id=actors.id
    WHERE event_id=%s;''',

  'actors_nonhuman_like': 'SELECT * FROM actors WHERE (name LIKE %s OR name LIKE %s) AND human=FALSE ORDER BY name ASC;',
  
  'actors_human_like': 'SELECT * FROM v_actors WHERE surname LIKE %s OR surname LIKE %s ORDER BY surname ASC;',

  'case_events': '''SELECT e.id, event_date, description, publication_date, type, refs, title, name AS location
    FROM (SELECT q.id AS id, event_date, description, publication_date, title, refs, location_id, name AS type, major
      FROM (SELECT id, event_date, description, publication_date, title, refs, location_id, UNNEST(types) AS type_id, major
        FROM events) AS q LEFT JOIN event_types ON q.type_id=event_types.id) AS e
        LEFT JOIN locations ON e.location_id=locations.id
        WHERE e.id=ANY(SELECT UNNEST(events) FROM scandals where id=%s) AND major=%s ORDER BY event_date;''',

  'case_num_events': '''select array_length(events,1) from scandals where id=%s;''',

  'actor_roles': '''SELECT DISTINCT s.id AS id, role, type, name[1] AS scandal FROM
    (SELECT event_id, role, name AS type FROM
      (SELECT event_id, name AS role, actor_type_id FROM
        (SELECT distinct event_id, UNNEST(roles) AS role_id, UNNEST(types) AS actor_type_id FROM actors_events
          WHERE actor_id=%s) AS ar
        LEFT JOIN actor_roles ON ar.role_id=id) AS ert
      LEFT JOIN actor_types ON actor_type_id=actor_types.id) AS event
  JOIN scandals AS s on event_id=ANY(s.events);''',

  'event': '''SELECT e.id, event_date, description, publication_date, type, refs, title, name, descriptive_date  AS location, type_id
      FROM (SELECT q.id AS id, event_date, description, publication_date, title, refs, location_id, name AS type, descriptive_date, type_id
            FROM (SELECT id, event_date, description, publication_date, title, refs, location_id, UNNEST(types) AS type_id, descriptive_date
                    FROM events) AS q LEFT JOIN event_types ON q.type_id=event_types.id) AS e
                            LEFT JOIN locations ON e.location_id=locations.id
                                    WHERE e.id=%s;''',
  
  
#  SELECT e.id, event_date, description, publication_date, type, refs, title, name AS location
#    FROM (SELECT q.id AS id, event_date, description, publication_date, title, refs, location_id, name AS type
#      FROM (SELECT id, event_date, description, publication_date, title, refs, location_id, UNNEST(types) AS type_id
#        FROM events) AS q LEFT JOIN event_types ON q.type_id=event_types.id) AS e
#        LEFT JOIN locations ON e.location_id=locations.id
#        WHERE e.id=%s;''',

  'event_count': 'SELECT count(id) FROM events WHERE scandal_id=%s;',

  'event_types': '''SELECT id,name
    FROM event_types
    WHERE id = ANY (SELECT UNNEST(types) FROM events WHERE id=1);''',

  'event_refs': '''SELECT id, art_title, pub_title, pub_date, access_date, url
    FROM refs WHERE id = aNY (SELECT UNNEST(refs) FROM events WHERE id=%s);''',

  'event_case_title': '''SELECT name from scandals where %s=any(events);''', 
  
  'refs':  'SELECT * FROM refs AS r WHERE r.id = ANY(%s);',

#  plain cases
#  'cases': 'SELECT id, name, description, background, consequences, types, fields, events  FROM scandals;',

  # cases sorted by earlier events
  
  'cases': '''SELECT * FROM (SELECT DISTINCT ON (s.id)
    s.id, s.name, s.description, s.background, s.consequences, s.types, s.fields, s.events, event_date
    FROM (SELECT id, name, description, background, consequences, types, fields, events, UNNEST (events) AS event_id
      FROM scandals) AS s LEFT JOIN events AS e ON s.event_id=e.id ORDER BY s.id,event_date) as scandals ORDER BY event_date DESC;''',

  'cases_type': 'SELECT id, name, description, background, consequences, types, fields, events FROM scandals WHERE %s=ANY(types);',
  'cases_field': 'SELECT id, name, description, background, consequences, types, fields, events FROM scandals WHERE %s=ANY(fields);',
  'cases_type_field': 'SELECT id, name, description, background, consequences, types, fields, events FROM scandals WHERE %s=ANY(types) AND %s=ANY(fields);',
  'case_actors':  '''SELECT DISTINCT actor_id, name, count(actor_id) AS count
    FROM (actors_events JOIN events ON event_id=events.id)
    JOIN actors ON actor_id=actors.id
    WHERE event_id=ANY(SELECT UNNEST(events) FROM scandals WHERE id=%s)
    GROUP BY actors_events.actor_id, actors.name ORDER BY count DESC;;''',

  'actor': 'SELECT id,name,human FROM actors WHERE id=%s;', 
  'actors': 'SELECT id,name,human FROM actors WHERE id=%s;', 
  'roles' : 'SELECT id,name,human FROM actor_roles;',
  'events_types': 'SELECT id, name FROM event_types;', 
  'locations': 'SELECT id,name from locations;',
#  'actor_roles': '''SELECT ar.id,ar.name,scandal_id,u.name FROM
#    (SELECT DISTINCT scandal_id,name,unnest(roles) FROM actors_events AS ae JOIN
#      (SELECT scandal_id,s.name,ee.id FROM events AS ee JOIN scandals AS s ON scandal_id=s.id)
#      AS e ON event_id=e.id WHERE actor_id=%s)
#    AS u JOIN actor_roles AS ar ON u.unnest=ar.id ORDER BY ar.id;''',

  'actor_event_types': '''SELECT id, name, human FROM actor_types
    WHERE id = ANY(SELECT UNNEST(types) FROM actors_events WHERE actor_id=%s AND event_id=%s);''',

  'actor_event_roles': '''SELECT id, name, human FROM actor_roles
    WHERE id = ANY(SELECT UNNEST(roles) FROM actors_events WHERE actor_id=%s AND event_id=%s);''',

  'actor_event_affiliations': '''SELECT id, name, human FROM actor_affiliations
    WHERE id = ANY(SELECT UNNEST(affiliations) FROM actors_events WHERE actor_id=%s AND event_id=%s);''',

  'prev_event': '''select id, event_date, title from events 
    where id=any(select unnest(events) from scandals where %s=any(events))
    AND event_date < (SELECT event_date FROM events WHERE id=%s) 
    ORDER BY event_date DESC LIMIT 1;''',

  'next_event': '''SELECT id, event_date, title FROM events
    where id=any(select unnest(events) from scandals where %s=any(events))
    AND event_date > (SELECT event_date FROM events WHERE id=%s) 
    ORDER BY event_date ASC LIMIT 1;''',

  'scandal_types': '''SELECT id,name,parent
    FROM scandal_types
    WHERE id = ANY(SELECT UNNEST(types) FROM scandals WHERE id=%s);''',

  'scandal_fields': '''SELECT id,name,parent_id
    FROM scandal_field
    WHERE id = ANY(SELECT UNNEST(fields) FROM scandals WHERE id=%s);''',

  'nonhuman_actor_list': '''SELECT DISTINCT actors.id, actor, name AS affiliation FROM
    (SELECT actor_id AS id, name AS actor, unnest(affiliations) AS affiliation_id FROM actors_events AS ae
      LEFT JOIN actors AS a ON ae.actor_id=a.id) AS actors LEFT JOIN
        actor_affiliations ON actors.affiliation_id=actor_affiliations.id WHERE human=FALSE
        GROUP BY affiliation,actors.id,actors.actor;''',
  

  'get_case' : ''' SELECT id, name, description, background, types, fields from scandals where id=%s;''', 
  
  'create_case': '''INSERT INTO scandals (id, name, description, background, types, fields) 
    VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING id;''', 
    
  'update_case': '''UPDATE scandals SET name=%s, description=%s, background=%s, types=%s, fields=%s WHERE id=%s;''',

  'case_types': 'SELECT id, name from scandal_types;',

  'case_fields': 'SELECT id, name from scandal_field;',

  'case_events_list': 'SELECT events FROM scandals WHERE id=%s;',

  'case_update_events': 'UPDATE scandals SET events=%s WHERE id=%s;',

  'all_actors': 'SELECT id, name FROM actors ORDER BY human, name;',

  'all_actor_types': 'SELECT id,name FROM actor_types ORDER BY name, human;',
  'all_actor_roles': 'SELECT id,name FROM actor_roles ORDER BY name, human;',
  'all_actor_affiliations': 'SELECT id,name FROM actor_affiliations ORDER BY name, human;',  
  'all_actor_secondary_affiliations': 'SELECT id,name FROM secondary_affiliations ORDER BY name, human;',    
  
  'letters': '''SELECT ARRAY
    (SELECT * FROM (SELECT DISTINCT LEFT(surname,1) AS letter FROM v_actors)
      AS l WHERE LENGTH(letter)=1 ORDER BY letter) AS letters;''',

  'create_event': '''insert into events (id, title, types, description, event_date, major, descriptive_date) 
     VALUES (DEFAULT, %s,%s,%s,%s,%s,%s) RETURNING id;''', 
  
  'update_event': 'UPDATE events SET title=%s, types=%s, description=%s, event_date=%s, major=%s, descriptive_date=%s where id=%s;',

  'create_actor': 'INSERT INTO actors (id, name, human) VALUES (DEFAULT, %s, %s) RETURNING id;',

  'update_actor': 'UPDATE actors set name=%s, human=%s WHERE id=%s;',  

  'assign_actor': '''INSERT INTO actors_events (event_id, actor_id, types, roles, affiliations, secondary_affiliations, primary, secondary)
     VALUES (%s, %s, %s, %s, %s, %s, %s, %s);''', 

  'case_actor_events_metadata': '''select types, roles, affiliations, secondary_affiliations 
    from actors_events where event_id in (select unnest(events) from scandals where id=%s)
    AND actor_id=%s;''',

  'event_refs': 'SELECT refs from events where id=%s;',
  'create_ref': '''INSERT INTO refs (id, art_title, pub_title, url, pub_date, access_date)
     VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING id;''',
   'update_event_refs': 'UPDATE events SET refs=%s WHERE id=%s;',

  'create_attribute_human': 'INSERT INTO <table> (id, name, human) VALUES (DEFAULT, %s, %s) RETURNING id;',
  'create_attribute': 'INSERT INTO <table> (id, name) VALUES (DEFAULT, %s) RETURNING id;',  

  'full_event_refs': '''select art_title,pub_title,pub_date,access_date,url 
    from refs where id=any(select unnest(refs) from events where id=%s);''',

  'create_related' : 'INSERT INTO related_actors (actor, affiliation, secondary) VALUES (%s, %s, %s);', 
  
  'related_actors': '''select distinct id,name from (select actor_id from (select distinct unnest(affiliations) as af_id from actors_events where actor_id=%s) as af left join actors_events as ae on af_id = any(ae.affiliations)) as ai left join actors on actor_id=actors.id where id!=%s;''',
  }

#  SELECT scandal_id,ar.id,ar.name FROM
#  (SELECT DISTINCT scandal_id,unnest(roles) FROM actors_events AS ae JOIN events AS e ON event_id=e.id
#  WHERE actor_id=%s) AS u JOIN actor_roles AS ar ON u.unnest=ar.id ORDER BY ar.id;''',

  
#  #'SELECT * FROM (SELECT DISTINCT UNNEST(roles) FROM actors_events WHERE actor_id=%s ORDER BY unnest) AS u JOIN actor_roles AS ar ON u.unnest=ar.id;'  }

def query (query_name, param=None, db='afery', connection=None, special=None):

  '''Run the chosen query against the named database, return a sequence of
  rows.  If DJANGO_SETTINGS_MODULE environment variable is set, it uses the
  database connection specified in Django site settings module.  If there is
  not, supply psycopg2's connection object as connection parameter.
  
  when <special> is true, the first data element is parsed into the query as table name
   
  THIS IS INSECURE
  '''
  
  if type(param) in (types.ListType, types.TupleType):
    param = tuple(param)
  else:
    param = tuple((param,))
    
  if DJANGO:
    cursor = connections[db].cursor()
  else:
    cursor = connection.cursor()

  q = Q[query_name]
  if special and '<table>' in q:
    q = q.replace('<table>',param[0])
    param = param[1:]
  cursor.execute(q, param)

  if settings.DEBUG:
    print cursor.query
  try:
    result = cursor.fetchall()
  except ProgrammingError: #ugly
    result = None
  if DJANGO:
    transaction.commit_unless_managed(using=db)

  return result
#    result = [ data if isinstance(data, unicode) else data.decode('utf-8') for data in row]
#    result.append(tuple(data))
#  return tuple(result) 


if __name__ == '__main__':
  pass
