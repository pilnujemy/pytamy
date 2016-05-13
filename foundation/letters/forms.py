# -*- coding: utf-8 -*-
from django import forms
from .models import OutgoingLetter
from crispy_forms.layout import Div, Fieldset, Layout, Submit
from django.utils.translation import ugettext_lazy as _
from braces.forms import UserKwargModelFormMixin
from atom.ext.crispy_forms.forms import HelperMixin, SingleButtonMixin
from foundation.offices.emails.fields import EmailAutocompleteField
from ckeditor.widgets import CKEditorWidget
# from autocomplete_light import shortcuts as autocomplete_light
from .utils import can_send
from dal import autocomplete


class LetterForm(UserKwargModelFormMixin, SingleButtonMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LetterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = OutgoingLetter
        fields = ['subject', 'content', 'email']


class NewReplyForm(HelperMixin, UserKwargModelFormMixin, forms.ModelForm):
    email2 = EmailAutocompleteField()

    def __init__(self, letter, *args, **kwargs):
        super(NewReplyForm, self).__init__(*args, **kwargs)
        self.instance.case = letter.case
        self.instance.author = self.user
        self.fields['subject'].initial = letter.case.name
        self.helper.layout = Layout(
            Fieldset(
                _('Recipient'),
                Div(
                    Div('office', css_class='col-sm-6'),
                    Div('email2', css_class='col-sm-6'),
                    css_class='row'
                ),
            ),
            Fieldset(
                _('Content'),
                'subject',
                'content',
            ),
        )
        if hasattr(letter, 'outgoingletter'):
            self.fields['office'].initial = letter.outgoingletter.office
        self.helper.add_input(Submit('save', _('Save '), css_class="btn-primary"))
        if can_send(self.user, letter.case):
            self.helper.add_input(Submit('send', _('Save & send'), css_class="btn-primary"))

    def save(self, *args, **kwargs):
        self.instance.email = self.cleaned_data['email2'].email
        super(NewReplyForm, self).save(*args, **kwargs)
        if 'send' in self.data and can_send(self.user, self.instance.case):
            self.instance.send(user=self.user)
        return self.instance

    class Meta:
        model = OutgoingLetter
        fields = ['office', 'content', 'subject']
        widgets = {
            'content': CKEditorWidget(),
            'office': autocomplete.ModelSelect2(url='offices:autocomplete')
        }
