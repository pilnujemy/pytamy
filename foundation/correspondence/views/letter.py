from django.views.generic import DeleteView, DetailView, UpdateView, CreateView
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from braces.views import LoginRequiredMixin, UserFormKwargsMixin, SelectRelatedMixin
from ..models import Letter, Attachment
from ..forms import LetterForm
from ..filters import LetterFilter
from ..tables import LetterTable
from .mixins import (PagedFilteredTableView, InitialFormMixin, CreateFormMessagesMixin,
    UpdateFormMessagesMixin, DeletedMessageMixin, CreateFormsetView, UpdateFormsetView)
from ..forms import AttachmentForm

from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse


class FormsetHelper(FormHelper):
    form_tag = False
    form_method = 'post'


class TableInlineHelper(FormsetHelper):
    template = 'bootstrap/table_inline_formset.html'


def formset_attachment_factory(form_formset=None, *args, **kwargs):
    if form_formset is None:
        class BaseAttachmentFormSet(BaseInlineFormSet):
            helper = TableInlineHelper()
        form_formset = BaseAttachmentFormSet
    return inlineformset_factory(Letter, Attachment, form=AttachmentForm, formset=form_formset,
        *args, **kwargs)

AttachmentFormSet = formset_attachment_factory()


class LetterDetailView(SelectRelatedMixin, DetailView):
    model = Letter
    select_related = ["created_by", "modified_by", "contact"]


class LetterListView(SelectRelatedMixin, PagedFilteredTableView):
    model = Letter
    table_class = LetterTable
    filter_class = LetterFilter
    select_related = ["created_by", "modified_by", "contact", ]


class LetterCreateView(LoginRequiredMixin, CreateFormMessagesMixin, UserFormKwargsMixin,
        InitialFormMixin, CreateFormsetView, CreateView):
    model = Letter
    form_class = LetterForm
    formset_class = {'attachment_form': AttachmentFormSet}


class LetterDeleteView(DeletedMessageMixin, DeleteView):
    model = Letter

    def get_success_message(self):
        return self.object

    def get_success_url(self):
        return reverse('correspondence:contact_list')


class LetterUpdateView(LoginRequiredMixin, UpdateFormMessagesMixin, UserFormKwargsMixin,
        UpdateFormsetView, UpdateView):
    model = Letter
    form_class = LetterForm
    formset_class = {'attachment_form': AttachmentFormSet}
