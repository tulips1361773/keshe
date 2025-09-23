from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SystemLogViewSet, LoginLogViewSet

router = DefaultRouter()
router.register(r'system-logs', SystemLogViewSet, basename='systemlog')
router.register(r'login-logs', LoginLogViewSet, basename='loginlog')

app_name = 'logs'

urlpatterns = [
    path('api/', include(router.urls)),
]