#from django.conf.urls.defaults import patterns, include, url
from django.conf.urls import patterns, url, include
from troca_app.views import *
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^mongonaut/', include('mongonaut.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', index),
    url(r'^search/$', search),
    url(r'^search/(?P<ordering>\w+)/$', search, name='search_ordering'),

    url(r'^thanks/$', thanks),
    
    url(r'^accounts/login/$', login, {'template_name': 'login.html'} ),
    url(r'^accounts/signin/', 'userena.views.signin', {'template_name': 'Userena/signin_form.html'}, name="signin"),
    url(r'^accounts/signup/', 'userena.views.signup', {'template_name': 'Userena/signup_form.html'}, name="signup"),
    url(r'^accounts/(?P<username>(?!signout|signup|signin)[\.\w-]+)/$',
       profile_detail_extended, {'template_name': 'Userena/profile_detail.html'},
       name='userena_profile_detail'),
    
    
    (r'^accounts/', include('userena.urls')),
    url(r'^facebook/', include('django_facebook.urls')),
    #url( r'^accounts/login/$', login, {'template_name': 'login.html'} ),
    #url( r'^accounts/logout/$', logout, {'next_page': '/'} ),

    #url( r'^my_items/$', login_required(ItemsForLoggedUser.as_view()) ),
    url(r'^my_items/$', myProfile, name='myProfile' ),

    url(r'^items/(?P<item_id>\w+)/$', detail, name='detail'),

    url(r'^add_item/(?P<category>\w+)$', add_item, name='add_item'),
    url(r'^categories/$', categories, name='categories'),
    url(r'^getCategories/$', getAjaxCategories, name='getAjaxCategories'),

    url(r'^vote/(?P<item_id>\w+)/(?P<vote>\w+)$', voteAjax, name='vote'),

    #url(r'^items/(?P<item_id>\w+)/make_offer/$', makeOffer, name='make_offer'),
    #url(r'^items/(?P<item_id>\w+)/make_offer/$', makeOfferWithForm, name='make_offer'),
    url(r'^make_offer/(?P<item_id>\w+)/$', testEmbeddedDocumentForm, name='make_offer'),

    url(r'^offers/(?P<item_id>\w+)/$', offers_for_item, name='offers_for_item'),
    url(r'^offers/(?P<item_id>\w+)/(?P<offer_title_slug>[-\w]+)/$', specific_offer, name='specific_offer'),
    url(r'^offers/(?P<item_id>\w+)/(?P<offer_title_slug>[-\w]+)/(?P<response>[-\w]+)/$', 
        decision_offer, name='decision_offer'),
                       
    #Don't add this line if you use django registration or userena for registration and auth.
    #url(r'^accounts/', include('django_facebook.auth_urls')), 

    url(r'^testImage/', testImage, name='testImage'), 

)

from troca_proj import settings
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))


    