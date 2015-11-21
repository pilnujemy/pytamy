# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from atom.filters import CrispyFilterMixin
import django_filters
from .models import Letter


class LetterFilter(CrispyFilterMixin, django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(LetterFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Letter
