from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('topword/', include('app_google_recommend.urls')),
]
