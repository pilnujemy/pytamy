# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
               url(r'^$', views.PostArchiveIndexView.as_view(),
                   name="archive"),
               url(r'^post-(?P<slug>[-\w]+)$',
                   views.PostDetailView.as_view(), name="details"),
               url(r'^tag-(?P<slug>[-\w]+)$', views.PostTagIndexView.as_view(),
                   name="archive"),
               url(r'^(?P<year>\d{4})/$', views.PostYearArchiveView.as_view(),
                   name="archive"),
               url(r'^(?P<year>\d{4})/(?P<month>\d+)/$',
                   views.PostMonthArchiveView.as_view(),
                   name="archive"),
               url(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/$',
                   views.PostDayArchiveView.as_view(),
                   name="archive"),
]
