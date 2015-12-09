# -*- coding: utf-8 -*-
from atom.filters import CrispyFilterMixin
import django_filters
from .models import Case
from taggit.models import Tag


class CaseFilter(CrispyFilterMixin, django_filters.FilterSet):
    office__tags = django_filters.ModelChoiceFilter(queryset=Tag.objects.all())

    def __init__(self, *args, **kwargs):
        super(CaseFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Case
        fields = ['name', 'office', 'created_by']
        order_by = ['created', ]
