from django import forms
from django.forms import ModelForm
from .models import savedSearch
from django.utils.translation import gettext_lazy as _

class savedSearchForm(ModelForm):

    class Meta:
        model = savedSearch
        fields = [
            'hunter', 'name', 'terms', 'source', 'price_min', 'price_max',
            'sort', 'url', 'is_subscribed',]

        labels = {
            'name': _('What\'s a good, memorable name for this search?'),
            'is_subscribed': _('I want to receive an email when new cameras match this search.'),
        }

        widgets = {
            'hunter': forms.HiddenInput(),
            'terms': forms.HiddenInput(),
            'source': forms.HiddenInput(),
            'price_min': forms.HiddenInput(),
            'price_max': forms.HiddenInput(),
            'sort': forms.HiddenInput(),
            'url': forms.HiddenInput(),
            }
