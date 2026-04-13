# Django Modules
from django.urls import path, include

# Project Modules
from .views import (
    get_page, 
    sse_notifications, 
    NotificationViewSet)

# DRF Modules
from rest_framework.routers import DefaultRouter


router: DefaultRouter = DefaultRouter()

router.register(
    prefix='notifications',
    viewset=NotificationViewSet,
    basename='notifications'
    )

urlpatterns = [
    path('posts/<slug:slug>/comments/', get_page, name='post_comments'),

    path('posts/stream/', sse_notifications),

    path('', include(router.urls)),
]