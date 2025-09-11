from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # 消息列表和统计
    path('list/', views.notification_list, name='notification_list'),
    path('stats/', views.notification_stats, name='notification_stats'),
    path('unread-count/', views.unread_count, name='unread_count'),
    
    # 消息详情和操作
    path('<int:notification_id>/', views.notification_detail, name='notification_detail'),
    path('<int:notification_id>/mark-read/', views.mark_as_read, name='mark_as_read'),
    path('<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    
    # 批量操作
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('clear-all/', views.clear_all_notifications, name='clear_all_notifications'),
    
    # 管理员功能
    path('create/', views.create_notification, name='create_notification'),
    path('bulk-create/', views.bulk_create_notifications, name='bulk_create_notifications'),
]