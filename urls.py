from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'direct_to_template', dict(template='main.html'), 'page_main'),
    (r'^/o-serwisie/$', 'direct_to_template', dict(template='about.html'),'page_about'),
    (r'^/kontakt/$', 'direct_to_template', dict(template='contact.html'),'page_contact'),
     
    # (r'^afery/', include('afery.foo.urls')),
    
    (r'afera/(?P<object_id>\d+)/$', 'afera.views.case' ),

    

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)



if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

