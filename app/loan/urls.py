"""
URL Configuration for customer app
"""
from django.urls import path
from . import views


urlpatterns = [
    path('check-eligibility/', views.CustomerEligibleView.as_view(),
         name='customer-eligibility'),
    path('create-loan/', views.LoanCreateView.as_view(), name='create-loan'),
    path('view-loan/<int:loan_id>/',
         views.LoanDetailView.as_view(), name='loan-detail'),
    path('view-loans/<int:customer_id>/', views.CustomerLoanDetailView.as_view(), name='loan-detail-customer'),

]
