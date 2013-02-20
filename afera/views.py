# Create your views here.

from django.http import HttpResponse as HTTPResponse

from django.template import Context, RequestContext, loader, Template


def case (request, object_id):

  'single scandal view'
  
  
  
  template = loader.get_template ('afera.html')

  return HTTPResponse (template.render(Context({}))  )
  