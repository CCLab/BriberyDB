# Create your views here.

import orm

from django.http import HttpResponse as HTTPResponse

from django.template import Context, RequestContext, loader, Template

from django.db import connections

# not views

def get_scandal (scandal_id, db='afery'):

  cursor = connections[db].cursor()
  cursor.execute("SELECT name, description, background FROM scandals WHERE id=%s;", (scandal_id,))
  return cursor.fetchall()

def get_events (scandal_id, db='afery'):

  ''' id  | description | scandal_id | location_id | event_date | publication_date | type_id | subtype_id | types | refs | title | description                                                                                                                                                                                                                                                                                     | scandal_id | location_id | event_date | publication_date | type_id | subtype_id | types | refs | title'''
                
  cursor = connections[db].cursor()
  cursor.execute ("SELECT id, event_date, description, publication_date, types, refs, title FROM events WHERE scandal_id=%s ORDER BY event_date ASC;", (scandal_id,))

  return cursor.fetchall ()

def get_event_actors (event_id, db='afery'):

  cursor = connections[db].cursor()
  
  cursor.execute ("SELECT actors.name,affiliations FROM actors_events JOIN actors ON actors_events.actor_id=actors.id where event_id=%s;",(event_id,))

  return cursor.fetchall ()
            
def get_case_actors (object_id, db='afery'):

  QUERY = "SELECT DISTINCT actor_id, name FROM (actors_events JOIN events ON event_id=events.id) JOIN ACTORS ON actor_id=actors.id WHERE scandal_id=%s"

  #"SELECT DISTINCT actor_id,name FROM (actors JOIN actors_events ON actor_id = actors_events.actor_id) RIGHT JOIN events ON event_id = events.id WHERE scandal_id=%s;"
  
  cursor = connections[db].cursor()

  cursor.execute (QUERY, (object_id,))

  return cursor.fetchall()

# views


def case (request, object_id):

  'single scandal view'
  
#  cursor = connections['afery'].cursor()
#  cursor = connections['kuku'].cursor()

  scandal = get_scandal(object_id)
  events = get_events (object_id)

#  print events[0]

  if events:
    ujawnienie = (events[0], get_event_actors(events[0][0])[:5],
                   len (get_event_actors(events[0][0])))

  else:
    ujawnienie = (None, None, None)
    
  result = {} 
  
  result['name'] = scandal [0][0][0]
  result['names'] = scandal [0][0][1:]
  result['description'] = scandal [0][1]
  result['background'] = scandal[0][2]
  result['num_events'] = len(events)
  result['event_leak'] = ujawnienie
  result['events'] = [ (e, get_event_actors(e[0])[:5], len(get_event_actors(e[0])))
                       for e in events[1:]]
   
  result['all_actors'] = get_case_actors(object_id)

  result['tab'] = 1
  print result['events']
  
  template = loader.get_template ('afera.html')

  return HTTPResponse (template.render(Context(result))  )
  

def cases (request):

  cases = orm.query('cases', None)
  result = []

  for c in cases:

    case = dict(id=c[0],title=c[1], description=c[2])
    actors = orm.query('case_actors', c[0])
    case['events'] = orm.query('event_count', c[0])[0][0]
    case['actors'] = actors[:5]
    case['num_actors'] = len(actors)
    result.append(case)
    print case

  template = loader.get_template ('afery.html')

  return HTTPResponse (template.render(Context(dict(cases=result,tab=1)))  )



def event (request, object_id):

  event = orm.query('event', object_id)[0]

  if event:

    refs = orm.query('refs','{'+','.join([str(i) for i in event[9]])+'}')

  result = dict(refs=refs, event=event)

  result['tab'] = 1

  template = loader.get_template("wydarzenie.html")

  return HTTPResponse (template.render(Context(result)))
