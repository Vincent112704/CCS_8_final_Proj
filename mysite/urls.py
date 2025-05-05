from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('AI_summarizer/', include('AI_summarizer.urls')),
    path('accounts/', include('accounts.urls')),

]
