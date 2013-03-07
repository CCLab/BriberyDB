# Create your views here.

import orm

from django.http import HttpResponse as HTTPResponse

from django.template import Context, RequestContext, loader, Template

def actors (request):
  'Actors index.'

  letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

  result = []
  
  for l in letters:

    result.append((l, orm.query('actors_like', (l.lower()+'%', l.upper()+'%'))))

  template = loader.get_template("indeks.html")

  return HTTPResponse (template.render(Context(dict(letters=result,tab=2))))
  
  

def actor (request, object_id):

  actor = orm.query('actor', object_id)[0]


  roles_rows = orm.query('actor_roles', object_id)

  roles_dict = {}
  for row in roles_rows:
    r = roles_dict.get(row[1],[])
    r.append ((row[2], row[3]))
    roles_dict [row[1]] = r
  
  roles = [ (r, roles_dict[r]) for r in roles_dict.keys()]

  print roles
  result = dict(actor=actor, roles=roles, tab=2)

  template = loader.get_template("aktor.html")

  return HTTPResponse (template.render(Context(result)))




def event_actors (request, object_id):

  actors = orm.query('event_actors', object_id)

  print actors

  return HTTPRequest ()
  
