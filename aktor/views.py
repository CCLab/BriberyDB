# Create your views here.

import orm

def actor (request, object_id):

  pass


def event_actors (request, object_id):

  actors = orm.query('event_actors', object_id)

  print actors
