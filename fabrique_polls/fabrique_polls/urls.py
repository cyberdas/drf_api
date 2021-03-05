from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


urlpatterns = [
    path("api/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls"))  # регистрация не нужна
]
