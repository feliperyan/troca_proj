from django.conf.urls.defaults import patterns, include, url
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
    url( r'^thanks/$', thanks),
    
    url( r'^accounts/login/$', login, {'template_name': 'login.html'} ),
    url( r'^accounts/logout/$', logout, {'next_page': '/'} ),

    #url( r'^my_items/$', login_required(ItemsForLoggedUser.as_view()) ),
    url( r'^my_items/$', myProfile, name='myProfile' ),

    url(r'^items/(?P<item_id>\w+)/$', detail, name='detail'),

    url(r'^add_item/(?P<category>\w+)$', add_item, name='add_item'),
    url(r'^categories/$', categories, name='categories'),
    url(r'^getCategories/$', getAjaxCategories, name='getAjaxCategories'),

    url(r'^items/(?P<item_id>\w+)/make_offer/$', makeOffer, name='make_offer'),
    #url(r'^items/(?P<item_id>\w+)/make_offer/$', makeOfferWithForm, name='make_offer'),


    url(r'^facebook/', include('django_facebook.urls')),
    #Don't add this line if you use django registration or userena for registration and auth.
    url(r'^accounts/', include('django_facebook.auth_urls')), 
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))


    