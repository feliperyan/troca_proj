# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import *
from forms import *
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView

def index(request):
    items = GenericItem.objects.all()
    return render(request, 'index.html', {'Items': items})


def thanks(request):
	return render(request, 'thanks.html', {})

@login_required
def genericItem(request):
	if request.method == 'POST':
		form = GenericItemForm(request.POST)

		print "request is post."

		if form.is_valid():
			#process the data in form.cleaned_data
			t = form.cleaned_data['title']
			d = form.cleaned_data['description']
			v = form.cleaned_data['value']

			#item = GenericItem(owner_id=request.user.id, title=t, description=d, value=v, location=None, offers=[])
			item = Car(owner_id=request.user.id, title=t, description=d, value=v, location=None, offers=[])
			item.save()

			return HttpResponseRedirect('/thanks/')

	else:
		form = GenericItemForm()

	return render(request, 'item.html', {
		'form': form,
	} )


#Could not use standard @login_required decorator since this is a ClassBased GenericView...
class ItemsForLoggedUser(ListView):
	
	context_object_name = 'myItems'
	template_name = 'myItems.html'


	def get_queryset(self):
		the_id = self.request.user.id
		return GenericItem.objects.filter(owner_id = the_id)









