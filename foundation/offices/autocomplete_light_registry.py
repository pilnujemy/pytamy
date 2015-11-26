from __future__ import absolute_import
import autocomplete_light
from .models import Email


class EmailAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['email', 'office__name']
    model = Email
    add_another_url_name = 'offices:create'
autocomplete_light.register(EmailAutocomplete)
