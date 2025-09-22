from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'reservations'

urlpatterns = [
    # 师生关系管理
    path('relations/', views.CoachStudentRelationListCreateView.as_view(), name='relation-list-create'),
    path('relations/<int:pk>/', views.CoachStudentRelationDetailView.as_view(), name='relation-detail'),
    path('relations/<int:relation_id>/approve/', views.approve_relation, name='approve-relation'),
    
    # 球台管理
    path('tables/', views.TableListView.as_view(), name='table-list'),
    path('tables/available/', views.available_tables, name='available-tables'),
    
    # 预约管理
    path('bookings/', views.BookingListCreateView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/<int:pk>/cancel/', views.BookingDetailView.as_view(), name='booking-cancel'),
    path('bookings/<int:booking_id>/confirm/', views.confirm_booking, name='booking-confirm'),
    path('bookings/cancel_stats/', views.cancel_stats, name='cancel-stats'),
    path('cancellations/<int:cancellation_id>/approve/', views.approve_cancellation, name='approve-cancellation'),
    path('cancellations/pending/', views.pending_cancellations, name='pending-cancellations'),
    
    # 教练列表
    path('coaches/', views.coach_list, name='coach-list'),
    
    # ==================== 教练更换相关路由 ====================
    
    # 教练更换请求管理
    path('coach-change-requests/', views.CoachChangeRequestListCreateView.as_view(), name='coach-change-request-list-create'),
    path('coach-change-requests/<int:pk>/', views.CoachChangeRequestDetailView.as_view(), name='coach-change-request-detail'),
    
    # 教练更换审批
    path('coach-change-requests/<int:request_id>/approve/', views.approve_coach_change, name='approve-coach-change'),
    
    # 我的教练更换请求
    path('my-coach-change-requests/', views.my_coach_change_requests, name='my-coach-change-requests'),
    
    # 待我审批的教练更换请求
    path('pending-coach-change-approvals/', views.pending_coach_change_approvals, name='pending-coach-change-approvals'),
    
    # 教练更换统计信息
    path('coach-change-statistics/', views.coach_change_statistics, name='coach-change-statistics'),
]