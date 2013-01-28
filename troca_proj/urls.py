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

    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url( r'^accounts/login/$', login, {'template_name': 'login.html'} ),
    url( r'^accounts/logout/$', logout, {'next_page': '/'} ),
    url( r'^accounts/profile/$', myProfile, name='profile' ),
	
    url( r'^$', index),
	url( r'^add_item/$', genericItem),
	url( r'^thanks/$', thanks),
    #url( r'^my_items/$', login_required(ItemsForLoggedUser.as_view()) ),
    
    url( r'^my_items/$', myProfile, name='myProfile' ),

    url(r'^items/(?P<item_id>\w+)/$', detail, name='detail'),
    url(r'^item/$', genericItem, name='add_item'),
    url(r'^items/(?P<item_id>\w+)/make_offer/$', makeOffer, name='make_offer'),
)
