import logging
import traceback
import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(MiddlewareMixin):
    """
    自定义错误处理中间件
    统一处理API错误响应和日志记录
    """
    
    def process_exception(self, request, exception):
        """
        处理未捕获的异常
        """
        # 记录详细的错误信息
        error_info = {
            'url': request.get_full_path(),
            'method': request.method,
            'user': str(request.user) if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
            'ip': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
            'traceback': traceback.format_exc()
        }
        
        # 记录请求数据（POST/PUT/PATCH）
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                if hasattr(request, 'body') and request.body:
                    # 尝试解析JSON数据
                    try:
                        error_info['request_data'] = json.loads(request.body.decode('utf-8'))
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        error_info['request_data'] = 'Unable to parse request body'
            except Exception:
                error_info['request_data'] = 'Error reading request body'
        
        # 根据异常类型记录不同级别的日志
        if isinstance(exception, (ValueError, TypeError, KeyError)):
            logger.warning(f"Client error: {error_info}")
        else:
            logger.error(f"Server error: {error_info}")
        
        # 如果是API请求，返回JSON格式的错误响应
        if request.path.startswith('/api/'):
            if settings.DEBUG:
                # 开发环境返回详细错误信息
                return JsonResponse({
                    'error': 'Internal Server Error',
                    'message': str(exception),
                    'type': type(exception).__name__,
                    'traceback': traceback.format_exc().split('\n') if settings.DEBUG else None
                }, status=500)
            else:
                # 生产环境返回通用错误信息
                return JsonResponse({
                    'error': 'Internal Server Error',
                    'message': '服务器内部错误，请稍后重试'
                }, status=500)
        
        # 非API请求，让Django默认处理
        return None
    
    def get_client_ip(self, request):
        """
        获取客户端真实IP地址
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    请求日志记录中间件
    记录所有API请求的详细信息
    """
    
    def process_request(self, request):
        """
        记录请求开始时间
        """
        import time
        request._start_time = time.time()
        
        # 只记录API请求
        if request.path.startswith('/api/'):
            request_info = {
                'url': request.get_full_path(),
                'method': request.method,
                'user': str(request.user) if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
                'ip': self.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            }
            
            # 记录请求参数
            if request.method == 'GET' and request.GET:
                request_info['query_params'] = dict(request.GET)
            
            logger.info(f"API Request: {request_info}")
    
    def process_response(self, request, response):
        """
        记录响应信息
        """
        if hasattr(request, '_start_time') and request.path.startswith('/api/'):
            import time
            duration = time.time() - request._start_time
            
            response_info = {
                'url': request.get_full_path(),
                'method': request.method,
                'status_code': response.status_code,
                'duration_ms': round(duration * 1000, 2),
                'user': str(request.user) if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
            }
            
            # 根据状态码记录不同级别的日志
            if response.status_code >= 500:
                logger.error(f"API Response: {response_info}")
            elif response.status_code >= 400:
                logger.warning(f"API Response: {response_info}")
            else:
                logger.info(f"API Response: {response_info}")
        
        return response
    
    def get_client_ip(self, request):
        """
        获取客户端真实IP地址
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """
    性能监控中间件
    监控慢查询和长时间请求
    """
    
    def process_request(self, request):
        import time
        request._start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, '_start_time'):
            import time
            duration = time.time() - request._start_time
            
            # 记录慢请求（超过2秒）
            if duration > 2.0:
                slow_request_info = {
                    'url': request.get_full_path(),
                    'method': request.method,
                    'duration_seconds': round(duration, 2),
                    'user': str(request.user) if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
                    'status_code': response.status_code
                }
                logger.warning(f"Slow Request: {slow_request_info}")
        
        return response