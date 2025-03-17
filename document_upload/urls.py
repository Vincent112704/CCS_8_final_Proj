from django.urls import path
from . import views

urlpatterns = [
    path("", views.hello, name="Home"),
    path("upload/", views.upload, name="Upload"),
]