# Create your views here.

from django.http import HttpResponse as HTTPResponse

from django.template import Context, RequestContext, loader, Template

from django.db import connections

# not views

def scandal (scandal_id, db='afery'):

  cursor = connections[db].cursor()
  cursor.execute("SELECT name,description,background  FROM scandals WHERE id=%s;", (scandal_id,))
  return cursor.fetchall()
          
# views


def case (request, object_id):

  'single scandal view'
  
#  cursor = connections['afery'].cursor()
#  cursor = connections['kuku'].cursor()

  data = scandal(object_id)
  result = {} 
  print data
  
  result['name'] = data[0][0][0]
  result['names'] = data[0][0][1:]
  
  template = loader.get_template ('afera.html')

  return HTTPResponse (template.render(Context(result))  )
  