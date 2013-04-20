#! /usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.

import datetime
from skandale import orm
from django import forms
from django.http import HttpResponse as HTTPResponse
from django.http import HttpResponseRedirect as HTTPResponseRedirect
from django.template import Context, RequestContext, loader, Template
from django.forms.extras.widgets import SelectDateWidget
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

#from django.db import connections
#  
  
#def execute (query, data):
#  cursor = db['afery'].cursor()

#  cursor.execute(
  
def afera(request, case_id=None):

  template = loader.get_template('edycja_afery.html')

  fields = orm.query('case_types')
  types = orm.query('case_fields') 

  class ScandalForm(forms.Form):
  
    name = forms.CharField(label=u'Tytuly (oddzielone przecinkami)')
    description = forms.CharField(label='Opis', widget=forms.Textarea())
    background = forms.CharField(label='Opis', widget=forms.Textarea())
    types = forms.MultipleChoiceField(orm.query('case_types'), widget=forms.CheckboxSelectMultiple(attrs={'size': len(orm.query('case_types'))}))
    fields = forms.MultipleChoiceField(orm.query('case_fields'), widget=forms.CheckboxSelectMultiple(attrs={'size': len(orm.query('case_fields'))}))
  
  if request.method == "GET":
  
    if case_id:
      case = orm.query('get_case', case_id)
      
      try: 
        if case[0][0]: #jest id
          case=case[0]
          case_form = ScandalForm(initial=dict(titles=','.join(case[1]), description=case[2], background=case[3]))
        else:
           case_form=ScandalForm()
      except IndexError:
        case_form=ScandalForm()
                 
    else:
      case_form=ScandalForm()
      
    return HTTPResponse(template.render(RequestContext(request, dict(form=case_form, case_id=case_id))))

  elif request.method == "POST":
    case_form = ScandalForm(request.POST)

    if case_form.is_valid():
      data = [ [ int(i) for i in case_form.cleaned_data[index] ] if index in ['types','fields'] else case_form.cleaned_data[index] 
        for index in ('name', 'description', 'background', 'types', 'fields')]
      
      data = [data[0].split(',')] + data[1:]

      if case_id:
        data.append(str(case_id))
        orm.query('update_case', data)  
      else:
        result=orm.query('create_case', data)[0][0]
        
      return HTTPResponseRedirect('/edit/%s' % result)
    else:

      return HTTPResponse(template.render(RequestContext(request, dict(form=case_form))))
                


def wydarzenie (request, case_id, event_id=None):

  locations = orm.query('locations')
  
  class EventForm (forms.Form):
    types = forms.ChoiceField(orm.query('events_types'))
    title = forms.CharField(label=u'Tytul')
    #initial=event[6] if object_id else None)
    description = forms.CharField(label='Opis', widget=forms.Textarea())
#    initial=event[2] if object_id else None)
    publication_date = forms.DateField(label='Data publikacji', widget=SelectDateWidget(years=range(1989, 2014)))
    event_date = forms.DateField(label='Data wydarzenia', widget=SelectDateWidget(years=range(1989,2014)))
#    location = forms.MultipleChoiceField(locations, required=False, widget=forms.CheckboxSelectMultiple(attrs={'size': len(locations)}))
    major = forms.BooleanField(label="Wazne", required=False)

  if request.method == "GET":

    if event_id:
      event = orm.query('event',event_id)
    
      try: 
        if event[0][0]:
          event=event[0]
          event_form = EventForm (initial=dict(title=event[6], description=event[2], 
            event_date=event[1], publication_date=event[3]))
        else:
          event_form = EventForm()
      except IndexError:
        event_form = EventForm()
    else:
      event_form = EventForm()

    template = loader.get_template('edycja_wydarzenia.html')
    return HTTPResponse(template.render(RequestContext(request, dict(form=event_form, event_id=event_id, case_id=case_id))))
    
  elif request.method =="POST":
  
    event_form = EventForm(request.POST)

    if event_form.is_valid():
      data = [ [int(event_form.cleaned_data[index])] if index=='types' else event_form.cleaned_data[index] 
        for index in ('title', 'types', 'description', 'publication_date', 'event_date', 'major')]

      if event_id:      
        data.append(str(event_id))
        result = orm.query('update_event', data)
      else:
        event_id = orm.query('create_event', data)[0][0]
        events = orm.query('case_events_list',int(case_id))[0][0]        
        events.append(int(event_id))        
        status = orm.query('case_update_events', (events, case_id))
                
      return HTTPResponseRedirect('/edit/%s/event/%s' % ( case_id, event_id))
    else:
      template = loader.get_template('edycja_wydarzenia.html')
      return HTTPResponse(template.render(RequestContext(request, dict(form=event_form))))
          
def aktor(request, case_id, event_id, actor_id=None, add=False):

  template = loader.get_template('edycja_aktora.html')
  
  class ActorForm(forms.Form):
    actor = forms.ChoiceField(choices=[ list(i) for i in orm.query('all_actors') ], 
      label="Nazwa", widget=forms.RadioSelect())    

  class AddActorForm(forms.Form):
    name = forms.CharField(label='Nazwa/nazwisko')
    human = forms.BooleanField(label="Wazne", required=False)
    
  class EventActorForm(forms.Form):
    types = forms.MultipleChoiceField(choices=[ list(i) for i in orm.query('all_actor_types') ],  widget=forms.CheckboxSelectMultiple(attrs={'size': 24}), label="Typy")
    roles = forms.ChoiceField(choices=orm.query('all_actor_roles'), label="Role")
    affiliations = forms.MultipleChoiceField(choices=[ list(i) for i in orm.query('all_actor_affiliations')], label="Afiliacje",widget=forms.CheckboxSelectMultiple(attrs={'size': 24}))
    secondary_affiliations = forms.MultipleChoiceField(choices=[ list(i) for i in orm.query('all_actor_secondary_affiliations')], label="Afiliacje drugorzedne",widget=forms.CheckboxSelectMultiple(attrs={'size': 24}))
    
  if request.method == "GET":
 
   if actor_id:
   # mamy wybranego aktora
   # todo uzupelnianie zaznaczen TODO
   
     metadata = orm.query('case_actor_events_metadata', (case_id, actor_id))
     cols = ('types','roles', 'affiliations', 'secondary_affiliations') 
     metadata_dict = {}
     for line in metadata:
       for item in cols:
          workset = metadata_dict.get(item,set())
          workset = workset.union(tuple(line[cols.index(item)]))
          metadata_dict[item] = workset
              
     output = {}
     for item in cols:
       workdict = {}
       workset = metadata_dict.get(item,set())
       for val in workset:
         workdict[val]  =' checked'
       output[item] = workdict
                          
     actor_form = EventActorForm(initial=output)
     return HTTPResponse(template.render(RequestContext(request, dict(form=actor_form, event_id=event_id, case_id=case_id))))
   else:
     if add:
       # dodajemy aktora
       return HTTPResponse(template.render(RequestContext(request, dict(form=AddActorForm(), event_id=event_id, case_id=case_id))))
     else:
       # wybieramy aktora
       return HTTPResponse(template.render(RequestContext(request, dict(form=ActorForm(), event_id=event_id, case_id=case_id))))
  elif request.method == "POST":
    if actor_id: 
    # wybralismy aktora i albo pokazujemy formatke albo go przypisujemy
      actor_form = EventActorForm(request.POST)
    
      if actor_form.is_valid():
        data = [ [int(i) for i in actor_form.cleaned_data[index]] if index in ['types', 'roles', 'affiliations', 'secondary_affiliations']  else actor_form.cleaned_data[index]
          for index in ('types', 'roles', 'affiliations', 'secondary_affiliations')]
        
        data = [event_id, actor_id] + data
        orm.query('assign_actor', data)
        
        return  HTTPResponseRedirect(redirect_to=reverse('edytor.views.wydarzenie', 
          kwargs=dict(event_id=event_id, case_id=case_id)))
      else: 
        #cos nie pasuje, pokazujemy form jeszcze raz TODO
        return HTTPResponse(template.render(RequestContext(request, dict(form=actor_form, event_id=event_id, case_id=case_id, actor_id=actor_id))))   
    else: 
      if add == True:
        add_actor_form=AddActorForm(request.POST)
        if add_actor_form.is_valid():
          actor_id = orm.query('create_actor', (add_actor_form.cleaned_data['name'], add_actor_form.cleaned_data['human']))[0][0]
          return  HTTPResponseRedirect(redirect_to=reverse('edytor.views.aktor', 
            kwargs=dict(event_id=event_id, case_id=case_id, actor_id=actor_id)))        
        else:
          return HTTPResponse(template.render(RequestContext(request, dict(form=add_actor_form, event_id=event_id, case_id=case_id))))          
      else:
        actor_form = ActorForm(request.POST)
        if actor_form.is_valid():
        # nie mamy actor_id, albo pokazujemy formatke, albo przekierowujemy do actor_id
          actor_id = actor_form.cleaned_data["actor"]
          return  HTTPResponseRedirect(redirect_to=reverse('edytor.views.aktor', 
            kwargs=dict(event_id=event_id, case_id=case_id, actor_id=actor_id)))        
        else:
          return HTTPResponse(template.render(RequestContext(request, dict(form=actor_form))))
            
        

def zrodlo(request, case_id, event_id):

  class RefForm (forms.Form):
    art_title = forms.CharField(label=u'Tytul artykulu')
    pub_title = forms.CharField(label=u'Tytul publikacji')
    url = forms.CharField(label=u'URL', required=False)
    pub_date = forms.DateField(label='Data publikacji', widget=SelectDateWidget(years=range(1989, 2014)),required=False)
    access_date = forms.DateField(label='Data dostepu', widget=SelectDateWidget(years=range(1989, 2014)),required=False)

                      
          
#def roles(request, object_id):
#
#  all_roles = orm.query('roles')
#  role_choice = [ (i[0], i[1]) for i in all_roles]
#
  
#  class RoleForm (forms.Form):
#    roles = forms.MultipleChoiceField (role_choice, 
#      label="Role w aferze", widget=forms.CheckboxSelectMultiple(attrs={'size': len(role_choice)}))
#    
#  role_form = RoleForm(initial ={'roles': {'10': 'checked',}})
  
#  return HTTPResponse(role_form)
  