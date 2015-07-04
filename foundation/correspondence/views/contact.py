from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from braces.views import LoginRequiredMixin, UserFormKwargsMixin, SelectRelatedMixin
from ..models import Contact
from ..forms import ContactForm
from ..filters import ContactFilter
from ..tables import ContactTable
from .mixins import (PagedFilteredTableView, InitialFormMixin, CreateFormMessagesMixin,
    UpdateFormMessagesMixin, DeletedMessageMixin)
from django.core.urlresolvers import reverse


class ContactDetailView(DetailView):
    model = Contact


class ContactListView(SelectRelatedMixin, PagedFilteredTableView):
    model = Contact
    table_class = ContactTable
    filter_class = ContactFilter
    select_related = ["created_by", "modified_by"]


class ContactCreateView(LoginRequiredMixin, CreateFormMessagesMixin, UserFormKwargsMixin,
        InitialFormMixin, CreateView):
    model = Contact
    form_class = ContactForm


class ContactDeleteView(DeletedMessageMixin, DeleteView):
    model = Contact

    def get_success_message(self):
        return self.object

    def get_success_url(self):
        return reverse('correspondence:contact_list')


class ContactUpdateView(LoginRequiredMixin, UpdateFormMessagesMixin, UserFormKwargsMixin,
        UpdateView):
    model = Contact
    form_class = ContactForm
