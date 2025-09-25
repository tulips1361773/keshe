from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # API路由
    path('list/', views.notification_list, name='api_notification_list'),
    path('stats/', views.notification_stats, name='api_notification_stats'),
    path('unread-count/', views.unread_count, name='api_unread_count'),
    path('<int:notification_id>/', views.notification_detail, name='api_notification_detail'),
    path('<int:notification_id>/mark-read/', views.mark_as_read, name='api_mark_as_read'),
    path('<int:notification_id>/delete/', views.delete_notification, name='api_delete_notification'),
    path('mark-all-read/', views.mark_all_as_read, name='api_mark_all_as_read'),
    path('clear-all/', views.clear_all_notifications, name='api_clear_all_notifications'),
    path('create/', views.create_notification, name='api_create_notification'),
    path('bulk-create/', views.bulk_create_notifications, name='api_bulk_create_notifications'),
    
    # 传统Django视图路由
    path('list/', views.notification_list, name='notification_list'),
    path('stats/', views.notification_stats, name='notification_stats'),
    path('unread-count/', views.unread_count, name='unread_count'),
    path('<int:notification_id>/', views.notification_detail, name='notification_detail'),
    path('<int:notification_id>/mark-read/', views.mark_as_read, name='mark_as_read'),
    path('<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('clear-all/', views.clear_all_notifications, name='clear_all_notifications'),
    path('create/', views.create_notification, name='create_notification'),
    path('bulk-create/', views.bulk_create_notifications, name='bulk_create_notifications'),
]