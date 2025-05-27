from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.posttempl, name='index'),  # TEST template for uploading PDF
    path('get2/', views.posttempl2, name='index2'),  # TEST template for ai chatbot
    path("", views.postPDF, name="Home"),
    path("chat/", views.chat, name="chat"),
]