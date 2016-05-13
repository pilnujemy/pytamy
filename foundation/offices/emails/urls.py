# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^~create$', views.EmailCreateView.as_view(),
        name="create"),
    url(r'^(?P<pk>[\w-]+)$', views.EmailUpdateView.as_view(),
        name="update"),
    url(r'^~create$', views.EmailAutocomplete.as_view(),
        name="autocomplete"),
]
