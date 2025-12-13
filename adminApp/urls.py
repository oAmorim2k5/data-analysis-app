from django.urls import path
from . import views

urlpatterns = [
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_home/clients/', views.client_management, name='clients_management')
]