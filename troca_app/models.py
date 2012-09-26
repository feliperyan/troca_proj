#from django.db import models
from mongoengine import *


class ItemInOffer(EmbeddedDocument):
    itemTitle = StringField(max_length=70, required=True)
    value = IntField()
    item = GenericReferenceField()

    def __unicode__(self):
        return self.itemTitle
    
    class Meta:
        app_label = 'troca_app'

class Offer(EmbeddedDocument):
    title = StringField(max_length=70, required=True)
    author = StringField(max_length=70, required=True)
    items = ListField(EmbeddedDocumentField('ItemInOffer'))
    
    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'troca_app'

class GenericItem(Document):
    title = StringField(max_length=70, required=True)
    description = StringField(max_length=140, required=True)
    value = IntField()
    location = GeoPointField()
    offers = ListField(EmbeddedDocumentField('Offer'))

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'troca_app'
