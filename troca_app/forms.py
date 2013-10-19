from django import forms
from django.forms import ModelMultipleChoiceField
from troca_app.models import *
from django.forms import ImageField
from django.forms.fields import CharField, MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from mongodbforms import DocumentForm
from mongodbforms import EmbeddedDocumentForm
from mongodbforms import ListField
from django.core.validators import EMPTY_VALUES
from django.forms.util import ErrorList
import re
from mongodbforms import DocumentMultipleChoiceField
from PIL import Image

# Custom Form Fields:

class PointFieldForm(CharField):
    def clean(self, value):
        clean_data = value.split(',')

        #import ipdb; ipdb.set_trace()

        if value in EMPTY_VALUES and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        elif value in EMPTY_VALUES and not self.required:
            return None

        if len(clean_data) != 2:
            forms.ValidationError('Incorrect number of parameters. Expecting: lon, lat')

        
        lat = float(clean_data[0])
        lon = float(clean_data[1])
        clean_data = {'type': 'Point', 'coordinates': [lat, lon]}

        return clean_data


# Forms for adding items:


class ModelFormGenericItem(DocumentForm):
    class Meta:
        document = GenericItem
        fields = ('title', 'value', 'description', 'img', 'geo_location', 'w_cat')

    c = list(Category.objects.all())
    cats = []
    for x in c:
        cats.append( ( x.id, x.categoryTitle ) )
    
    img = forms.ImageField(widget=forms.ClearableFileInput, label='Image')
    geo_location = PointFieldForm(required=False, widget=forms.HiddenInput)
    w_cat = MultipleChoiceField(widget=CheckboxSelectMultiple, required=False, choices=cats)

    def clean_img(self):
        cleaned_data = super(ModelFormGenericItem,self).clean()
        image = cleaned_data.get("img")
                
        if image:
            if image._size > 4*1024*1024:
                raise forms.ValidationError(
                   "Image Must be <4mb Less")
            if not image.name[-3:].lower() in ['jpg','png']:
                raise forms.ValidationError(
                   "Your file extension was not recongized")
            try: 
                Image.open(image)
            except IOError:
                raise forms.ValidationError(
                   "Your file doesn't appear to be a real picture.")
                
        return image


class VehicleForm(DocumentForm):
    class Meta:
        document = Vehicle
        fields = ('title', 'value', 'description', 'img', 'geo_location', 'model')


class SkillForm(ModelFormGenericItem):
    class Meta:
        document = Skill
        fields = ('title', 'skill_name', 'skill_level', 'class_duration', 'value', 'description', 'img', 'geo_location')


# Forms for making Offers:


class SelectMultipleItemsField(DocumentMultipleChoiceField):
#class SelectMultipleItemsField(ModelMultipleChoiceField):
    # def prepare_value(self, value):
    #     if hasattr(value, '_meta'):
    #         if self.to_field_name:
    #             return value.serializable_value(self.to_field_name)
    #         else:
    #             return value.pk
        
    #     return super(SelectMultipleItemsField, self).prepare_value(value)

    def clean(self, value):
        #import ipdb; ipdb.set_trace();

        littleItems = list()
        
        for pk in value:
            wholeItem = GenericItem.objects.get(pk=pk)
            partialItem = ItemInOffer(itemTitle=wholeItem.title, value=wholeItem.value, item=wholeItem)
            littleItems.append(partialItem)

        return littleItems


class TestOfferForm(EmbeddedDocumentForm):

    class Meta:
        document = Offer
        embedded_field_name = 'offers' 
        #fields = ['title']
        fields = ['title', 'items']

    items = SelectMultipleItemsField (queryset=GenericItem.objects.filter(owner_id=0), widget=forms.CheckboxSelectMultiple, required=True)

    def __init__(self, user_id=None, parent_document=None, data=None):
        #import ipdb; ipdb.set_trace();
        super(TestOfferForm, self).__init__(parent_document=parent_document, data=data)
        self.fields['items'].queryset = GenericItem.objects.filter(owner_id = user_id, available='available')


class TestImageForm(forms.Form):
    title = forms.CharField(max_length=100)
    img = forms.ImageField(widget=forms.ClearableFileInput)



