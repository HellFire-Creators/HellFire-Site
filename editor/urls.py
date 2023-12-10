from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:path>", views.show_path, name="show_path")
]
