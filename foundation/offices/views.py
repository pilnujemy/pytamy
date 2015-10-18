from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.utils.translation import ugettext_lazy as _
from braces.views import (SelectRelatedMixin, LoginRequiredMixin, FormValidMessageMixin,
                          UserFormKwargsMixin)
from django.core.urlresolvers import reverse_lazy
from django_filters.views import FilterView
from atom.views import DeleteMessageMixin
from .models import Office
from .forms import OfficeForm
from .forms import OfficeFilter


class OfficeListView(SelectRelatedMixin, FilterView):
    filterset_class = OfficeFilter
    model = Office
    # select_related = ['',]
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        qs = super(OfficeListView, self).get_queryset(*args, **kwargs)
        return qs


class OfficeDetailView(SelectRelatedMixin, DetailView):
    model = Office
    # select_related = ['', ]


class OfficeCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = Office
    form_class = OfficeForm

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
    success_url = reverse_lazy('APP_NAME:list')

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)
