# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.views import defaults
urlpatterns = [
    url(r'^', include('foundation.main.urls')),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('foundation.press.urls', namespace="press")),
    # User management
    url(r'^users/', include("foundation.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),
    # Your stuff: custom urls includes go here
    url(r'^correspondence/', include("foundation.correspondence.urls", namespace="correspondence")),
    url(r'^kraj/', include("foundation.teryt.urls", namespace="teryt")),
    url(r'^urzedy/', include("foundation.offices.urls", namespace="offices")),
    url(r'^sprawy/', include("foundation.cases.urls", namespace="cases")),
    url(r'^listy/', include("foundation.letters.urls", namespace="letters")),
    url(r'^strony/(?P<url>.*/)$', views.flatpage),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', defaults.bad_request),
        url(r'^403/$', defaults.permission_denied),
        url(r'^404/$', defaults.page_not_found),
        url(r'^500/$', defaults.server_error),
    ]
