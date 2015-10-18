# -*- coding: utf-8 -*-
from django import forms
from .models import Office
from braces.forms import UserKwargModelFormMixin


class OfficeForm(UserKwargModelFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OfficeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Office
        fields = ['name', ]
