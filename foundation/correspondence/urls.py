# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.LetterListView.as_view(), name="letter_list"),
    url(r'^~create$', views.LetterCreateView.as_view(), name="letter_create"),
    url(r'^(?P<pk>\d+)$', views.LetterDetailView.as_view(), name="letter_detail"),
    url(r'^(?P<pk>\d+)/update$', views.LetterUpdateView.as_view(), name="letter_update"),
    url(r'^(?P<pk>\d+)/delete$', views.LetterDeleteView.as_view(), name="letter_delete"),
    url(r'^contact/$', views.ContactListView.as_view(), name="contact_list"),
    url(r'^contact/~create$', views.ContactCreateView.as_view(), name="contact_create"),
    url(r'^contact/(?P<pk>\d+)$', views.ContactDetailView.as_view(), name="contact_detail"),
    url(r'^contact/(?P<pk>\d+)/update$', views.ContactUpdateView.as_view(), name="contact_update"),
    url(r'^contact/(?P<pk>\d+)/delete$', views.ContactDeleteView.as_view(),
        name="contact_delete"),
]
