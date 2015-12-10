from __future__ import absolute_import, unicode_literals
from autocomplete_light import shortcuts as autocomplete_light
from .models import Email, Office
from taggit.models import Tag
autocomplete_light.register(Tag)


class EmailAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['email', 'office__name']
    model = Email
    add_another_url_name = 'offices:create'

    def choice_label(self, obj):
        return "{office} ({email})".format(office=obj.office.name,
                                           email=obj.email)
autocomplete_light.register(EmailAutocomplete)


class OfficeAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['name', ]
    model = Office
    add_another_url_name = 'offices:create'
autocomplete_light.register(OfficeAutocomplete)


