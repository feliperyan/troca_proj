from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from troca_app.models import Category

admin.site.register(Category)

#admin.site.register(User)
#admin.site.register(Group)
#admin.site.register(Site)