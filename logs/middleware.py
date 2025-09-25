import json
import time
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from .utils import log_user_action, get_client_ip, get_user_agent


class UserActionLoggingMiddleware(MiddlewareMixin):
    """用户操作日志中间件"""
    
    # 需要记录日志的URL模式
    LOGGED_PATTERNS = [
        'reservations',  # 预约相关
        'accounts',      # 账户相关
        'payments',      # 支付相关
        'competitions',  # 比赛相关
        'notifications', # 通知相关
        'courses',       # 课程相关
        'campus',        # 校区相关
    ]
    
    # 不需要记录日志的操作
    EXCLUDED_PATTERNS = [
        'list',          # 列表查询
        'retrieve',      # 详情查询
        'logs',          # 日志相关
        'admin',         # 管理后台
        'static',        # 静态文件
        'media',         # 媒体文件
    ]
    
    # HTTP方法到操作类型的映射
    METHOD_ACTION_MAP = {
        'POST': 'create',
        'PUT': 'update',
        'PATCH': 'update',
        'DELETE': 'delete',
    }
    
    def process_request(self, request):
        """处理请求"""
        request._log_start_time = time.time()
        return None
    
    def process_response(self, request, response):
        """处理响应"""
        # 检查是否需要记录日志
        if not self._should_log(request, response):
            return response
        
        try:
            # 解析URL
            resolver_match = resolve(request.path_info)
            
            # 获取操作信息
            action_info = self._get_action_info(request, resolver_match)
            if not action_info:
                return response
            
            # 记录日志
            self._log_action(request, response, action_info)
            
        except Exception as e:
            # 日志记录失败不应该影响业务逻辑
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"用户操作日志中间件记录失败: {e}")
        
        return response
    
    def _should_log(self, request, response):
        """判断是否需要记录日志"""
        # 只记录认证用户的操作
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return False
        
        # 检查是否已被标记跳过日志记录
        if hasattr(request, '_skip_logging') and request._skip_logging:
            return False
        
        # 只记录特定HTTP方法
        if request.method not in self.METHOD_ACTION_MAP:
            return False
        
        # 只记录成功的操作（2xx状态码）
        if not (200 <= response.status_code < 300):
            return False
        
        # 检查URL模式
        try:
            resolver_match = resolve(request.path_info)
            namespace = resolver_match.namespace
            url_name = resolver_match.url_name
            
            # 检查是否在需要记录的模式中
            if namespace and namespace in self.LOGGED_PATTERNS:
                # 检查是否在排除的模式中
                if url_name and any(pattern in url_name for pattern in self.EXCLUDED_PATTERNS):
                    return False
                return True
            
            # 检查URL路径
            if any(pattern in request.path_info for pattern in self.LOGGED_PATTERNS):
                if any(pattern in request.path_info for pattern in self.EXCLUDED_PATTERNS):
                    return False
                return True
                
        except Exception:
            pass
        
        return False
    
    def _get_action_info(self, request, resolver_match):
        """获取操作信息"""
        try:
            namespace = resolver_match.namespace
            url_name = resolver_match.url_name
            view_name = resolver_match.view_name
            
            # 获取操作类型
            action_type = self.METHOD_ACTION_MAP.get(request.method, 'other')
            
            # 获取资源类型
            resource_type = 'other'
            if namespace:
                if 'booking' in namespace or 'reservation' in namespace:
                    resource_type = 'booking'
                elif 'account' in namespace or 'user' in namespace:
                    resource_type = 'user'
                elif 'payment' in namespace:
                    resource_type = 'payment'
                elif 'competition' in namespace:
                    resource_type = 'competition'
                elif 'notification' in namespace:
                    resource_type = 'notification'
                elif 'course' in namespace:
                    resource_type = 'course'
                elif 'campus' in namespace:
                    resource_type = 'campus'
            
            # 获取资源ID（从URL参数中）
            resource_id = None
            if resolver_match.kwargs:
                # 常见的ID参数名
                id_params = ['pk', 'id', 'booking_id', 'user_id', 'payment_id', 
                           'competition_id', 'notification_id', 'course_id', 'campus_id']
                for param in id_params:
                    if param in resolver_match.kwargs:
                        resource_id = resolver_match.kwargs[param]
                        break
            
            return {
                'action_type': action_type,
                'resource_type': resource_type,
                'resource_id': resource_id,
                'namespace': namespace,
                'url_name': url_name,
                'view_name': view_name
            }
            
        except Exception:
            return None
    
    def _log_action(self, request, response, action_info):
        """记录操作日志"""
        try:
            # 生成描述
            user_name = request.user.real_name or request.user.username
            action_display = {
                'create': '创建',
                'update': '更新',
                'delete': '删除'
            }.get(action_info['action_type'], action_info['action_type'])
            
            resource_display = {
                'booking': '预约',
                'user': '用户',
                'payment': '支付',
                'competition': '比赛',
                'notification': '通知',
                'course': '课程',
                'campus': '校区'
            }.get(action_info['resource_type'], action_info['resource_type'])
            
            description = f"{user_name} {action_display}了{resource_display}"
            if action_info['resource_id']:
                description += f"（ID: {action_info['resource_id']}）"
            
            # 获取额外数据
            extra_data = {
                'url_name': action_info['url_name'],
                'view_name': action_info['view_name'],
                'method': request.method,
                'status_code': response.status_code
            }
            
            # 添加请求处理时间
            if hasattr(request, '_log_start_time'):
                processing_time = time.time() - request._log_start_time
                extra_data['processing_time'] = round(processing_time, 3)
            
            # 记录日志
            log_user_action(
                user=request.user,
                action_type=action_info['action_type'],
                resource_type=action_info['resource_type'],
                resource_id=action_info['resource_id'],
                description=description,
                request=request,
                extra_data=extra_data
            )
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"记录用户操作日志失败: {e}")