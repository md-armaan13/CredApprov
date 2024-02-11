"""
URL Configuration for customer app
"""
from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.CustomerView.as_view(), name='customer-register'),
    
]