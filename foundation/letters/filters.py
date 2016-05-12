# -*- coding: utf-8 -*-
from atom.ext.django_filters.filters import CrispyFilterMixin
from django.utils.translation import ugettext as _
import django_filters
from .models import Letter


class LetterFilter(CrispyFilterMixin, django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(LetterFilter, self).__init__(*args, **kwargs)
        self.filters['case__created_by'].label = _('Case maintained by')

    class Meta:
        model = Letter
        fields = ['case__created_by', ]
