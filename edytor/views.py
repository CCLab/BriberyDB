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
    background = forms.CharField(label='Tło', widget=forms.Textarea())
    types = forms.MultipleChoiceField(orm.query('case_types'), widget=forms.CheckboxSelectMultiple(attrs={'size': len(orm.query('case_types'))}),label="Typ")
    fields = forms.MultipleChoiceField(orm.query('case_fields'), widget=forms.CheckboxSelectMultiple(attrs={'size': len(orm.query('case_fields'))}), label="Sfera")
  
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
    description = forms.CharField(label='Opis', widget=forms.Textarea())
#    publication_date = forms.DateField(label='Data publikacji', widget=SelectDateWidget(years=range(1989, 2014)), required=False)
    event_date = forms.DateField(label='Data wydarzenia', widget=SelectDateWidget(years=range(1989,2014)))
    major = forms.BooleanField(label="Wazne", required=False)
    descriptive_date = forms.CharField(label='Data opisowa', required=False)

  if request.method == "GET":

    if event_id:
      event = orm.query('event',event_id)
    
      try: 
        if event[0][0]:
          event=event[0]
          event_form = EventForm (initial=dict(title=event[6], description=event[2], 
            event_date=event[1], descriptive_date=event[8]))
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
        for index in ('title', 'types', 'description', 'event_date', 'major', 'descriptive_date')]

      if event_id:      
        data.append(str(event_id))
        result = orm.query('update_event', data)
      else:
        event_id = orm.query('create_event', data)[0][0]
        events = orm.query('case_events_list',int(case_id))[0][0]        
        if not events:
          events = []
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
    human = forms.BooleanField(label="Osoba", required=False)
    
  class EventActorForm(forms.Form):
    types = forms.MultipleChoiceField(choices=[ list(i) for i in orm.query('all_actor_types') ],  widget=forms.CheckboxSelectMultiple(attrs={'size': 24}), label="Typy", required=False)
    roles = forms.ChoiceField(choices=orm.query('all_actor_roles'), label="Role", required=False)
    affiliations = forms.MultipleChoiceField(choices=[ list(i) for i in orm.query('all_actor_affiliations')], label="Afiliacje",widget=forms.CheckboxSelectMultiple(attrs={'size': 24}), required=False)
    secondary_affiliations = forms.MultipleChoiceField(choices=[ list(i) for i in orm.query('all_actor_secondary_affiliations')], label="Afiliacje drugorzedne",widget=forms.CheckboxSelectMultiple(attrs={'size': 24}), required=False)
    
  if request.method == "GET":
 
   if actor_id:
   # mamy wybranego aktora
   # todo uzupelnianie zaznaczen TODO
   
     metadata = orm.query('case_actor_events_metadata', (case_id, actor_id))
     if metadata:
       line = metadata[-1]
     
       cols = ('types','roles', 'affiliations', 'secondary_affiliations') 
       metadata_dict = {}
#    for line in metadata:
       for item in cols:
         workset = metadata_dict.get(item,set())
         workset = workset.union(tuple(line[cols.index(item)]))
         metadata_dict[item] = workset
              
       output = {}
       for item in cols:
         workdict = {}
         workset = metadata_dict.get(item,set())
         for val in workset:
           workdict[val] = 'checked'
         output[item] = workdict
         actor_form = EventActorForm(initial=output)
     else:
       actor_form = EventActorForm()

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

  template = loader.get_template("edycja_zrodla.html")
  
  class RefForm (forms.Form):
    art_title = forms.CharField(label=u'Tytul artykulu', required=False)
    pub_title = forms.CharField(label=u'Tytul publikacji', required=False)
    url = forms.CharField(label=u'URL', required=False)
    pub_date = forms.DateField(label='Data publikacji', widget=SelectDateWidget(years=range(1989, 2014)),required=False)
    access_date = forms.DateField(label='Data dostepu', widget=SelectDateWidget(years=range(1989, 2014)))

  if request.method == 'GET':
    ref_form=RefForm()
      
  elif request.method == 'POST':
    ref_form = RefForm(request.POST)
    if ref_form.is_valid():
      data = [ ref_form.cleaned_data[item] for item in ('art_title', 'pub_title', 'url', 'pub_date', 'access_date') ]
      try:
        event_refs=list(orm.query('event_refs', event_id)[0][0][0])
      except (TypeError, IndexError):
        event_refs=[]
      ref_id=orm.query('create_ref', data)[0]
      event_refs.append(ref_id)
      orm.query('update_event_refs', (event_refs, event_id))
      return HTTPResponseRedirect(reverse('edytor.views.wydarzenie', kwargs=dict(event_id=event_id, case_id=case_id)))

  return HTTPResponse(template.render(RequestContext(request, dict(form=ref_form)))) 
                
def atrybut(request, case_id=None, event_id=None, actor_id=None):

  case_attributes = {'scandal_types':'Typ', 'scandal_field': 'Sfera dotknięta korupcją'}
  class CaseForm(forms.Form):
    attribute = forms.ChoiceField(choices=[(key, case_attributes[key]) for key in case_attributes.keys()],
      label="Wybierz atrybut")
    name = forms.CharField(label="Nazwa")
   
  event_attributes = {'event_types': 'Typ wydarzenia'}
  class EventForm(forms.Form):
    attribute = forms.ChoiceField(choices=[(key, event_attributes[key]) for key in event_attributes.keys()],label="Wybierz atrybut")
    name = forms.CharField(label="Nazwa")
    
  actor_attributes = {'secondary_affiliations': 'Afiliacja drugorzędna', 
    'actor_affiliations': 'Afiliacja','actor_roles':'Rola', 'actor_types': 'Typ'}
  class ActorForm(forms.Form):
    attribute = forms.ChoiceField(choices=[(key, actor_attributes[key]) for key in actor_attributes.keys()],label="Wybierz atrybut")          
    name = forms.CharField(label="Nazwa")    
    human = forms.BooleanField(label="Osoba", required=False)
  
  if actor_id:
    form=ActorForm
    if actor_id=='0':
      back = reverse('edytor.views.wydarzenie', kwargs=dict(case_id=case_id, event_id=event_id)    )
    else:  
      back = reverse('edytor.views.aktor', kwargs=dict(case_id=case_id, event_id=event_id, actor_id=actor_id))
  elif event_id:
    form=EventForm
    back = reverse('edytor.views.wydarzenie', kwargs=dict(case_id=case_id, event_id=event_id)    )
  elif case_id:
    form=CaseForm           
    back = reverse('edytor.views.afera', kwargs=dict(case_id=case_id))

  template=loader.get_template("atrybut.html")

  if request.method=='GET':
    attribute_form = form()  

  elif request.method == 'POST':

    attribute_form = form(request.POST)
    if attribute_form.is_valid():
      table = attribute_form.cleaned_data['attribute']
      name  = attribute_form.cleaned_data['name']
      
      if isinstance(attribute_form, ActorForm):
        data = (table, name,  attribute_form.cleaned_data['human'])
        orm.query('create_attribute_human', data, special=True)        
      else:
        data = (table, name)
        orm.query('create_attribute', data, special=True)      

      return HTTPResponseRedirect(back)
  return HTTPResponse(template.render(RequestContext(request, dict(form=attribute_form,
    event_id=event_id, actor_id=actor_id, case_id=case_id))))
      

  
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
  