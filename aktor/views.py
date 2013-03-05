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
  pass



def event_actors (request, object_id):

  actors = orm.query('event_actors', object_id)

  print actors

  return HTTPRequest ()
  
