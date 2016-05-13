from __future__ import absolute_import

from atom.views import FormInitialMixin
from braces.views import FormValidMessageMixin, LoginRequiredMixin, UserFormKwargsMixin
from dal import autocomplete
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView
from .forms import EmailForm
from .models import Email


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


class EmailAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Email.objects.all()
        if self.q:
            qs = qs.filter(email__icontains=self.q)
        return qs
