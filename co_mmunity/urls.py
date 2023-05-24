from django.contrib import admin
from django.urls import path, include
from article import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include('users.urls')),
    path("articles/", include('article.urls')),
    path("", views.main_page, name="main_page")
]
