from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
#    (r'^$', direct_to_template, dict(template='main.html', tab=1),'page_main'),
    (r'^$', 'afera.views.cases', dict(intro=True), 'page_main'),
    (r'^o-serwisie/$', direct_to_template,
      dict(template='about.html', extra_context=dict(tab=4)), 'page_about'),
    (r'^kontakt/$', direct_to_template,
     dict(template='contact.html', extra_context=dict(tab=5)), 'page_contact'),
     
    (r'^wydarzenie/(?P<object_id>\d+)/$', 'afera.views.event'),
    (r'^wydarzenie/(?P<object_id>\d+)/podmioty/$', 'aktor.views.event'),

    (r'^afery/$', 'afera.views.cases' ),

    (r'^afery/(?P<type_id>\d+)/$', 'afera.views.cases' ),
    (r'^afery/(?P<type_id>\d+)/(?P<field_id>\d+)/$', 'afera.views.cases' ),
    (r'^afery//(?P<field_id>\d+)/$', 'afera.views.cases' ),    
    (r'^afera/(?P<object_id>\d+)/$', 'afera.views.timeline', None, 'single_case' ),
    (r'^afera/(?P<object_id>\d+)/vertical/$', 'afera.views.case' ),
#    (r'^afera/(?P<object_id>\d+)/os/$', 'afera.views.timeline' ),                       
    (r'^afera/all/$', 'afera.views.cases' ),
    (r'^afera/(?P<object_id>\d+)/podmioty/$', 'afera.views.case_actors' ),


    (r'^podmiot/(?P<object_id>\d+)/?$', 'aktor.views.actor'),
    (r'^podmiot/ludzie/?$', 'aktor.views.actors', dict(human=True),'page_actors_human'),
    (r'^podmiot/instytucje/?$', 'aktor.views.actors', dict(human=False), 'page_actors_organizational'),

    (r'^api/afera/(?P<object_id>\d+)/(?P<major>major)/?$', 'afera.views.api_case_json' ),    
    (r'^api/afera/(?P<object_id>\d+)/?$', 'afera.views.api_case_json' ),
    
    (r'^edit/', include('edytor.urls')),   
    (r'^search/', include('szukanie.urls')),    
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

)



if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

