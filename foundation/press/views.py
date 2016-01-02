from braces.views import SelectRelatedMixin
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import DayArchiveView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import Post, Tag


class PostArchiveMixin(SelectRelatedMixin):
    model = Post
    date_field = "published"
    select_related = ['user', ]
    make_object_list = True
    month_format = '%m'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(PostArchiveMixin, self).get_context_data(**kwargs)
        context['month_list'] = self.model.objects.datetimes('published', 'month')
        return context


class PostArchiveIndexView(PostArchiveMixin, ArchiveIndexView):
    pass


class PostTagIndexView(PostArchiveMixin, ArchiveIndexView):
    template_name_suffix = '_archive_tag'

    def get_queryset(self, *args, **kwargs):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        qs = super(PostTagIndexView, self).get_queryset(*args, **kwargs)
        return qs.filter(tags=self.tag)

    def get_context_data(self, *args, **kwargs):
        context = super(PostTagIndexView, self).get_context_data(*args, **kwargs)
        context['tag'] = self.tag
        return context


class PostYearArchiveView(PostArchiveMixin, YearArchiveView):
    pass


class PostMonthArchiveView(PostArchiveMixin, MonthArchiveView):
    pass


class PostDayArchiveView(PostArchiveMixin, DayArchiveView):
    pass


class PostDetailView(PostArchiveMixin, DetailView):
    def get_queryset(self, *args, **kwargs):
        qs = super(PostDetailView, self).get_queryset(*args, **kwargs)
        return qs.published()
