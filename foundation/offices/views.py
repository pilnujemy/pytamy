from __future__ import absolute_import

from atom.views import DeleteMessageMixin
from atom.ext.crispy_forms.forms import BaseTableFormSet
from braces.views import FormValidMessageMixin, LoginRequiredMixin, SelectRelatedMixin, UserFormKwargsMixin
from dal import autocomplete
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DeleteView, DetailView, UpdateView
from django_filters.views import FilterView
from extra_views import CreateWithInlinesView, InlineFormSet, NamedFormsetsMixin

from foundation.letters.models import Letter
from foundation.offices.emails.models import Email
from foundation.offices.emails.forms import EmailForm

from .filters import OfficeFilter
from .forms import OfficeForm
from .models import Office


class OfficeListView(SelectRelatedMixin, FilterView):
    filterset_class = OfficeFilter
    model = Office
    select_related = ['jst', ]
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        qs = super(OfficeListView, self).get_queryset(*args, **kwargs)
        return qs.with_case_count()


class OfficeDetailView(SelectRelatedMixin, DetailView):
    model = Office
    select_related = ['jst', ]

    def get_context_data(self, **kwargs):
        context = super(OfficeDetailView, self).get_context_data(**kwargs)
        context['inbox'] = (Letter.objects.filter(case__office=self.object).
                            for_milestone().
                            order_by('-created').all()[:20])
        context['email_set'] = Email.objects.filter(office=self.object).all()
        return context


class EmailInline(InlineFormSet):
    model = Email
    form_class = EmailForm
    formset_class = BaseTableFormSet
    fields = ['email', 'default']

    def get_extra_form_kwargs(self):
        return {'user': self.request.user}


class OfficeCreateView(LoginRequiredMixin, NamedFormsetsMixin, UserFormKwargsMixin,
                       CreateWithInlinesView):
    model = Office
    form_class = OfficeForm
    inlines = [EmailInline]
    inlines_names = ['emails']


class OfficeUpdateView(LoginRequiredMixin, UserFormKwargsMixin, FormValidMessageMixin,
                       UpdateView):
    model = Office
    form_class = OfficeForm

    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)


class OfficeDeleteView(LoginRequiredMixin, DeleteMessageMixin, DeleteView):
    model = Office
    success_url = reverse_lazy('offices:list')

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)


class OfficeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Office.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
