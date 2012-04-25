from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^cal/$', include('mysite.urls')),
    url(r'^group/$', include('mysite.urls')),
    url(r'^$', include('mysite.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^accounts/login/$', 'django_cas.views.login'),
    url(r'^accounts/logout/$', 'django_cas.views.logout'),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url':'static/favicon.ico'}),
)
