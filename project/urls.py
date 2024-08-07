from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("accounts/", include("allauth.urls")),
    path("", include("django_finance.tracker.urls")),
    path("admin/", admin.site.urls),
]
