from rest_framework import permissions


class LogViewPermission(permissions.BasePermission):
    """日志查看权限"""
    
    def has_permission(self, request, view):
        """检查用户是否有查看日志的权限"""
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 超级管理员和校区管理员可以查看日志
        if request.user.is_super_admin or request.user.is_campus_admin:
            return True
        
        # 普通用户只能查看自己的日志（在视图中进一步限制）
        return True
    
    def has_object_permission(self, request, view, obj):
        """检查用户是否有查看特定日志对象的权限"""
        user = request.user
        
        if user.is_super_admin:
            # 超级管理员可以查看所有日志
            return True
        elif user.is_campus_admin:
            # 校区管理员只能查看自己管理的校区的日志
            managed_campuses = user.managed_campus.all()
            
            if hasattr(obj, 'campus') and obj.campus:
                return obj.campus in managed_campuses
            elif hasattr(obj, 'user') and obj.user:
                # 检查用户是否属于管理的校区
                for campus in managed_campuses:
                    # 检查是否是校区管理员
                    if campus.manager == obj.user:
                        return True
                    # 检查是否是校区学员
                    if campus.students.filter(student=obj.user, is_active=True).exists():
                        return True
                    # 检查是否是校区教练
                    if campus.coaches.filter(coach=obj.user, is_active=True).exists():
                        return True
                return False
            return False
        else:
            # 普通用户只能查看自己的日志
            return hasattr(obj, 'user') and obj.user == user