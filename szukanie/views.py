# Create your views here.

from skandale import orm
from django import forms
from django.http import HttpResponse as HTTPResponse
from django.http import HttpResponseRedirect as HTTPResponseRedirect
from django.template import Context, RequestContext, loader, Template
from django.forms.extras.widgets import SelectDateWidget
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

class SearchForm (forms.Form):

  term = forms.CharField(label=u'Wyszukaj')

def szukaj (request):

  result = dict(form=SearchForm())
  if request.method == 'POST':    
    form = SearchForm(request.POST)
    if form.is_valid():
    
      term = form.cleaned_data.get('term', '').strip()
      
      if term:
        t = '%' + term + '%'
        result['cases'] = orm.query('search_cases', (t, t))
        result['events'] = orm.query('search_events', (t, t))
        result['actors'] = orm.query('search_actors', t)
        result['form'] = form

  template = loader.get_template("wyniki.html")      
  return HTTPResponse(template.render(RequestContext(request, result)))
    
      
  
    