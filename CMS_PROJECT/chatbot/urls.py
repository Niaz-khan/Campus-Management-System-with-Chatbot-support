from django.urls import path
from .views import chatbot_view

urlpatterns = [
    path('chat/', chatbot_view, name='chatbot_chat')
]
# This code defines the URL patterns for the chatbot application. It includes a single path that maps to the `chatbot_view` function, which handles the chatbot interaction. The URL pattern is named 'chatbot_chat' for easy reference in templates and views.
# The `urlpatterns` list is used by Django to route incoming requests to the appropriate view based on the URL.