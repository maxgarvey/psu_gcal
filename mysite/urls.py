'''mysite/urls.py'''
from django.conf.urls.defaults import patterns, url

# admin is at the global urls level, not this subdir one
urlpatterns = patterns('',
  url(r'^$', 'mysite.views.index'),
  url(r'^accounts/login/$', 'django_cas.views.login'),
  url(r'^accounts/logout/$', 'django_cas.views.logout'),
)
