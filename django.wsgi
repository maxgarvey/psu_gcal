import os
import sys

paths = []
paths.append( '/home/maxgarvey/psu_gcal' )
paths.append( '/home/maxgarvey/' )

for path in paths:
  if not (path in sys.path):
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
