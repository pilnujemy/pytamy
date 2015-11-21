from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, FormView
from django.utils.translation import ugettext_lazy as _
from braces.views import (SelectRelatedMixin, LoginRequiredMixin, FormValidMessageMixin,
                          UserFormKwargsMixin)
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse_lazy
from django_filters.views import FilterView
from atom.views import DeleteMessageMixin
from cached_property import cached_property
from .models import Letter
from .forms import LetterForm, NewReplyForm
from .filters import LetterFilter


class LetterListView(SelectRelatedMixin, FilterView):
    filterset_class = LetterFilter
    model = Letter
    select_related = ['case', 'sender_user', 'sender_office']
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        qs = super(LetterListView, self).get_queryset(*args, **kwargs)
        return qs


class LetterDetailView(SelectRelatedMixin, DetailView):
    model = Letter
    select_related = ['case', 'sender_user', 'sender_office']


class LetterCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = Letter
    form_class = LetterForm

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class LetterUpdateView(LoginRequiredMixin, UserFormKwargsMixin,  FormValidMessageMixin,
                       UpdateView):
    model = Letter
    form_class = LetterForm

    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)


class ReplyView(SingleObjectMixin, UserFormKwargsMixin, FormView):
    form_class = NewReplyForm
    template_name_suffix = '_reply'
    model = Letter

    @cached_property
    def object(self):
        return self.get_object()

    def get_form_kwargs(self, *args, **kwargs):
        kw = super(ReplyView, self).get_form_kwargs(*args, **kwargs)
        kw['letter'] = self.get_object()
        return kw

    def get_success_url(self, *args, **kwargs):
        return self.new_object.get_absolute_url()

    def get_template_names(self, *args, **kwargs):
        return ["%s/%s%s.html" % (
                self.object._meta.app_label,
                self.object._meta.model_name,
                self.template_name_suffix
                ),
                ]

    def form_valid(self, form):
        self.new_object = form.save()
        return super(ReplyView, self).form_valid(form)


class LetterDeleteView(LoginRequiredMixin, DeleteMessageMixin, DeleteView):
    model = Letter
    success_url = reverse_lazy('APP_NAME:list')

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)
