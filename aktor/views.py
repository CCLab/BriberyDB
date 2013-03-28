# Create your views here.

from skandale import orm

from django.http import HttpResponse as HTTPResponse

from django.template import Context, RequestContext, loader, Template

def actors (request, human=True):

  'Actors index.'

  letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

  result = []
  
  for l in letters:

    if human:
      result.append((l, orm.query('actors_human_like', (l.lower()+'%', l.upper()+'%'))))
    else:
      result.append((l, orm.query('actors_nonhuman_like', (l.lower()+'%', l.upper()+'%'))))
  template = loader.get_template("indeks.html")

  return HTTPResponse (template.render(Context(dict(letters=result,tab=2 if human else 3))))
    

def actor (request, object_id):

  actor = orm.query('actor', object_id)[0]

  roles_rows = orm.query('actor_roles', object_id)

  roles_dict = {}
  for row in roles_rows:
    role = row[1]
    case = row[3]
    role_dict = roles_dict.get(role,dict(id=row[0]))
    case_list = role_dict.get(case, [])
    case_list.append(row[2])
    role_dict[case] = case_list
    roles_dict[role] = role_dict
    
  roles = [ ( role, [ ((case, roles_dict[role]['id']), roles_dict[role][case]) for case in roles_dict[role].keys() if not case=='id' ] ) for role in roles_dict.keys() ]
  
  result = dict(actor=actor, roles=roles, tab=2)

  template = loader.get_template("aktor.html")

  return HTTPResponse (template.render(Context(result)))


def event_actors (request, object_id):

  actors = orm.query('event_actors', object_id)

  print actors

  return HTTPRequest ()
  
