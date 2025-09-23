from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.utils import timezone
from .models import SystemLog, LoginLog

User = get_user_model()


def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """获取用户代理信息"""
    return request.META.get('HTTP_USER_AGENT', '')


def log_user_action(user, action_type, resource_type, resource_id=None, 
                   resource_name=None, description='', request=None, 
                   extra_data=None, campus=None):
    """记录用户操作日志"""
    ip_address = None
    user_agent = None
    
    if request:
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
    
    return SystemLog.create_log(
        user=user,
        action_type=action_type,
        resource_type=resource_type,
        resource_id=resource_id,
        resource_name=resource_name,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
        extra_data=extra_data,
        campus=campus
    )


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """记录用户登录"""
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    session_key = request.session.session_key
    
    # 创建登录日志
    LoginLog.objects.create(
        user=user,
        login_time=timezone.now(),
        ip_address=ip_address,
        user_agent=user_agent,
        session_key=session_key,
        is_successful=True
    )
    
    # 创建系统日志
    SystemLog.create_log(
        user=user,
        action_type='login',
        resource_type='system',
        description=f'用户 {user.real_name or user.username} 登录系统',
        ip_address=ip_address,
        user_agent=user_agent
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """记录用户登出"""
    if user:
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        session_key = request.session.session_key
        
        # 更新登录日志的登出时间
        try:
            login_log = LoginLog.objects.filter(
                user=user,
                session_key=session_key,
                logout_time__isnull=True
            ).latest('login_time')
            login_log.logout_time = timezone.now()
            login_log.save()
        except LoginLog.DoesNotExist:
            pass
        
        # 创建系统日志
        SystemLog.create_log(
            user=user,
            action_type='logout',
            resource_type='system',
            description=f'用户 {user.real_name or user.username} 退出系统',
            ip_address=ip_address,
            user_agent=user_agent
        )


def log_failed_login(username, ip_address, user_agent, reason='用户名或密码错误'):
    """记录登录失败"""
    try:
        user = User.objects.get(username=username)
        LoginLog.objects.create(
            user=user,
            login_time=timezone.now(),
            ip_address=ip_address,
            user_agent=user_agent,
            is_successful=False,
            failure_reason=reason
        )
        
        SystemLog.create_log(
            user=user,
            action_type='login',
            resource_type='system',
            description=f'用户 {username} 登录失败: {reason}',
            ip_address=ip_address,
            user_agent=user_agent,
            campus=getattr(user, 'campus', None)
        )
    except User.DoesNotExist:
        # 用户不存在时，创建匿名日志
        SystemLog.create_log(
            user=None,
            action_type='login',
            resource_type='system',
            description=f'未知用户 {username} 尝试登录失败: {reason}',
            ip_address=ip_address,
            user_agent=user_agent
        )