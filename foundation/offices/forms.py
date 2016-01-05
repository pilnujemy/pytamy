# -*- coding: utf-8 -*-
from django import forms
from .models import Office, Email
from braces.forms import UserKwargModelFormMixin
from django.utils.translation import ugettext as _
from atom.ext.crispy_forms.forms import SingleButtonMixin
from autocomplete_light.contrib.taggit_field import TaggitField, TaggitWidget
from autocomplete_light import shortcuts as autocomplete_light
from crispy_forms.layout import Layout, Fieldset

OFFICE_FORM_FIELD = ['name', 'jst', 'parent', 'krs', 'regon', 'tags', 'postcode']

EMAIL_HELP_TEXT = _("After creating the office, you can add another e-mail addresses.")


class CreateOfficeForm(SingleButtonMixin, UserKwargModelFormMixin,  autocomplete_light.ModelForm):
    email = forms.EmailField(label=_("E-mail address"),
                             help_text=EMAIL_HELP_TEXT)
    tags = TaggitField(widget=TaggitWidget('TagAutocomplete'), required=False)

    def __init__(self, *args, **kwargs):
        super(CreateOfficeForm, self).__init__(*args, **kwargs)
        self.instance.created_by = self.user
        self._email = Email()
        self.helper.layout = Layout(
            Fieldset(
                _('Identification'),
                'name',
                'jst',
                'krs',
                'regon',
                'postcode'
            ),
            Fieldset(
                _('Contacts'),
                'email',
                'parent',
            ),
            Fieldset(
                _('Other'),
                'tags',
            ),
        )

    def save_email(self, commit=True):
        self._email.office = self.instance
        self._email.created_by = self.user
        self._email.email = self.cleaned_data['email']
        if commit:
            self._email.save()
        return self._email

    def save(self, commit=True, *args, **kwargs):
        super(CreateOfficeForm, self).save(commit=True, *args, **kwargs)
        if self.cleaned_data['email']:
            self.save_email()
        return self.instance

    class Meta:
        model = Office
        fields = OFFICE_FORM_FIELD
        autocomplete_names = {'jst': 'JSTCommunityAutocomplete'}


class OfficeForm(UserKwargModelFormMixin, SingleButtonMixin, forms.ModelForm):
    tags = TaggitField(widget=TaggitWidget('TagAutocomplete'))

    class Meta:
        model = Office
        fields = OFFICE_FORM_FIELD


class EmailForm(UserKwargModelFormMixin, SingleButtonMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            self.instance.created_by = self.user

    class Meta:
        model = Email
        fields = ['email', 'office', 'default']
