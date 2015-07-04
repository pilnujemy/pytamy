import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
import autocomplete_light
from .models import Letter, Contact


class ContactFilter(django_filters.FilterSet):
    created_on = django_filters.DateRangeFilter()

    @property
    def form(self):
        self._form = super(ContactFilter, self).form
        self._form.helper = FormHelper()
        self._form.helper.form_class = 'form-inline'
        self._form.helper.form_method = 'get'
        self._form.helper.layout = Layout(
            'postcode',
            'city',
            'created_by',
            'created_on',
            Submit('save', 'save')
        )
        return self._form

    class Meta:
        model = Contact
        fields = ['postcode', 'city', 'created_by', 'created_on']


class LetterFilter(django_filters.FilterSet):
    created_on = django_filters.DateRangeFilter()
    contact = django_filters.ModelChoiceFilter(
        queryset=Contact.objects.all(),
        widget=autocomplete_light.ChoiceWidget('ContactAutocomplete')
        )

    @property
    def form(self):
        self._form = super(LetterFilter, self).form
        self._form.helper = FormHelper()
        self._form.helper.form_class = 'form-inline'
        self._form.helper.form_method = 'get'
        self._form.helper.layout = Layout(
            'outgoing',
            'contact',
            'created_on',
            Submit('save', 'save')
        )
        return self._form

    class Meta:
        model = Letter
        fields = ['outgoing', 'created_on', 'contact', ]
