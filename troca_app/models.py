from mongoengine import *
from django.contrib.auth.models import User
from django.db import models
from django.db.models import datetime

import os
from django.contrib.auth.models import User
from django_facebook.models import BaseFacebookProfileModel

from custom_fields import DJFileField

from userena.models import UserenaBaseProfile

class TrocaUserProfile(BaseFacebookProfileModel, UserenaBaseProfile):
    '''
    From django_facebook
    '''
    user = models.OneToOneField('auth.User')
    image = models.ImageField(blank=True, null=True, upload_to='profile_pics', max_length=255)

    

#Make sure we create a MyCustomProfile when creating a User
from django.db.models.signals import post_save

def create_facebook_profile(sender, instance, created, **kwargs):
    if created:
        TrocaUserProfile.objects.create(user=instance)

post_save.connect(create_facebook_profile, sender=User)


class Category(models.Model):
    categoryTitle = models.CharField(max_length=100, )
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

class Vote(EmbeddedDocument):
    author_id = IntField(required=True)
    direction = IntField(required=True)
    date_voted = DateTimeField(default=datetime.datetime.now)

class GenericItem(Document):
    owner_id = IntField(required=True)
    owner_username = StringField(max_length=70, required=True)
    title = StringField(max_length=70, required=True)
    description = StringField(max_length=140, required=True)
    value = IntField()
    geo_location = GeoPointField()
    text_location = StringField(max_length=128, required=False)
    date_added = DateTimeField(default=datetime.datetime.now)
    offers = ListField(EmbeddedDocumentField('Offer'))
    img = DJFileField(upload_to = 'ups')
    available = StringField(max_length=70, default='available')
    votes = ListField(EmbeddedDocumentField('Vote'))

    def hasAlreadyVoted(self, user_id):
        for v in self.votes:
            if v.author_id == user_id:
                return True
        return False

    #Tally up the votes:
    def countVotes(self):
        sum = 0
        for v in self.votes:
            sum += v.direction
        return sum

    #Used to check and alert users if they have already made an offer to this item.
    def hasAlreadyMadeOffer(self, user_id):
        for o in self.offers:
            if o.author_id == user_id:
                return True
        return False

    # Called when this item is no longer available:
    def reject_all_offers(reason):
        for o in self.offers:
            if reason:
                o.status = 'reason'
            else:
                o.status = 'rejected'

    def get_offer_by_slug(self, slug_title):
        for o in self.offers:
            if slug_title == o.slug:
                return o
        return None

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
    author_id = IntField(required=False)
    author = StringField(max_length=70, required=False)
    items = ListField(EmbeddedDocumentField('ItemInOffer'))
    
    # Change to Status = ChoiceField?
    status = StringField(max_length=70, default='pending')
    
    datetime_made = DateTimeField(default=datetime.datetime.now)
    slug = StringField(max_length=70, required=False)

    def __unicode__(self):
        return self.title

    _meta = {}


class Muffin(GenericItem):
    baked_on = DateTimeField()

class Camera(GenericItem):
    brand = StringField(max_length=70)


class ImageTest(Document):
    title = StringField(max_length=70, required=True)
    foto = DJFileField(upload_to = 'ups')


