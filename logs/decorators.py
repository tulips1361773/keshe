from functools import wraps
from django.http import JsonResponse
from rest_framework.response import Response
from .utils import log_user_action, get_client_ip, get_user_agent


def log_user_operation(action_type, resource_type, description_template=None, 
                      get_resource_info=None, log_on_error=False):
    """
    用户操作日志装饰器
    
    Args:
        action_type: 操作类型 (create, update, delete, approve, etc.)
        resource_type: 资源类型 (booking, user, payment, etc.)
        description_template: 描述模板，可以使用 {user}, {resource_name} 等占位符
        get_resource_info: 函数，用于从请求或响应中提取资源信息
        log_on_error: 是否在操作失败时也记录日志
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # 执行原始视图函数
            response = view_func(request, *args, **kwargs)
            
            # 检查是否需要记录日志
            should_log = False
            
            if isinstance(response, Response):
                # DRF Response
                if response.status_code < 400:
                    should_log = True
                elif log_on_error and response.status_code >= 400:
                    should_log = True
            elif isinstance(response, JsonResponse):
                # Django JsonResponse
                if response.status_code < 400:
                    should_log = True
                elif log_on_error and response.status_code >= 400:
                    should_log = True
            else:
                # 其他响应类型，默认记录
                should_log = True
            
            if should_log and request.user and request.user.is_authenticated:
                try:
                    # 获取资源信息
                    resource_id = None
                    resource_name = None
                    extra_data = {}
                    
                    if get_resource_info:
                        resource_info = get_resource_info(request, response, *args, **kwargs)
                        if resource_info:
                            resource_id = resource_info.get('resource_id')
                            resource_name = resource_info.get('resource_name')
                            extra_data = resource_info.get('extra_data', {})
                    
                    # 生成描述
                    if description_template:
                        description = description_template.format(
                            user=request.user.real_name or request.user.username,
                            resource_name=resource_name or '',
                            action=action_type,
                            **extra_data
                        )
                    else:
                        description = f"用户执行了{action_type}操作"
                    
                    # 记录日志
                    log_user_action(
                        user=request.user,
                        action_type=action_type,
                        resource_type=resource_type,
                        resource_id=resource_id,
                        resource_name=resource_name,
                        description=description,
                        request=request,
                        extra_data=extra_data
                    )
                except Exception as e:
                    # 日志记录失败不应该影响业务逻辑
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"记录用户操作日志失败: {e}")
            
            return response
        return wrapper
    return decorator


def log_model_operation(action_type, get_model_info=None):
    """
    模型操作日志装饰器（用于序列化器）
    
    Args:
        action_type: 操作类型
        get_model_info: 函数，用于从模型实例中提取信息
    """
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            # 执行原始方法
            result = method(self, *args, **kwargs)
            
            # 记录日志
            if hasattr(self, 'context') and 'request' in self.context:
                request = self.context['request']
                if request.user and request.user.is_authenticated:
                    try:
                        # 获取模型信息
                        resource_type = 'other'
                        resource_id = None
                        resource_name = None
                        description = f"用户执行了{action_type}操作"
                        extra_data = {}
                        
                        if get_model_info and result:
                            model_info = get_model_info(result)
                            if model_info:
                                resource_type = model_info.get('resource_type', resource_type)
                                resource_id = model_info.get('resource_id')
                                resource_name = model_info.get('resource_name')
                                description = model_info.get('description', description)
                                extra_data = model_info.get('extra_data', {})
                        
                        # 记录日志
                        log_user_action(
                            user=request.user,
                            action_type=action_type,
                            resource_type=resource_type,
                            resource_id=resource_id,
                            resource_name=resource_name,
                            description=description,
                            request=request,
                            extra_data=extra_data
                        )
                    except Exception as e:
                        # 日志记录失败不应该影响业务逻辑
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.error(f"记录模型操作日志失败: {e}")
            
            return result
        return wrapper
    return decorator