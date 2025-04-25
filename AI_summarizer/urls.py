from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Home"),
    path("chat", views.chat, name="chat"),
]