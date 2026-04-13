# Django Modules
from django.contrib import admin
from django.urls import path, include

# Project Modules 
from .consumers import CommentConsumer


ws_urlpatterns = [
    path('ws/posts/<slug:slug>/comments/', CommentConsumer.as_asgi())
]