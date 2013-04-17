# Create your views here.

from skandale import orm

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

# views


def case (request, object_id):

  'single scandal view'
  
  scandal = get_scandal(object_id)
  events = orm.query('case_events', object_id)

  if events:
    ujawnienie_actors = orm.query('event_actors',events[0][0])
    ujawnienie = (events[0], ujawnienie_actors[:5],len(ujawnienie_actors))

  else:
    ujawnienie = (None, None, None)
    
  result = {} 
  
  result['name'] = scandal [0][0][0]
  result['names'] = scandal [0][0][1:]
  result['description'] = scandal [0][1]
  result['background'] = scandal[0][2]
  result['num_events'] = len(events)
  result['event_leak'] = ujawnienie
  result['events'] = [ (e, orm.query('event_actors', e[0])[:6]  )
                       for e in events[1:]]
   
  result['javascripts'] = ['actors']
  result['all_actors'] = orm.query('case_actors', object_id)
  result['tab'] = '1'
  result['fields'] = orm.query('scandal_fields', object_id)
  result['types'] = orm.query('scandal_types', object_id)
  
  template = loader.get_template ('afera.html')

  return HTTPResponse (template.render(Context(result))  )


def case_actors (request, object_id):
  'returns HTML <ul> for case actors'
  
  result = {}
  result['actors'] = orm.query('case_actors', object_id)
  template = loader.get_template("aktorzy.inc")
  return HTTPResponse (template.render(Context(dict(case=result))))


def cases (request, object_id=None):
  'all cases view'

  if object_id:
    cases = orm.query('cases_type', object_id)
  else:
    cases = orm.query('cases')

  types =  [ (typ[0], [ t for t in typ[1].split('/') if t]) for typ in orm.query('case_types') ]
  fields = [ (field[0], [ t for t in field[1].split('/') if t]) for field in orm.query('case_fields') ]
  result = []

  for c in cases:

    case = dict(id=c[0],title=c[1], description=c[2])
    actors = orm.query('case_actors', c[0])
    case['events'] = orm.query('event_count', c[0])[0][0]
    case['actors'] = actors[:5]
    case['num_actors'] = len(actors)
    case['num_events'] = len(c[7])
 #   case['fields'] = orm.query('scandal_fields', c[0])
#    fields = orm.query('scandal_fields', c[0])
    
    result.append(case)
    print case

  template = loader.get_template ('afery.html')

  return HTTPResponse (template.render(Context(dict(cases=result,
    tab=1, javascripts=['actors', 'jquery-1.9.1.min'], jquery=True, types=types, fields=fields))))


def event (request, object_id):
  'single event view'
  scandal_title = None  
  event = list(orm.query('event', object_id)[0])
  actors = orm.query('event_actors', object_id)  
  event[2] = event[2].split('\n')
  
  scandal_title = orm.query('event_case_title', event[0])[0][0][0]
  
  try:
    if event:
      refs = orm.query('refs','{'+','.join([str(i) for i in event[5]])+'}')
  except (IndexError, TypeError):
    refs = []

  try: 
    prev_e = orm.query('prev_event', (object_id, object_id))[0]
  except IndexError:
    prev_e = None
  try:
    next_e = orm.query('next_event', (object_id,object_id))[0]
  except IndexError:
    next_e = None
                      
  result = dict(refs=refs, event=event, prev=prev_e, next=next_e, actors=actors,tab=1)

  result['tab'] = 1
  result['scandal_title'] = scandal_title if isinstance(scandal_title, unicode) else scandal_title.decode('utf-8')

  template = loader.get_template("wydarzenie.html")

  return HTTPResponse (template.render(Context(result)))


def timeline(request, object_id):
  'single scandal timeline view'

  result = {}
  scandal = get_scandal(object_id)
  result['name'] = scandal [0][0][0]
  result['names'] = scandal [0][0][1:]
  result['description'] = scandal [0][1]
  result['background'] = scandal[0][2]
  result['case'] = object_id
  template = loader.get_template ('linia.html')

  return HTTPResponse (template.render(Context(result))  )


def api_case_json(request, object_id):

  import json

  case = get_scandal(object_id)
  events = orm.query('case_events', object_id)

  result = {}

  result['timeline'] = { 'headline': case[0][0][0], 'type': 'default', 'text': case[0][1], 'startDate': events[0][1].strftime('%Y,%m,%d') }


  dates = []

  for event in events:
    dates.append({'startDate': event[1].strftime('%Y,%m,%d'), 'endDate': event[1].strftime('%Y-%m-%d'), 'headline':event[6], 'text': event[2]})

  result['timeline']['date']=dates

  return HTTPResponse(json.dumps(result))
