from django.utils.translation import ugettext as _
from django_tables2 import tables
from django_tables2.utils import A
from .models import Contact, Letter


class ContactTable(tables.Table):
    name = tables.columns.LinkColumn('correspondence:contact_detail', args=[A('pk')])
    add = tables.columns.TemplateColumn(template_name="correspondence/_link_add_letter.html",
        verbose_name=_("Actions"))
    created_by = tables.columns.LinkColumn('users:detail', args=[A('created_by.username')])

    class Meta:
        model = Contact
        attrs = {'class': 'table table-striped'}
        exclude = ['id', 'comment', 'modified_by', 'modified_on']


class LetterTable(tables.Table):
    id = tables.columns.LinkColumn('correspondence:letter_detail', args=[A('pk')])
    contact = tables.columns.LinkColumn('correspondence:contact_detail', args=[A('contact_id')])
    created_by = tables.columns.LinkColumn('users:detail', args=[A('created_by.username')])
    modified_by = tables.columns.LinkColumn('users:detail', args=[A('created_by.username')])

    class Meta:
        model = Letter
        attrs = {'class': 'table table-striped'}
