from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建路由器
router = DefaultRouter()
router.register(r'relations', views.CoachStudentRelationViewSet, basename='relation')
router.register(r'tables', views.TableViewSet, basename='table')
router.register(r'bookings', views.BookingViewSet, basename='booking')
router.register(r'cancellations', views.BookingCancellationViewSet, basename='cancellation')

app_name = 'reservations'

urlpatterns = [
    # ViewSet路由
    path('', include(router.urls)),
    
    # 额外的API端点
    path('coaches/', views.get_coaches, name='get_coaches'),
    path('students/', views.get_students, name='get_students'),
    path('statistics/', views.booking_statistics, name='booking_statistics'),
]