# -*- coding: utf-8 -*-
from atom.ext.crispy_forms.forms import HelperMixin, SingleButtonMixin
from braces.forms import UserKwargModelFormMixin
from ckeditor.widgets import CKEditorWidget
from crispy_forms.layout import Div, Fieldset, Layout, Submit
from dal import autocomplete
from django import forms
from django.utils.translation import ugettext_lazy as _

from foundation.letters.models import OutgoingLetter
from foundation.letters.utils import can_send
from foundation.offices.emails.models import Email

from .models import Case


class CaseForm(UserKwargModelFormMixin, SingleButtonMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Case
        fields = ['name']


class NewCaseForm(HelperMixin, UserKwargModelFormMixin, forms.ModelForm):
    email = forms.ModelChoiceField(
        queryset=Email.objects.all(),
        widget=autocomplete.ModelSelect2(url='offices:emails:autocomplete',
                                         forward=['office'])
    )
    subject = forms.CharField(max_length=250, label=_("Subject"))
    text = forms.CharField(widget=CKEditorWidget(),
                           label=_("Inquire"))

    def __init__(self, *args, **kwargs):
        super(NewCaseForm, self).__init__(*args, **kwargs)
        self.instance.created_by = self.user
        self.helper.add_input(Submit('save', _("Save"), css_class="btn-primary"))
        if can_send(self.user, self.instance):
            self.helper.add_input(Submit('send', _("Save & send"), css_class="btn-primary"))
        self.instance.created_by = self.user
        self.helper.layout = Layout(
            Fieldset(
                _('Identification'),
                'name',
            ),
            Fieldset(
                _('Recipient'),
                Div(
                    Div('office', css_class='col-sm-6'),
                    Div('email', css_class='col-sm-6'),
                    css_class='row'
                ),
                'postcode'
            ),
            Fieldset(
                _('Content'),
                'subject',
                'text',
            ),
        )

    def save_letter(self):
        letter = OutgoingLetter(case=self.instance,
                                office=self.cleaned_data['office'],
                                subject=self.cleaned_data['subject'],
                                content=self.cleaned_data['text'],
                                email=self.cleaned_data['email'].email,
                                author=self.user)
        if 'send' in self.data and can_send(self.user, self.instance):
            letter.send(user=self.user)
        letter.save()
        return letter

    def save(self, *args, **kwargs):
        super(NewCaseForm, self).save(*args, **kwargs)
        self.letter = self.save_letter()
        return self.instance

    class Meta:
        model = Case
        fields = ['name', 'office']
        widgets = {
            'office': autocomplete.ModelSelect2(url='offices:autocomplete')
        }
