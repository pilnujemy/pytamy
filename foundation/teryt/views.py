from django.views.generic import DetailView
from braces.views import SelectRelatedMixin
from django_filters.views import FilterView
from .models import JST
from .filters import JSTFilter


class JSTListView(SelectRelatedMixin, FilterView):
    filterset_class = JSTFilter
    model = JST
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        qs = super(JSTListView, self).get_queryset(*args, **kwargs)
        return qs


class JSTDetailView(SelectRelatedMixin, DetailView):
    model = JST
    select_related = ['parent', ]
