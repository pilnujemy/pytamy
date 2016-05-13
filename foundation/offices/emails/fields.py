from dal import autocomplete
from django import forms
from django.utils.translation import ugettext as _

from .models import Email


class EmailAutocompleteField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['label'] = kwargs.get('label', _('E-mail'))
        kwargs['queryset'] = Email.objects.all()
        kwargs['widget'] = autocomplete.ModelSelect2(url='offices:emails:autocomplete',
                                                     forward=['office'])
        super(EmailAutocompleteField, self).__init__(*args, **kwargs)
