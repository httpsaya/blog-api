# Django Modules
from django.urls import path, include

# Rest Framework
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

# Project Modules
from apps.users.views import UserViewSet


router: DefaultRouter = DefaultRouter(
)

router.register(
    prefix="auth",
    viewset=UserViewSet,
    basename='auth',
)

urlpatterns = [
    path('', include(router.urls)),

   #Tokens
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]