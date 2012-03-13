import os
import sys

paths = []
paths.append( '/home/maxgarvey/python/django/psu_gcal' )
paths.append( '/home/maxgarvey/python/django/psu_gcal/mysite' )
paths.append( '/home/maxgarvey/python/django/psu_gcal/mysite/psu_gcal' )

for path in paths:
  if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
