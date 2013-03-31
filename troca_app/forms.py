from django import forms
from django.forms import ModelMultipleChoiceField
from troca_app.models import *
from django.forms import ModelForm

from mongodbforms import DocumentForm
from mongodbforms import EmbeddedDocumentForm

class FormGenericItem(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
    value = forms.IntegerField()
    

    
# Don't think I can use ModelForms with a Model object that inherits from Document
# and not models.Model ...

class ModelFormGenericItem(DocumentForm):
   class Meta:
       document = GenericItem
       fields = ('title', 'value', 'description')


class ModelFormMuffin(DocumentForm):
    class Meta:
        document = Muffin
        fields = ('title', 'value', 'description')


class ModelFormCameras(DocumentForm):
    class Meta:
        document = Camera
        fields = ('title', 'value', 'description', 'brand')


# Here we use a dummy `queryset`, because ModelChoiceField
# see: http://stackoverflow.com/questions/4789466/populate-a-django-form-with-data-from-database-in-view

# Bloody "objects" object from the GenericItem model, which inherits from Document and not models.Model 

# class MakeOfferForm(forms.Form):
#     itemsToOffer = forms.ModelMultipleChoiceField \
#         (queryset=Category.objects.none(), required=True)
    
#     title = forms.CharField(max_length = 100)

#     def __init__(self, user_id):
#         super(MakeOfferForm, self).__init__()
#         self.fields['itemsToOffer'].queryset =\
#          GenericItem.objects.filter(owner_id = user_id)

class SelectMultipleItemsField(ModelMultipleChoiceField):
    def prepare_value(self, value):
        if hasattr(value, '_meta'):
            if self.to_field_name:
                return value.serializable_value(self.to_field_name)
            else:
                return value.pk
        
        return super(SelectMultipleItemsField, self).prepare_value(value)

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
        fields = ['title', 'items']

    items = SelectMultipleItemsField \
        (queryset=GenericItem.objects.filter(owner_id=0), widget=forms.CheckboxSelectMultiple, required=True)

    def __init__(self, user_id=None, parent_document=None, data=None):
        super(TestOfferForm, self).__init__(parent_document, data)
        self.fields['items'].queryset =\
         GenericItem.objects.filter(owner_id = user_id)





