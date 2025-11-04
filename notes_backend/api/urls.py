from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    health,
    RegisterView,
    LoginView,
    LogoutView,
    NoteViewSet,
)

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

auth_patterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
]

urlpatterns = [
    path('health/', health, name='Health'),
    path('auth/', include((auth_patterns, 'auth'))),
    path('', include(router.urls)),
]
