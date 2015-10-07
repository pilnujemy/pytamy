from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from braces.views import LoginRequiredMixin, UserFormKwargsMixin, SelectRelatedMixin
from ..models import Contact
from ..forms import ContactForm
from ..filters import ContactFilter
from .mixins import (InitialFormMixin,
                     CreateFormMessagesMixin,
                     UpdateFormMessagesMixin,
                     DeletedMessageMixin)
from django.core.urlresolvers import reverse
from django_filters.views import FilterView


class ContactDetailView(DetailView):
    model = Contact


class ContactListView(SelectRelatedMixin, FilterView):
    model = Contact
    filterset_class = ContactFilter
    select_related = ["created_by", "modified_by"]


class ContactCreateView(LoginRequiredMixin, CreateFormMessagesMixin,
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
