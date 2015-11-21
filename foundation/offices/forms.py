# -*- coding: utf-8 -*-
from django import forms
from .models import Office, Email
from braces.forms import UserKwargModelFormMixin
from django.utils.translation import ugettext as _
from atom.ext.crispy_forms.forms import SingleButtonMixin

OFFICE_FORM_FIELD = ['name', 'jst', 'parent', 'krs', 'regon', 'tags', 'postcode']


class CreateOfficeForm(SingleButtonMixin, UserKwargModelFormMixin, forms.ModelForm):
    email = forms.EmailField(label=_("E-mail address"))

    def __init__(self, *args, **kwargs):
        super(CreateOfficeForm, self).__init__(*args, **kwargs)
        self.instance.created_by = self.user
        self._email = Email()

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


class OfficeForm(UserKwargModelFormMixin, forms.ModelForm):
    class Meta:
        model = Office
        fields = OFFICE_FORM_FIELD


class EmailForm(UserKwargModelFormMixin, forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email', 'default']
