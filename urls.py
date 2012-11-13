from django.conf.urls.defaults import patterns, include, url

#for debug
from django.views import static as my_static
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^calendar_form/$', include('mysite.urls')),
    url(r'^group_form/$', include('mysite.urls')),
    url(r'^cal/$', include('mysite.urls')),
    url(r'^group/$', include('mysite.urls')),
    url(r'^alias/$', include('mysite.urls')),
    url(r'^$', include('mysite.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^accounts/login/$', 'django_cas.views.login'),
    url(r'^accounts/logout/$', 'django_cas.views.logout'),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url':'static/favicon.ico'}),
    url(r'^static/(?P<path>.*)$', my_static.serve, {'document_root': '/home/maxgarvey/projects/psu_gcal/live_version/mysite/static/'}),
)

#debug also
#urlpatterns += staticfiles_urlpatterns()
