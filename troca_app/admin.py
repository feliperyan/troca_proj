from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from troca_app.models import Category, TrocaUserProfile
from userena.models import *

admin.site.register(UserenaSignup)
admin.site.register(Category)
