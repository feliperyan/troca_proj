from mongoengine import *
from django.contrib.auth.models import User
from django.db import models
from django.db.models import datetime
import os
from django.contrib.auth.models import User
from django_facebook.models import BaseFacebookProfileModel
from custom_fields import DJFileField, LocalImageField
from userena.models import UserenaBaseProfile
from django.db.models.signals import post_save


class TrocaUserProfile(BaseFacebookProfileModel, UserenaBaseProfile):
    user = models.OneToOneField('auth.User')
    image = models.ImageField(blank=True, null=True, upload_to='profile_pics', max_length=255)


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
            printable = oneUp.categoryTitle +' > ' + printable
            oneUp = oneUp.parentCategory
        
        return printable

    def howToOrder(self):
        oneUp = self.parentCategory
        printable = self.categoryTitle
        while oneUp:    
            printable = oneUp.categoryTitle +' > '+ printable
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
    geo_location = PointField(required=False)
    text_location = StringField(max_length=128, required=False)
    date_added = DateTimeField(default=datetime.datetime.now)
    offers = ListField(EmbeddedDocumentField('Offer'))
    img = LocalImageField(upload_to = 'ups')
    available = StringField(max_length=70, default='available')
    votes = ListField(EmbeddedDocumentField('Vote'))
    v_count = IntField(default=0)
    cat =  StringField(max_length=140, default='generic')
    w_cat = ListField(StringField(max_length=50))
    
    meta = { 'allow_inheritance': True }        

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
                o.status = reason
            else:
                o.status = 'rejected'

    def get_offer_by_slug(self, slug_title):
        for o in self.offers:
            if slug_title == o.slug:
                return o
        return None

    def __unicode__(self):
        return self.title
    
    def fields_for_detail_template(self):
        fs = [ 'title', 'description', 'value' ]
        return fs
    
    def get_name_vals(self):
        fs = self.fields_for_detail_template()
        r = []
        for f in fs:
            name = self._fields[f].verbose_name
            val = self.__getattribute__(f)
            r.append( (name, val) )
        
        return r


class Vehicle(GenericItem):
    model = StringField(max_length=70, required=True)


class Ticket(GenericItem):
    category_slug = 'Tickets and Reservations'
    date = DateTimeField(verbose_name='Date of event', default=datetime.datetime.now)
    location = StringField(verbose_name='Location of event', max_length=200, required=True)
    
    def fields_for_detail_template(self):
        f_wanted = ['date', 'location']
        fs = super(Ticket, self).fields_for_detail_template()
        for i in f_wanted: fs.append( i )
        return fs

class Skill(GenericItem):
    sk_lvl = (
        ('B', 'Beginner'),
        ('A', 'Average'),
        ('E', 'Expert'),
    )
    category_slug = 'Skills'
    
    skill_name = StringField(verbose_name='Name of the skill', max_length=140, required=True)
    skill_level = StringField(verbose_name='Skill level', max_length=1, required=True, choices=sk_lvl, default='B')
    class_duration = IntField(verbose_name='Duration of class')
    date = DateTimeField(default=datetime.datetime.now)

    def fields_for_detail_template(self):
        f_wanted = ['skill_level', 'skill_name', 'class_duration', 'date']
        fs = super(Skill, self).fields_for_detail_template()
        for i in f_wanted: fs.append( i )
        return fs
        

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
    items = ListField(EmbeddedDocumentField('ItemInOffer'), required=True)
    
    # Change to Status = ChoiceField?
    status = StringField(max_length=70, default='pending')
    
    datetime_made = DateTimeField(default=datetime.datetime.now)
    slug = StringField(max_length=70, required=False)

    def __unicode__(self):
        return self.title

    _meta = {}


class ImageTest(Document):
    title = StringField(max_length=70, required=True)
    foto = DJFileField(upload_to = 'ups')


