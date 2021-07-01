from django.contrib import admin
from django.urls import path, include
from .views import MainView, PasswordResetRequestView

app_name = 'home'
urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path("password_reset", PasswordResetRequestView.as_view(), name="password_reset")
]
