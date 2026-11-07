"""Корневая маршрутизация Django-проекта."""

from django.contrib import admin

from django.conf import settings

from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("plays/", include("plays.urls")),
    path("bookings/", include("bookings.urls")),
]

handler404 = "homepage.views.page_not_found"

# Подключаем маршруты Debug Toolbar только в режиме отладки.
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
