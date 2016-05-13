# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.JSTListView.as_view(), name="list"),
    url(r'^voivodeship-autocomplete/$',
        views.VoivodeshipAutocomplete.as_view(),
        name='voivodeship-autocomplete',),
    url(r'^county-autocomplete/$',
        views.CountyAutocomplete.as_view(),
        name='county-autocomplete',),
    url(r'^community-autocomplete/$',
        views.CommunityAutocomplete.as_view(),
        name='community-autocomplete',),
    url(r'^region-(?P<slug>[\w-]+)$', views.JSTDetailView.as_view(), name="details"),
    url(r'^gmina-(?P<slug>[\w-]+)$', views.JSTDetailView.as_view(), name="details_g"),
    url(r'^powiat-(?P<slug>[\w-]+)$', views.JSTDetailView.as_view(), name="details_p"),
    url(r'^wojewodztwo-(?P<slug>[\w-]+)$', views.JSTDetailView.as_view(), name="details_w"),
]
