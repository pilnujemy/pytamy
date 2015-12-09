from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, FormView
from django.utils.translation import ugettext_lazy as _
from braces.views import (SelectRelatedMixin, LoginRequiredMixin, FormValidMessageMixin,
                          UserFormKwargsMixin)
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse_lazy
from django_filters.views import FilterView
from atom.views import DeleteMessageMixin, ActionMessageMixin, ActionView
from cached_property import cached_property
from .models import Letter
from .forms import LetterForm, NewReplyForm
from .filters import LetterFilter


class LetterListView(FilterView):
    filterset_class = LetterFilter
    model = Letter
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        qs = super(LetterListView, self).get_queryset(*args, **kwargs)
        return qs.for_list()


class LetterDetailView(DetailView):
    model = Letter

    def get_queryset(self, *args, **kwargs):
        qs = super(LetterDetailView, self).get_queryset(*args, **kwargs)
        return qs.for_detail()


class LetterCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = Letter
    form_class = LetterForm

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class LetterUpdateView(LoginRequiredMixin, UserFormKwargsMixin, FormValidMessageMixin,
                       UpdateView):
    model = Letter
    form_class = LetterForm

    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)


class ReplyView(LoginRequiredMixin, SingleObjectMixin, UserFormKwargsMixin, FormView):
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
    success_url = reverse_lazy('letters:list')

    def get_success_message(self):
        return _("{0} deleted!").format(self.object)


class LetterSendView(LoginRequiredMixin, ActionMessageMixin, ActionView):
    model = Letter
    success_message = _("Letter has been send!")
    template_name_suffix = '_send'

    def action(self):
        self.object.send(self.request.user)

    def get_success_url(self):
        return self.object.get_absolute_url()
