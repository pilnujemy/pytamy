from django_filters import FilterSet, DateRangeFilter
from .models import Letter, Contact
from atom.ext.django_filters.filters import CrispyFilterMixin


class ContactFilter(CrispyFilterMixin, FilterSet):
    created_on = DateRangeFilter()

    class Meta:
        model = Contact
        fields = ['postcode', 'city', 'created_by', 'created_on']


class LetterFilter(CrispyFilterMixin, FilterSet):
    created_on = DateRangeFilter()
    # TODO: contact = AutocompleteChoiceFilter('ContactAutocomplete')

    class Meta:
        model = Letter
        fields = ['outgoing', 'created_on', 'contact', ]
