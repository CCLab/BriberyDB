# Create your views here.

from django.http import HttpResponse as HTTPResponse

from django.template import Context, RequestContext, loader, Template

from django.db import connections

# not views

def get_scandal (scandal_id, db='afery'):

  cursor = connections[db].cursor()
  cursor.execute("SELECT name,description,background  FROM scandals WHERE id=%s;", (scandal_id,))
  return cursor.fetchall()

def get_events (scandal_id, db='afery'):

  ''' id  | description | scandal_id | location_id | event_date | publication_date | type_id | subtype_id | types | refs | title | description                                                                                                                                                                                                                                                                                     | scandal_id | location_id | event_date | publication_date | type_id | subtype_id | types | refs | title'''
                
  cursor = connections[db].cursor()
  cursor.execute ("SELECT id, event_date, description, publication_date, types, refs FROM events WHERE scandal_id=%s ORDER BY event_date ASC;", (scandal_id,))

  return cursor.fetchall ()

def get_event_actors (event_id, db='afery'):

  cursor = connections[db].cursor()
  
  cursor.execute ("SELECT actors.name,affiliations FROM actors_events JOIN actors ON actors_events.actor_id=actors.id where event_id=%s;",(event_id,))

  return cursor.fetchall ()
            
# views


def case (request, object_id):

  'single scandal view'
  
#  cursor = connections['afery'].cursor()
#  cursor = connections['kuku'].cursor()

  scandal = get_scandal(object_id)
  events = get_events (object_id)

#  print events[0]

  if events:
    ujawnienie = (events[0], get_event_actors(events[0][0]))

  else:
    ujawnienie = (None, None)
    
  result = {} 
  
  result['name'] = scandal [0][0][0]
  result['names'] = scandal [0][0][1:]
  result['description'] = scandal [0][1]  
  result['num_events'] = len(events)
  result['event_leak'] = ujawnienie
  result['events'] = [ (e, get_event_actors(e[0])) for e in events[1:]]
   
  print result['events']
  
  template = loader.get_template ('afera.html')

  return HTTPResponse (template.render(Context(result))  )
  