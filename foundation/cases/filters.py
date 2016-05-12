# -*- coding: utf-8 -*-
from atom.ext.django_filters.filters import CrispyFilterMixin
from django.utils.translation import ugettext as _
import django_filters
from .models import Case


class CaseFilter(CrispyFilterMixin, django_filters.FilterSet):
    # office = AutocompleteChoiceFilter('OfficeAutocomplete', label=_("Office"))
    # office__tags = AutocompleteChoiceFilter('TagAutocomplete', label=_("Office tags"))

    def __init__(self, *args, **kwargs):
        super(CaseFilter, self).__init__(*args, **kwargs)
        self.filters['created_by'].label = _('Maintained by')
        self.filters['name'].lookup_type = 'icontains'

    class Meta:
        model = Case
        fields = ['name', 'office', 'created_by']
        order_by = ['created', ]
