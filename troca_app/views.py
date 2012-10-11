# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import *
from forms import *


def index(request):
    items = GenericItem.objects.all()
    return render(request, 'index.html', {'Items': items})


def thanks(request):
	return render(request, 'thanks.html', {})


def genericItem(request):
	if request.method == 'POST':
		form = GenericItemForm(request.POST)

		print "request is post."

		if form.is_valid():
			#process the data in form.cleaned_data
			t = form.cleaned_data['title']
			d = form.cleaned_data['description']
			v = form.cleaned_data['value']

			item = GenericItem(title=t, description=d, value=v, location=None, offers=[])
			item.save()

			return HttpResponseRedirect('/thanks/')

	else:
		form = GenericItemForm()

	return render(request, 'item.html', {
		'form': form,
	} )

