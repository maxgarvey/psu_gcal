from django.conf.urls.defaults import patterns, include, url

# admin is at the global urls level, not this subdir one
urlpatterns = patterns('',
  url(r'^$', 'psu_gcal.views.index'),
  url(r'(?P<file>\w+.\w*)/$', 'psu_gcal.views.static' ),
  url(r'^accounts/login/$', 'django_cas.views.login'),
  url(r'^accounts/logout/$', 'django_cas.views.logout'),
)
