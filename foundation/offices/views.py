from __future__ import absolute_import
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.utils.translation import ugettext_lazy as _
from braces.views import (SelectRelatedMixin, LoginRequiredMixin, FormValidMessageMixin,
                          UserFormKwargsMixin)
from django.core.urlresolvers import reverse_lazy
from django_filters.views import FilterView
from atom.views import DeleteMessageMixin, FormInitialMixin
from .models import Office, Email
from .forms import OfficeForm, CreateOfficeForm, EmailForm
from .filters import OfficeFilter
from foundation.letters.models import Letter


class OfficeListView(SelectRelatedMixin, FilterView):
    filterset_class = OfficeFilter
    model = Office
    select_related = ['jst', ]
    paginate_by = 25


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


class OfficeCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = Office
    form_class = CreateOfficeForm

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class OfficeUpdateView(LoginRequiredMixin, UserFormKwargsMixin,  FormValidMessageMixin,
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


class EmailCreateView(LoginRequiredMixin, UserFormKwargsMixin, FormValidMessageMixin,
                      CreateView):
    model = Email
    form_class = EmailForm

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class EmailUpdateView(LoginRequiredMixin, FormInitialMixin, UserFormKwargsMixin,
                      FormValidMessageMixin, UpdateView):
    model = Email
    form_class = EmailForm

    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)
