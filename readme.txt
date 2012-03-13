for this app, the root dir should be a directory inside of the django instance.
Django_cas-2.0.3 should be installed in the base dir. The specs for django_cas are in settings.py in the mysite dir. 
Also, I've included the apache2 configs needed to get this running in the base directory. They use mod_wsgi, so that must be installed in the apache2 plugins.
httpd.conf is the main apache2 conf, and vhost-sites.conf is the conf for the /etc/apache2/sites-enabled dir
also, i added '/home/maxgarvey/python/django/psu_gcal/mysite' to django's python path, where mysite is the same mysite from the root dir.
