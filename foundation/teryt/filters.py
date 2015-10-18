# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from atom.ext.django_filters.filters import CrispyFilterMixin
import django_filters
from .models import JST


class JSTFilter(CrispyFilterMixin, django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(JSTFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = JST
