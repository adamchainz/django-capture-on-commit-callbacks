from django.urls import path

from tests import views

urlpatterns = [
    path("contact/", views.contact),
]
