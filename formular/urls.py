from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("send_form", views.send_form, name="send_form")
]