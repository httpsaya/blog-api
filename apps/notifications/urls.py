# Django Modules
from django.urls import path

# Project Modules
from .views import get_page, sse_notifications

urlpatterns = [
    path('posts/<slug:slug>/comments/', get_page, name='post_comments'),

    path('posts/stream/', sse_notifications)
]