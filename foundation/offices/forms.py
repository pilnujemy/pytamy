# -*- coding: utf-8 -*-
from django import forms
from .models import Office
from braces.forms import UserKwargModelFormMixin
from django.utils.translation import ugettext_lazy as _
from atom.ext.crispy_forms.forms import SingleButtonMixin
from crispy_forms.layout import Layout, Fieldset, Div
from dal import autocomplete
from foundation.teryt.models import JST


class OfficeForm(SingleButtonMixin, UserKwargModelFormMixin, forms.ModelForm):
    voivodeship = forms.ModelChoiceField(
        label=_("Voivodeship"),
        required=False,
        queryset=JST.objects.voivodeship().all(),
        widget=autocomplete.ModelSelect2(url='teryt:voivodeship-autocomplete')
    )
    county = forms.ModelChoiceField(
        label=_("County"),
        required=False,
        queryset=JST.objects.county().all(),
        widget=autocomplete.ModelSelect2(url='teryt:county-autocomplete',
                                         forward=['voivodeship'])
    )

    def __init__(self, *args, **kwargs):
        super(OfficeForm, self).__init__(*args, **kwargs)
        self.helper.form_tag = False
        self.instance.created_by = self.user
        self.fields['jst'].label = _('Community')
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
                Div(
                    Div('voivodeship', css_class='col-sm-4'),
                    Div('county', css_class='col-sm-4'),
                    Div('jst', css_class='col-sm-4'),
                    css_class='row'
                ),
            ),
            Fieldset(
                _('Other'),
                'tags',
            ),
        )

    class Meta:
        model = Office
        fields = ['name', 'jst', 'krs', 'regon', 'tags', 'postcode']
        widgets = {
            'jst': autocomplete.ModelSelect2(url='teryt:community-autocomplete',
                                             forward=['county']),
        }
