from django.views.generic import DeleteView, DetailView
from braces.views import LoginRequiredMixin, UserFormKwargsMixin, SelectRelatedMixin
from ..models import Letter, Attachment
from ..forms import LetterForm
from ..filters import LetterFilter
from ..tables import LetterTable
from .mixins import (PagedFilteredTableView, InitialFormMixin, CreateFormMessagesMixin,
    UpdateFormMessagesMixin, DeletedMessageMixin)

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from django.core.urlresolvers import reverse


class ItemInline(InlineFormSet):
    model = Attachment


class LetterDetailView(SelectRelatedMixin, DetailView):
    model = Letter
    select_related = ["created_by", "modified_by", "contact"]


class LetterListView(SelectRelatedMixin, PagedFilteredTableView):
    model = Letter
    table_class = LetterTable
    filter_class = LetterFilter
    select_related = ["created_by", "modified_by", "contact", ]


class LetterCreateView(LoginRequiredMixin, CreateFormMessagesMixin, UserFormKwargsMixin,
        InitialFormMixin, CreateWithInlinesView):
    model = Letter
    form_class = LetterForm
    inlines = [ItemInline]


class LetterDeleteView(DeletedMessageMixin, DeleteView):
    model = Letter

    def get_success_message(self):
        return self.object

    def get_success_url(self):
        return reverse('correspondence:contact_list')


class LetterUpdateView(LoginRequiredMixin, UpdateFormMessagesMixin, UserFormKwargsMixin,
        UpdateWithInlinesView):
    model = Letter
    form_class = LetterForm
    inlines = [ItemInline]
