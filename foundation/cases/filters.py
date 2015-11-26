# -*- coding: utf-8 -*-
from atom.filters import CrispyFilterMixin
import django_filters
from .models import Case


class CaseFilter(CrispyFilterMixin, django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(CaseFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Case
        fields = ['name', 'office', 'created_by']
        order_by = ['created', ]
