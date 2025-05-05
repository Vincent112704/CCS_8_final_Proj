from django.urls import path
from . import views


urlpatterns = [
    # path('LoginInTemp/', views.loginTemplate, name='log'), #TEST template login account
    # path('signInTemp/', views.signupTemplate, name='sign'),#TEST template signup account
    # path('deleteTemp/', views.deleTemplate, name='dele'),#TEST template delete account
    path('manage/', views.manageAccount, name='manage'),
    path('delete/', views.deleteAccount, name='delete'), 
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]