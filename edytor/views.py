# Create your views here.

# -*- coding: utf-8 -*-

from skandale import orm
from django import forms
from django.http import HttpResponse as HTTPResponse
from django.template import Context, RequestContext, loader, Template
from django.forms.extras.widgets import SelectDateWidget

#def afera(request, object_id):
#  pass
def afera(request, object_id):

  all_roles = orm.query('roles')
  role_choice = [ (i[0], i[1]) for i in all_roles]

  
  class RoleForm (forms.Form):
    roles = forms.MultipleChoiceField (role_choice, 
      label="Role w aferze", widget=forms.CheckboxSelectMultiple(attrs={'size': len(role_choice)}))
    
  role_form = RoleForm(initial ={'roles': {'10': 'checked',}})
  
  return HTTPResponse(role_form)
  
  

def wydarzenie (request, object_id=None):

  locations = orm.query('locations')
    
  class EventForm (forms.Form):
    title = forms.CharField(label=u'Tytul')
    #initial=event[6] if object_id else None)
    description = forms.CharField(label='Opis', widget=forms.Textarea())
#    initial=event[2] if object_id else None)
    publication = forms.DateField(label='Data publikacji', widget=SelectDateWidget())
    event = forms.DateField(label='Data wydarzenia', widget=SelectDateWidget())
    location = forms.MultipleChoiceField(locations, widget=forms.CheckboxSelectMultiple(attrs={'size': len(locations)}))


  if object_id:
    event = orm.query('event')
    
#    if event:

    event_form = EventForm (initial=dict(title=event[6], description=event[2], event=event[1], publication=event[3]))

  else:
    event_form = EventForm()
  return HTTPResponse(event_form.as_p())
      