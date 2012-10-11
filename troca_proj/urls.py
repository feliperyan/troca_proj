from django.conf.urls import patterns, include, url
from troca_app.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'troca_proj.views.home', name='home'),
    # url(r'^troca_proj/', include('troca_proj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	url( r'^$', index),
	url( r'^item/$', genericItem),
	url( r'^thanks/$', thanks),
)
