from __future__ import absolute_import
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.utils.translation import ugettext_lazy as _
from braces.views import (SelectRelatedMixin, LoginRequiredMixin, FormValidMessageMixin,
                          UserFormKwargsMixin)
from django.core.urlresolvers import reverse_lazy
from django_filters.views import FilterView
from atom.views import DeleteMessageMixin, FormInitialMixin
from .models import Office, Email
from .forms import OfficeForm, EmailForm
from foundation.letters.models import Letter
from .filters import OfficeFilter
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory
from functools import wraps
from django.utils.functional import curry
from atom.ext.crispy_forms.forms import BaseTableFormSet
from django.contrib import messages


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


class FormSetMixin(object):
    inline_model = None
    inline_form_cls = None
    formset_cls = BaseTableFormSet
    formsets = {'name': {'model': None,
                         'form': None,
                         'kw_callback': lambda self: {}}
                }

    def get_form(self, form_class, *args, **kwargs):
        form = super(FormSetMixin, self).get_form(form_class, *args, **kwargs)
        if hasattr(form, 'helper'):
            form.helper.form_tag = False
        return form

    def get_formset(self, formset):
        constructed = inlineformset_factory(parent_model=self.model,
                                            model=formset['model'],
                                            form=formset['form'],
                                            formset=self.formset_cls)
        kwargs = formset.get('kw_callback', lambda x: {})(self)
        constructed.form = staticmethod(curry(formset['form'], **kwargs))
        return constructed

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.object if hasattr(self, 'object') else self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formsets = {k: self.get_formset(v)() for k, v in self.formsets.items()}
        return self.render_to_response(
            self.get_context_data(form=form,
                                  formsets=formsets))

    def post(self, request, *args, **kwargs):
        self.object = self.object if hasattr(self, 'object') else self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = form.save(commit=False)
            formsets = {}
            for k, v in self.formsets.items():
                formsets[k] = self.get_formset(v)(self.request.POST or None,
                                                  self.request.FILES,
                                                  instance=self.object)
            if all(x.is_valid() for x in formsets.values()):
                return self.form_valid(form, formsets)
            return self.form_invalid(form, formsets)
        formsets = {k: self.get_formset(v)(self.request.POST or None, self.request.FILES)
                    for k, v in self.formsets.items()}
        return self.form_invalid(form, formsets)

    def form_valid(self, form, formsets):
        self.object.save()
        [x.save() for x in formsets.values()]
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formsets):
        return self.render_to_response(
            self.get_context_data(form=form, formsets=formsets))


class OfficeCreateView(LoginRequiredMixin, FormSetMixin, UserFormKwargsMixin, CreateView):
    object = None
    model = Office
    form_class = OfficeForm
    formsets = {'email': {'model': Email,
                          'form': EmailForm,
                          'kw_callback': lambda x: {'user': x.request.user}}
                }


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
