from django.conf.urls import patterns, include, url
from troca_app.views import *
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

from django.contrib.auth.decorators import login_required

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
    url( r'^accounts/login/$', login, {'template_name': 'login.html'} ),
    url( r'^accounts/profile/$', logout ),
    url( r'^accounts/logout/$', logout ),
    url( r'^my_items/$', login_required(ItemsForLoggedUser.as_view()) ),

)
