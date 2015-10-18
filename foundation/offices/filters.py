# -*- coding: utf-8 -*-
from __future__ import absolute_import
from atom.ext.django_filters.filters import CrispyFilterMixin
import django_filters
from .models import Office


class OfficeFilter(CrispyFilterMixin, django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_type='icontains')
    # institution = AutocompleteChoiceFilter('InstitutionAutocomplete')

    def __init__(self, *args, **kwargs):
        super(OfficeFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Office
        # fields = ['name', 'monitoring', 'institution']
        # order_by = ['-letter_count', 'created', ]
