# firebase_auth_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('accounts/', include('allauth.urls')),  # Include allauth URLs

]
