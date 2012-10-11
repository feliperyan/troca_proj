from django import forms

class GenericItemForm(forms.Form):
	title = forms.CharField(max_length=100)
	description = forms.CharField(max_length=100)
	value = forms.IntegerField()
	#location = forms.CharField(max_length=100)
	#offers = forms.CharField(max_length=100)