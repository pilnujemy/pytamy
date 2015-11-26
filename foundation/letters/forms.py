# -*- coding: utf-8 -*-
from django import forms
from .models import Letter
from django.utils.translation import ugettext_lazy as _
from braces.forms import UserKwargModelFormMixin
from atom.ext.crispy_forms.forms import HelperMixin, SingleButtonMixin
from crispy_forms.layout import Submit
from ckeditor.widgets import CKEditorWidget
from .utils import can_send


class LetterForm(UserKwargModelFormMixin, SingleButtonMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LetterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Letter
        fields = ['subject', 'content', 'email']


class NewReplyForm(HelperMixin, UserKwargModelFormMixin, forms.ModelForm):
    def __init__(self, letter, *args, **kwargs):
        super(NewReplyForm, self).__init__(*args, **kwargs)
        self.instance.case = letter.case
        self.instance.author = self.user
        self.fields['content'].widget = CKEditorWidget()
        self.fields['subject'].initial = letter.case.name
        self.fields['email'].limit_choices_to = {'office': letter.case.office}
        self.fields['email'].reqiured = True
        self.fields['email'].initial = letter.email
        self.helper.add_input(Submit('save', _('Save '), css_class="btn-primary"))
        if can_send(self.user, letter.case):
            self.helper.add_input(Submit('send', _('Save & send'), css_class="btn-primary"))

    def save(self, *args, **kwargs):
        super(NewReplyForm, self).save(*args, **kwargs)
        if 'send' in self.data and can_send(self.user, self.instance.case):
            self.instance.send(user=self.user)
        return self.instance

    class Meta:
        model = Letter
        fields = ['subject', 'content', 'email']
