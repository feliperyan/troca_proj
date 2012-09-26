# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from models import *


def index(request):
    
    items = GenericItem.objects.all()

    return render(request, 'index.html', {'Items': items})

    #return HttpResponse('OK')
