import os
import sys
import django.core.handlers.wsgi

path = (lambda p:'/'.join(p.split('/')[:-1]))(os.path.abspath(__file__))

if path not in sys.path:
    sys.path.append(path)
    sys.path.append('/usr/share/pyshared/django/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'afery.settings'

application = django.core.handlers.wsgi.WSGIHandler()
