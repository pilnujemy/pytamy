# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.LetterListView.as_view(),
        name="list"),
    url(r'^~create$', views.LetterCreateView.as_view(),
        name="create"),
    url(r'^list-(?P<slug>[\w-]+)$', views.LetterDetailView.as_view(),
        name="details"),
    url(r'^list-(?P<slug>[\w-]+)/~update$', views.LetterUpdateView.as_view(),
        name="update"),
    url(r'^list-(?P<slug>[\w-]+)/~delete$', views.LetterDeleteView.as_view(),
        name="delete"),
    url(r'^list-(?P<slug>[\w-]+)/~reply$', views.ReplyView.as_view(),
        name="reply"),
    url(r'^list-(?P<slug>[\w-]+)/~send$', views.LetterSendView.as_view(),
        name="send"),

]
