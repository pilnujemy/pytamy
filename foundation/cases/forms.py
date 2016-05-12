# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from braces.forms import UserKwargModelFormMixin
from atom.ext.crispy_forms.forms import HelperMixin, SingleButtonMixin
from crispy_forms.layout import Submit
from foundation.letters.models import Letter
from .models import Case
from foundation.offices.models import Email
from ckeditor.widgets import CKEditorWidget
from foundation.letters.utils import can_send
# from autocomplete_light import shortcuts as autocomplete_light


class CaseForm(UserKwargModelFormMixin, SingleButtonMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Case
        fields = ['name']


class NewCaseForm(HelperMixin, UserKwargModelFormMixin, forms.ModelForm):
    letter = None
    text = forms.CharField(widget=CKEditorWidget(),
                           label=_("Inquire"))
    # email = autocomplete_light.ModelChoiceField('EmailAutocomplete')

    def __init__(self, *args, **kwargs):
        super(NewCaseForm, self).__init__(*args, **kwargs)
        self.instance.created_by = self.user
        self.helper.add_input(Submit('save', _("Save"), css_class="btn-primary"))
        if can_send(self.user, self.instance):
            self.helper.add_input(Submit('send', _("Save & send"), css_class="btn-primary"))

    def save(self, *args, **kwargs):
        self.instance.office = self.cleaned_data['email'].office
        super(NewCaseForm, self).save(*args, **kwargs)
        letter = Letter(case=self.instance,
                        subject=self.cleaned_data['name'],
                        content=self.cleaned_data['text'],
                        email=self.cleaned_data['email'],
                        author=self.user)
        if 'send' in self.data and can_send(self.user, self.instance):
            letter.send(user=self.user)
        letter.save()
        self.letter = letter
        return self.instance

    class Meta:
        model = Case
        fields = ['name']
