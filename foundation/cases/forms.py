# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from braces.forms import UserKwargModelFormMixin
from atom.ext.crispy_forms.forms import HelperMixin, SingleButtonMixin
from crispy_forms.layout import Submit
from foundation.letters.models import Letter
from .models import Case
from foundation.offices.models import Email


class CaseForm(UserKwargModelFormMixin, SingleButtonMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Case
        fields = ['name']


class NewCaseForm(HelperMixin, UserKwargModelFormMixin, forms.ModelForm):
    message = None
    letter = None
    text = forms.CharField(widget=forms.Textarea(),
                           label=_("Inquire"))
    email = forms.ModelChoiceField(queryset=Email.objects.all())

    def __init__(self, *args, **kwargs):
        super(NewCaseForm, self).__init__(*args, **kwargs)
        self.instance.created_by = self.user
        self.helper.add_input(Submit('save', _("Save"), css_class="btn-primary"))
        self.helper.add_input(Submit('send', _("Save & send"), css_class="btn-primary"))

    def save(self, *args, **kwargs):
        self.instance.office = self.cleaned_data['email'].office
        obj = super(NewCaseForm, self).save(*args, **kwargs)
        letter = Letter(case=obj)
        letter.name = self.cleaned_data['name']
        letter.content = self.cleaned_data['text']
        letter.recipient = obj.office
        letter.email = self.cleaned_data['email']
        letter.sender_user = self.user
        letter.save()
        self.message = None
        if 'send' in self.data:
            message = letter.send_to_office(user=self.user)
            self.message = message
        self.letter = letter
        return self.instance

    class Meta:
        model = Case
        fields = ['name']

