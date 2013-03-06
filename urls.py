from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'direct_to_template', dict(template='main.html'), 'page_main'),
    (r'^/o-serwisie/$', 'direct_to_template',
      dict(template='about.html', extra_context=dict(tab=4)), 'page_about'),
    (r'^/kontakt/$', 'direct_to_template',
     dict(template='contact.html', extra_context=dict(tab=5)), 'page_contact'),
     
    # (r'^afery/', include('afery.foo.urls')),

    (r'^wydarzenie/(?P<object_id>\d+)/$', 'afera.views.event'),
    
    (r'^afera/(?P<object_id>\d+)/$', 'afera.views.case' ),
    (r'^afera/all/$', 'afera.views.cases' ),
    (r'^afera/(?P<object_id>\d+)/actors/$', 'afera.views.case_actors' ),
    (r'^podmiot/(?P<object_id>\d+)/?$', 'aktor.views.actor'),
    (r'^podmiot/all/?$', 'aktor.views.actors'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)



if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

