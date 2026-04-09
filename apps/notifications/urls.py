# apps/blog/urls.py (или твое приложение)
from django.urls import path
from .views import get_page

urlpatterns = [
    # Важно: убедись, что этот urls.py включен в основной urls.py проекта через include()
    path('posts/<slug:slug>/comments/', get_page, name='post_comments'),
]