from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import SystemLog, LoginLog
from .serializers import SystemLogSerializer, LoginLogSerializer
from .permissions import LogViewPermission


class SystemLogViewSet(viewsets.ReadOnlyModelViewSet):
    """系统日志视图集"""
    serializer_class = SystemLogSerializer
    permission_classes = [permissions.IsAuthenticated, LogViewPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action_type', 'resource_type', 'user', 'campus']
    search_fields = ['description', 'resource_name', 'user__username', 'user__real_name']
    ordering_fields = ['created_at', 'action_type', 'resource_type']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """根据用户权限过滤日志"""
        user = self.request.user
        queryset = SystemLog.objects.select_related('user', 'campus')
        
        if user.is_super_admin:
            # 超级管理员可以查看所有日志
            return queryset
        elif user.is_campus_admin:
            # 校区管理员只能查看自己管理的校区的日志
            managed_campuses = user.managed_campus.all()
            if managed_campuses.exists():
                return queryset.filter(campus__in=managed_campuses)
            else:
                return queryset.none()
        else:
            # 其他用户只能查看自己的操作日志
            return queryset.filter(user=user)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """日志统计信息"""
        queryset = self.get_queryset()
        
        # 时间范围过滤
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)
        queryset = queryset.filter(created_at__gte=start_date)
        
        # 统计数据
        total_count = queryset.count()
        action_stats = {}
        resource_stats = {}
        
        for log in queryset:
            # 操作类型统计
            action_display = log.get_action_type_display()
            action_stats[action_display] = action_stats.get(action_display, 0) + 1
            
            # 资源类型统计
            resource_display = log.get_resource_type_display()
            resource_stats[resource_display] = resource_stats.get(resource_display, 0) + 1
        
        return Response({
            'total_count': total_count,
            'days': days,
            'action_statistics': action_stats,
            'resource_statistics': resource_stats,
        })
    
    @action(detail=False, methods=['get'])
    def recent_activities(self, request):
        """最近活动"""
        queryset = self.get_queryset()
        limit = int(request.query_params.get('limit', 10))
        recent_logs = queryset[:limit]
        
        serializer = self.get_serializer(recent_logs, many=True)
        return Response(serializer.data)


class LoginLogViewSet(viewsets.ReadOnlyModelViewSet):
    """登录日志视图集"""
    serializer_class = LoginLogSerializer
    permission_classes = [permissions.IsAuthenticated, LogViewPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'is_successful']
    search_fields = ['user__username', 'user__real_name', 'ip_address']
    ordering_fields = ['login_time', 'logout_time']
    ordering = ['-login_time']
    
    def get_queryset(self):
        """根据用户权限过滤登录日志"""
        user = self.request.user
        queryset = LoginLog.objects.select_related('user')
        
        if user.is_super_admin:
            # 超级管理员可以查看所有登录日志
            return queryset
        elif user.is_campus_admin:
            # 校区管理员只能查看自己管理的校区用户的登录日志
            managed_campuses = user.managed_campus.all()
            if managed_campuses.exists():
                # 获取这些校区的所有用户
                campus_users = []
                for campus in managed_campuses:
                    # 获取校区的学员
                    students = [cs.student for cs in campus.students.filter(is_active=True)]
                    # 获取校区的教练
                    coaches = [cc.coach for cc in campus.coaches.filter(is_active=True)]
                    # 获取校区管理员
                    if campus.manager:
                        campus_users.append(campus.manager)
                    campus_users.extend(students)
                    campus_users.extend(coaches)
                
                return queryset.filter(user__in=campus_users)
            else:
                return queryset.none()
        else:
            # 其他用户只能查看自己的登录日志
            return queryset.filter(user=user)
    
    @action(detail=False, methods=['get'])
    def login_statistics(self, request):
        """登录统计"""
        queryset = self.get_queryset()
        
        # 时间范围过滤
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now() - timedelta(days=days)
        queryset = queryset.filter(login_time__gte=start_date)
        
        total_logins = queryset.count()
        successful_logins = queryset.filter(is_successful=True).count()
        failed_logins = queryset.filter(is_successful=False).count()
        
        # 按日期统计
        daily_stats = {}
        for log in queryset:
            date_key = log.login_time.strftime('%Y-%m-%d')
            if date_key not in daily_stats:
                daily_stats[date_key] = {'successful': 0, 'failed': 0}
            
            if log.is_successful:
                daily_stats[date_key]['successful'] += 1
            else:
                daily_stats[date_key]['failed'] += 1
        
        return Response({
            'total_logins': total_logins,
            'successful_logins': successful_logins,
            'failed_logins': failed_logins,
            'success_rate': round(successful_logins / total_logins * 100, 2) if total_logins > 0 else 0,
            'daily_statistics': daily_stats,
            'days': days,
        })