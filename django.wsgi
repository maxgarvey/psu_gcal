import os
import sys

#activate_this = 'env/bin/activate_this.py'
#execfile(activate_this,dict(__file__=activate_this))

paths = []
paths.append( '/var/www/psu_gcal' )
paths.append( '/var/www/psu_gcal/mysite' )

for path in paths:
  if not (path in sys.path):
    sys.path.append(path)

#debug
#print 'syspath: ' + str(sys.path)
#print 'py home: ' + str(os.environ['HOME'])
#end debug

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
