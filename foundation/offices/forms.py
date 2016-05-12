# -*- coding: utf-8 -*-
from django import forms
from .models import Office
from braces.forms import UserKwargModelFormMixin
from django.utils.translation import ugettext as _
from atom.ext.crispy_forms.forms import SingleButtonMixin
# from autocomplete_light.contrib.taggit_field import TaggitField, TaggitWidget
# from autocomplete_light import shortcuts as autocomplete_light
from crispy_forms.layout import Layout, Fieldset

EMAIL_HELP_TEXT = _("After creating the office, you can add another e-mail addresses.")

OFFICE_FORM_FIELD = ['name', 'jst', 'parent', 'krs', 'regon', 'tags', 'postcode']


class OfficeForm(SingleButtonMixin, UserKwargModelFormMixin,  forms.ModelForm):
    email = forms.EmailField(label=_("E-mail address"),
                             help_text=EMAIL_HELP_TEXT)
    # TODO: tags = TaggitField(widget=TaggitWidget('TagAutocomplete'), required=False)

    def __init__(self, *args, **kwargs):
        super(OfficeForm, self).__init__(*args, **kwargs)
        self.instance.created_by = self.user
        self.helper.layout = Layout(
            Fieldset(
                _('Identification'),
                'name',
                'krs',
                'regon',
                'postcode'
            ),
            Fieldset(
                _('Relations'),
                'jst',
                'parent',
            ),
            Fieldset(
                _('Other'),
                'tags',
            ),
        )

    class Meta:
        model = Office
        fields = OFFICE_FORM_FIELD
        autocomplete_names = {'jst': 'JSTCommunityAutocomplete'}
