#from django.db import models
from mongoengine import *
from django.contrib.auth.models import User

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
        abstract = True
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
    items = ListField(EmbeddedDocumentField('ItemInOffer'))
    
    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'troca_app'


class Muffin(GenericItem):
    baked_on = DateTimeField(required=False)

class Car(GenericItem):
    kilometers = IntField(required=False)


