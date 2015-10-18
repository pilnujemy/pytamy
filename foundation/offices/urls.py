# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'^$', views.OfficeListView.as_view(), name="list"),
   url(r'^~create$', views.OfficeCreateView.as_view(), name="create"),
   url(r'^urzad-(?P<slug>[\w-]+)$', views.OfficeDetailView.as_view(), name="detail"),
   url(r'^urzad-(?P<slug>[\w-]+)/~update$', views.OfficeUpdateView.as_view(),
       name="update"),
   url(r'^urzad-(?P<slug>[\w-]+)/~delete$', views.OfficeDeleteView.as_view(),
       name="delete"),
]
