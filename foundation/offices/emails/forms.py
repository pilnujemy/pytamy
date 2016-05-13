# -*- coding: utf-8 -*-
from django import forms
from .models import Email
from braces.forms import UserKwargModelFormMixin
from atom.ext.crispy_forms.forms import SingleButtonMixin
# from autocomplete_light.contrib.taggit_field import TaggitField, TaggitWidget
# from autocomplete_light import shortcuts as autocomplete_light


class EmailForm(UserKwargModelFormMixin, SingleButtonMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.helper.form_tag = False
        if not self.instance.pk:
            self.instance.created_by = self.user
        if not self.user.has_perm('offices.change_email'):
            del self.fields['default']
        self.fields['default'].help_text = None

    class Meta:
        model = Email
        fields = ['email', 'default']
