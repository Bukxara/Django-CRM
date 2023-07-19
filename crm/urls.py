from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customers/', views.customers_page, name='customers'),
    path("orders-by-customer/<str:telegram_id>/", views.customer_orders, name="customer_orders"),
    path('transactions/', views.transactions, name='transactions'),
    path('dashboard/<int:pk>/', views.change_status, name='change_status'),
    path('logout/', views.logout_user, name='logout'),
]
