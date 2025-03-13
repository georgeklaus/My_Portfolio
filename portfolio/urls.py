from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Define the index URL pattern
    path('home/', views.home_view, name='home'),  # Define the home URL pattern
    path('contact/', views.contact_view, name='contact'),
]