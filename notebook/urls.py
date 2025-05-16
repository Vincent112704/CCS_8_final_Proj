from django.urls import path
from . import views

urlpatterns = [
    path("post/", views.saveNotebook, name="Home"), 
    path("get/", views.getNotebook, name="getNotebook"),
    path("delete/", views.deleteNotebook, name="deleteNotebook"),
    path("getNB/", views.getOneNB, name="getNotebookByID"),
]