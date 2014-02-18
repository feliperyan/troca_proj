# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from models import *
from forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.http import Http404
from django.views.generic import ListView
from django.utils import simplejson
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from bson.objectid import ObjectId

from userena.views import *

import logging
logger = logging.getLogger('troca')


def categories(request):
    return render(request, 'select_categories.html', )

@login_required
def voteAjax(request, item_id, vote):
    wantedItem = GenericItem.objects.get(pk=item_id)
    point = 0
    
    if vote != 'up' and vote != 'down':
        raise Http404
    else:
        if vote == 'down':
            point = -1
        else:
            point = 1

    logger.info('VOTE: %s' % vote)

    if request.is_ajax():
        if wantedItem.hasAlreadyVoted(request.user.id):
            logger.info('VOTE: not_ok')
            m = {'answer': 'not_ok'}
        else:
            logger.info('VOTE: ok')
            v = Vote(author_id=request.user.id, direction=point)
            wantedItem.votes.append(v)
            wantedItem.v_count += point
            wantedItem.save()
            m = {'answer': 'ok', 'total':wantedItem.countVotes()}
        
        m = simplejson.dumps(m)
    
    else:
        raise Http404

    return HttpResponse(m, mimetype='application/json')


def getAjaxCategories(request):

    if request.GET['category']:
        parent = request.GET['category']
        #import pdb; pdb.set_trace()
    
    if request.is_ajax():
        if parent:
            p = get_object_or_404( Category, categoryTitle = parent )
            
            #Breaking the string into tokens for the javascript to handle:
            crumbs = p.howToOrder().split('>')

            #Only interested in the categoryTitle attribute of the Category object
            items = list(Category.objects.filter( parentCategory = p ).values_list('categoryTitle'))        
            
            m = {'items': items, 'crumbs': crumbs}
            message = simplejson.dumps(m)

        else:
            #reached the end of the categories.
            message = 'no more cats'
    else:
        #this should be a response for non ajax requests...
        message = 'god damn'

    #import time
    #time.sleep(3)
    return HttpResponse(message, mimetype='application/json')


def index(request):
    
    #categories = Category.objects.all()
    item_list = GenericItem.objects.order_by('-date_added')
    paginator = Paginator(item_list, 6)

    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'items': items})


def search(request, ordering=None):
    title = None
    geo = None
    category = None
    lat = None
    lon = None
    
    context = {}

    #Dealing with pagination for queries
    #http://djangosnippets.org/snippets/1592/

    q_no_page = request.GET.copy()
    if q_no_page.has_key('page'):
        del q_no_page['page']

    queries = q_no_page

    #Give us a result even if there is no search info:
    item_list = GenericItem.objects.order_by('-date_added')

    if 'title' in request.GET and request.GET['title']:
        title = request.GET['title']
        if title == '':
            title = None

    if 'geo' in request.GET and request.GET['geo'] and\
    'lat' in request.GET and request.GET['lat'] and\
    'lon' in request.GET and request.GET['lon']:
        geo = request.GET['geo']
        lat = request.GET['lat']
        lon = request.GET['lon']
        
        if geo.isdigit and lat.isdigit and lon.isdigit:
            geo = int(geo)
            lat = float(lat)
            lon = float(lon)
            if geo == 0:
                geo = None

    if 'cat' in request.GET and request.GET['cat']:
        category = request.GET['cat']
        if category == 'abc':
            category = None

    logger.info(title)
    logger.info(category)
    logger.info(geo)
    logger.info(lon)
    logger.info(lat)
    
    if title is not None:
        logger.info('searching for title:'+title)
        item_list = GenericItem.objects(title__icontains=title).order_by('date_added')
    
    if category is not None:
        logger.info('searching for category:'+category)
        item_list = item_list.filter(cat__icontains=category)
        
    if geo is not None:
        item_list = item_list.filter(geo_location__near=[lon,lat], geo_location__max_distance=geo)

    if ordering == 'votes':
        item_list = item_list.order_by('-v_count')    

    paginator = Paginator(item_list, 6)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    terms = {'title':title, 'geo':geo, 'category':category, 'lat':lat, 'lon':lon}
    
    return render(request, 'index.html', {'items': items, 'queries': queries, 'terms':terms})

    #eos = GenericItem.objects(Q(geo_location__near=[37.769,40.123], \
        #geo_location__max_distance=100) & Q(title__icontains='4'))


def detail(request, item_id):
    try:
        item = GenericItem.objects.get(pk=item_id)
        owner = User.objects.get(pk=item.owner_id)
    except GenericItem.DoesNotExist:
        raise Http404
    return render(request, 'item_detail.html', {'item': item, 'owner': owner})


def thanks(request):
    return render(request, 'thanks.html', {})

@login_required
def add_item(request, category):
    
    logger.info(category)
    
    if request.method == 'POST':        
        
        if category == 'Tickets_and_reservations':
            logger.info('got tickets form') 
            form = TicketsForm(request.POST, request.FILES)       
        
        elif category == 'Skills':            
            form = SkillForm(request.POST, request.FILES)        
        
        else:                    
            form = ModelFormGenericItem(request.POST, request.FILES)

        if form.is_valid():

            instance = form.save(commit = False)
            instance.owner_id = request.user.id
            instance.owner_username = request.user.username
            instance.cat = instance._class_name.split('.')[-1]
            
            instance.save()
            
            return HttpResponseRedirect('/thanks/')

    else:
        # Ensure that this is a "final" category:
        p = get_object_or_404( Category, categoryTitle = category )        
        i = Category.objects.filter( parentCategory = p )
        if i.count() != 0:
            raise Http404

        if category == 'Tickets_and_reservations':
            form = TicketsForm()
        
        elif category == 'Skills':
            logger.info('display Skills form')
            form = SkillForm()
        
        else:        
            logger.info('display Generic form')
            form = ModelFormGenericItem()

    return render(request, 'item.html', {
        'form': form,
        'category': category,
    } )

# EmbeddedForm MakeOffer has replaced this - Will it be good enought to stay?!

@login_required
def makeOffer(request, item_id):
    
    wantedItem = GenericItem.objects.get(pk=item_id)

    myItems = GenericItem.objects.filter(owner_id = request.user.id)

    if request.method == 'POST':
        selected_items = request.POST.getlist('items_selected')

        #import pdb; pdb.set_trace()

        offer_title = request.POST.get('offer_title')

        if len(selected_items) < 1:
            return render(request, 'make_offer.html', {
                'wantedItem': wantedItem,'myItems': myItems, 'error':'Must select an item.'
            })

        else:
            items_in_offer = list()
            for i in selected_items:
                #wholeItem = get_object_or_404( GenericItem, pk = i )
                wholeItem = GenericItem.objects.get(pk=i)
                partialitem = ItemInOffer(itemTitle=wholeItem.title, value=wholeItem.value, item=wholeItem)
                items_in_offer.append(partialitem)

            offer = Offer(title=offer_title, author_id=request.user.id, author=request.user.username, items=items_in_offer)

            #import pdb; pdb.set_trace()

            wantedItem.offers.append(offer)
            wantedItem.save()

            return HttpResponseRedirect('/thanks/')

    else:
        
        return render(request, 'make_offer.html', {
            'wantedItem': wantedItem,
            'myItems': myItems,
            'hasMadeOffer': wantedItem.hasAlreadyMadeOffer(request.user.id)
        })

@login_required
def myProfile(request):
    myItems = GenericItem.objects.filter(owner_id = request.user.id)


    # Example of a RAW MongoDB query:
    #itemsWithMyOffers = GenericItem.the_objects.raw_query({ 'offers.author_id': request.user.id })
    itemsWithMyOffers = GenericItem.objects(__raw__={ 'offers.author_id': request.user.id })

    return render(request, 'myItems.html', {
            'myItems': myItems,'myOffers': itemsWithMyOffers
    })

@login_required
def decision_offer(request, item_id, offer_title_slug, response):
    owner = request.user.id
    wantedItem = GenericItem.objects.get(pk=item_id)
    ofr = None

    #import ipdb; ipdb.set_trace()

    #Only item owner can accept offers of course:
    if owner != wantedItem.owner_id or wantedItem is None:
        return render(request, 'info.html', {'info': 'You don\'t own that item and can not accept offers for it!' })

    ofr = wantedItem.get_offer_by_slug(offer_title_slug)
    if not ofr:
        return render(request, 'info.html', {'info': 'Offer Not found!' })

    if response == 'reject' and ofr.status == 'pending':
        ofr.status = 'rejected'
        wantedItem.save()
        return render(request, 'info.html', {'info': 'offer Rejected!' })
    elif ofr.status != 'pending':
        return render(request, 'info.html', {'info': 'This offer has already been dealt with.' })

    else:
        # First make this item temporarily unavailable.
        # Going down to pymongo level in order to use findAndModify
        locked = acquire_pending_lock(wantedItem)
        if not locked:
            info = 'Could not accept any offers for this item right now!'
            return render(request, 'info.html', {'info': info} )

        # Second check that items in the offer being accepted are available 
        locked = []
        failed_to_lock = None
        for i in ofr.items:
            got_lock = acquire_pending_lock(i.item)
            if got_lock:
                locked.append(i.item)
            else:
                failed_to_lock = i.item

        if failed_to_lock:
            info = 'One of the items offered is not available!'
            for i in locked:
                i.available = 'available'
                i.save()
            return render(request, 'info.html', {'info': info} )

        for o in wantedItem.offers:
            o.status = 'rejected'

        ofr.status = 'accepted'
        wantedItem.available = 'traded'
        wantedItem.save()
        
        return render(request, 'info.html', {'info': 'Accepted!'} )

# Using PyMongo 
def acquire_pending_lock(generic_item):
    raw = GenericItem._get_collection()
    result = raw.find_and_modify(
        query = { '_id': generic_item.id, 'available':'available' },
        update = { '$set':{'available': 'locked'} }
        )
    
    s = ''
    if result is None:
        s = '*** Could not acquire pending lock for: %s id:%s'\
         %(generic_item.title, generic_item.id)
    else:
        s = '*** Acquired pending lock for: %s id:%s' %(generic_item.title, generic_item.id)

    logger.info(s)

    return result

@login_required
def testEmbeddedDocumentForm(request, item_id):
    wantedItem = GenericItem.objects.get(pk=item_id)

    if wantedItem.available != 'available':
        return render(request, 'info.html', {'info': 'Item not available!' })

    myItems = GenericItem.objects.filter(owner_id=request.user.id)
    if myItems:
        for i in myItems:
            for o in i.offers:
                for x in o.items:
                    if x.item == wantedItem:
                        s = 'This item is part of an offer made to one of your items,'+\
                        ' please respond to that offer first!'
                        return render(request, 'info.html', {'info': s })

    if request.POST: 
        
        form = TestOfferForm( data=request.POST, parent_document=wantedItem)
        
        if form.is_valid():    
            ofr = form.save(commit=False)
            ofr.author = request.user.username
            ofr.author_id = request.user.id
            ofr.slug = slugify(ofr.title)
            form.save()
            return HttpResponseRedirect('/thanks/')
        else:
            return render(request, 'testEmbeddedDocumentForm.html', {
            'form': form,
            'wantedItem': wantedItem
        })


    else:
        form = TestOfferForm( user_id=request.user.id, parent_document=wantedItem)
        #form = TestOfferForm(parent_document=wantedItem)
        
        return render(request, 'testEmbeddedDocumentForm.html', {
            'form': form,
            'wantedItem': wantedItem
        })


def offers_for_item(request, item_id):
    wantedItem = GenericItem.objects.get(pk=item_id)

    return render(request, 'all_offers_for_item.html', {
            'item': wantedItem
    })


def specific_offer(request, item_id, offer_title_slug):
    wantedItem = GenericItem.objects.get(pk=item_id)
    
    ofr = None

    if not wantedItem:
        raise Http404
    else:
        for o in wantedItem.offers:
            if offer_title_slug == o.slug:
                ofr = o

    if not ofr:
        raise Http404     

    return render(request, 'specific_offer_for_item.html', {
            'offer': ofr,
            'item': wantedItem
    })    


def testImage(request):
    
    if request.POST:
        #import ipdb; ipdb.set_trace()
        form = TestImageForm(request.POST, request.FILES) 
        
        if form.is_valid():
            instance = ImageTest()
            instance.title = form.cleaned_data['title']
            instance.foto = request.FILES['img']
            instance.save()

            return HttpResponseRedirect('/thanks/')

    else:
        form = TestImageForm()
        return render(request, 'testImage.html', { 'form': form })


def profile_detail_extended(request, username, template_name):
    #logger.info('new profile')
    extra_context = dict()
    #extra_context['extra'] = 'boom!'
    
    extra_context['active_items'] = GenericItem.objects.filter(\
        available = 'available',owner_id = request.user.id).count()
        
    extra_context['traded_out'] = GenericItem.objects.filter(\
        available = 'traded',owner_id = request.user.id).count()
        
    extra_context['traded_in'] = GenericItem.objects(__raw__={ \
        'offers.author_id': request.user.id, 'offers.status': 'accepted' }).count()
    
    return profile_detail(request, username,\
    template_name=template_name, extra_context=extra_context)
