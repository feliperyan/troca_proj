#from django.db import models
from mongoengine import *
from django.contrib.auth.models import User
from django.db import models
from django.db.models import *

import os
from django.contrib.auth.models import User
from django_facebook.models import BaseFacebookProfileModel


class TrocaUserProfile(BaseFacebookProfileModel):
    '''
    From django_facebook
    '''
    user = models.OneToOneField('auth.User')
    image = models.ImageField(blank=True, null=True, upload_to='newprofiles', max_length=255)

    class Meta:
        app_label = 'django_facebook'

#Make sure we create a MyCustomProfile when creating a User
from django.db.models.signals import post_save

def create_facebook_profile(sender, instance, created, **kwargs):
    if created:
        TrocaUserProfile.objects.create(user=instance)

post_save.connect(create_facebook_profile, sender=User)


class Category(models.Model):
    categoryTitle = CharField(max_length=100, )
    parentCategory = models.ForeignKey('self', null=True, blank=True, related_name='subs')

    def __unicode__(self):
        oneUp = self.parentCategory
        printable = self.categoryTitle
        while oneUp:    
            printable = oneUp.categoryTitle +'>' + printable
            oneUp = oneUp.parentCategory
        
        return printable

    def howToOrder(self):
        oneUp = self.parentCategory
        printable = self.categoryTitle
        while oneUp:    
            printable = oneUp.categoryTitle +'>'+ printable
            oneUp = oneUp.parentCategory
        
        return printable

    class Meta:
        verbose_name_plural = "Categories"
        #app_label = 'relational'




class GenericItem(Document):
    owner_id = IntField(required=True)
    title = StringField(max_length=70, required=True)
    description = StringField(max_length=140, required=True)
    value = IntField()
    location = GeoPointField()
    offers = ListField(EmbeddedDocumentField('Offer'))

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = False
        app_label = 'troca_app'
        db_table = 'generic_item'
        allow_inheritance = True

        

class ItemInOffer(EmbeddedDocument):
    itemTitle = StringField(max_length=70, required=True)
    value = IntField()
    item = ReferenceField(GenericItem)

    def __unicode__(self):
        return self.itemTitle
    
    class Meta:
        app_label = 'troca_app'

class Offer(EmbeddedDocument):
    title = StringField(max_length=70, required=True)
    author_id = IntField(required=True)
    author = StringField(max_length=70, required=True)
    items = ListField(EmbeddedDocumentField('ItemInOffer'))
    
    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'troca_app'


class Muffin(GenericItem):
    baked_on = DateTimeField()

class Camera(GenericItem):
    brand = StringField(max_length=70)


