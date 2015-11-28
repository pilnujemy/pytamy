from django.views.generic import DetailView
from braces.views import SelectRelatedMixin
from django_filters.views import FilterView
from .models import JST
from .filters import JSTFilter
from foundation.offices.models import Office


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

    def get_context_data(self, **kwargs):
        context = super(JSTDetailView, self).get_context_data(**kwargs)
        context['office_list'] = (Office.objects.for_user(self.request.user).for_list().
                                  area(self.object).all())
        return context
