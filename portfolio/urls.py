from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Define the index URL pattern
    path('home/', views.home_view, name='home'),  # Define the home URL pattern
    path('contact/', views.contact_view, name='contact'),
    path('chatbot-stream/', views.chatbot_stream, name='chatbot_stream'),
    path('chat/', views.chat_view, name='chat'),


]