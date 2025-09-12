from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'accounts'

# API路由
urlpatterns = [
    # 认证相关API
    path('api/csrf-token/', views.get_csrf_token, name='api_csrf_token'),
    path('api/login/', views.user_login, name='api_login'),
    path('api/logout/', views.user_logout, name='api_logout'),
    path('api/register/', views.user_register, name='api_register'),
    path('api/profile/', views.user_profile, name='api_profile'),
    path('api/profile/update/', views.update_profile, name='api_update_profile'),
    path('api/change-password/', views.change_password, name='api_change_password'),
    path('api/stats/', views.user_stats, name='api_user_stats'),
    
    # 教练员管理API
    path('api/coaches/pending/', views.pending_coaches, name='api_pending_coaches'),
    path('api/coaches/<int:coach_id>/approve/', views.approve_coach, name='api_approve_coach'),
    path('api/coaches/', views.coach_list, name='api_coach_list'),
    path('api/coaches/<int:coach_id>/', views.coach_detail, name='api_coach_detail'),
    
    # 头像上传API
    path('api/upload-avatar/', views.upload_avatar, name='upload_avatar'),
    
    # 传统Django视图
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
]