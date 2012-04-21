from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^cal/$', include('mysite.urls')),
    url(r'^group/$', include('mysite.urls')),
    url(r'^$', include('mysite.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^accounts/login/$', 'django_cas.views.login'),
    url(r'^accounts/logout/$', 'django_cas.views.logout'),
)
