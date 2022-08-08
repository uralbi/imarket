from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Item, ItemGallery, SavedItem
import re
from django.forms import inlineformset_factory

class Item_Creation_Form(forms.ModelForm):
    status_choice = (
        ('Selling', 'selling'),
        ('Buying', 'buying'),
        ('Renting', 'renting'),
        ('For Rent', 'for rent'),
    )
    status = forms.ChoiceField(choices=status_choice)

    class Meta:
        model = Item
        fields = ['item_name', 'description', 'price', 'status', 'category', 'image1']
        labels = {'image1': 'Item photo'}

    def __init__(self, *args, **kwargs):
        super(Item_Creation_Form, self).__init__(*args, **kwargs)
#         self.fields['item_name'].widget.attrs['placeholder'] = 'Item Name'
#         self.fields['description'].widget.attrs['placeholder'] = 'Description'
#         self.fields['price'].widget.attrs['placeholder'] = 'Price'
#         self.fields['image1'].widget = 'Photo'
        self.fields['description'].widget.attrs['rows'] = 4
        self.fields['description'].widget.attrs['columns'] = 15
        self.fields['price'].widget.attrs['step'] = 0.01
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control inner_shadow'


class GalleryForm(forms.ModelForm):
    image = forms.ImageField(required=True, error_messages={'invalid':("Image files only")})
    class Meta:
        model = ItemGallery
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control py-0'
            self.fields[field].widget.attrs['required'] = True


class SavedItem_Form(forms.ModelForm):
    class Meta:
        model = SavedItem
        fields = ['user', 'item']
