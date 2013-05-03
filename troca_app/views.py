# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from models import *
from forms import *
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic import ListView

from django.utils import simplejson

from django.shortcuts import get_object_or_404

from django.template.defaultfilters import slugify

def categories(request):
    return render(request, 'select_categories.html', )



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
    items = GenericItem.objects.all()
    return render(request, 'index.html', {'Items': items})



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

    if request.method == 'POST':        
        
        if category == 'Muffins':
            form = ModelFormMuffin(request.POST, request.FILES)        
        
        elif category == 'Cameras':
            form = ModelFormCameras(request.POST, request.FILES)        
        
        else:        
            form = ModelFormGenericItem(request.POST, request.FILES)

        #form = ModelFormGenericItem(request.POST)

        #import ipdb; ipdb.set_trace()
        if form.is_valid():

            instance = form.save(commit = False)
            instance.owner_id = request.user.id
            instance.owner_username = request.user.username
            
            instance.save()
            
            return HttpResponseRedirect('/thanks/')

    else:
        # Ensure that this is a "final" category:
        p = get_object_or_404( Category, categoryTitle = category )        
        i = Category.objects.filter( parentCategory = p )
        if i.count() != 0:
            raise Http404

        if category == 'Muffins':
            form = ModelFormMuffin()
        
        elif category == 'Cameras':
            form = ModelFormCameras()
        
        else:        
            form = ModelFormGenericItem()

    return render(request, 'item.html', {
        'form': form,
        'category': category,
    } )


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


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

#Could not use standard @login_required decorator since this is a ClassBased GenericView...
class ItemsForLoggedUser(ListView):
    
    context_object_name = 'myItems'
    template_name = 'myItems.html'

    #Overloading the get_queryset method of ListView
    def get_queryset(self):
        the_id = self.request.user.id
        return GenericItem.objects.filter(owner_id = the_id)


def testEmbeddedDocumentForm(request, item_id):
    wantedItem = GenericItem.objects.get(pk=item_id)

    if request.POST: 
        
        form = TestOfferForm(parent_document=wantedItem, data=request.POST)

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



