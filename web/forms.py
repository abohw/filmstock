from django import forms
from django.forms import ModelForm
from .models import savedSearch

class savedSearchForm(ModelForm):

    class Meta:
        model = savedSearch
        fields = [
            'hunter', 'name', 'terms', 'source', 'price_min', 'price_max',
            'new', 'sort', 'url',]
        widgets = {
            'hunter': forms.HiddenInput(),
            'terms': forms.HiddenInput(),
            'source': forms.HiddenInput(),
            'price_min': forms.HiddenInput(),
            'price_max': forms.HiddenInput(),
            'new': forms.HiddenInput(),
            'sort': forms.HiddenInput(),
            'url': forms.HiddenInput(),
            }
