from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pdf_gen", views.pdf_gen, name="pdf_gen"),
]