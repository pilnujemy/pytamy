from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from braces.views import FormMessagesMixin
from django.utils.translation import ugettext as _
from django_tables2 import SingleTableView, RequestConfig


class CreateFormMessagesMixin(FormMessagesMixin):
    def get_form_invalid_message(self):
        return _(u"Something went wrong, %s was not saved") % (self.model._meta.verbose_name)

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)


class UpdateFormMessagesMixin(FormMessagesMixin):
    def get_form_invalid_message(self):
        return _(u"Something went wrong, %s was not updated") % (self.model._meta.verbose_name)

    def get_form_valid_message(self):
        return _("{0} updated!").format(self.object)


class DeletedMessageMixin(object):
    success_message = None

    def get_success_message(self):
        if self.success_message:
            return self.message.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No message to add. Provide a success_message.")

    def delete(self, *args, **kwargs):
        r = super(DeletedMessageMixin, self).delete(*args, **kwargs)
        messages.add_message(self.request, messages.SUCCESS, self.get_success_message())
        return r


class PagedFilteredTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_table(self, **kwargs):
        table = super(PagedFilteredTableView, self).get_table()
        RequestConfig(self.request, paginate={'page': self.kwargs.get('page', 1),
                            "per_page": self.paginate_by}).configure(table)
        return table

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context


class InitialFormMixin(object):
    def get_initial(self, *args, **kwargs):
        initial = super(InitialFormMixin, self).get_initial(*args, **kwargs)
        initial.update(self.request.GET.dict())
        return initial
