import logging
import traceback
from typing import Dict, Any, Optional
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings

logger = logging.getLogger(__name__)

class APIErrorHandler:
    """
    API错误处理工具类
    提供统一的错误处理和响应格式
    """
    
    @staticmethod
    def handle_validation_error(errors: Dict[str, Any], message: str = "数据验证失败") -> Response:
        """
        处理数据验证错误
        """
        logger.warning(f"Validation error: {errors}")
        
        # 格式化错误信息
        formatted_errors = {}
        for field, error_list in errors.items():
            if isinstance(error_list, list):
                formatted_errors[field] = error_list[0] if error_list else "未知错误"
            else:
                formatted_errors[field] = str(error_list)
        
        return Response({
            'error': 'validation_error',
            'message': message,
            'details': formatted_errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def handle_permission_error(message: str = "权限不足") -> Response:
        """
        处理权限错误
        """
        logger.warning(f"Permission denied: {message}")
        return Response({
            'error': 'permission_denied',
            'message': message
        }, status=status.HTTP_403_FORBIDDEN)
    
    @staticmethod
    def handle_not_found_error(resource: str = "资源") -> Response:
        """
        处理资源未找到错误
        """
        message = f"{resource}不存在"
        logger.info(f"Resource not found: {message}")
        return Response({
            'error': 'not_found',
            'message': message
        }, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def handle_conflict_error(message: str = "资源冲突") -> Response:
        """
        处理资源冲突错误
        """
        logger.warning(f"Conflict error: {message}")
        return Response({
            'error': 'conflict',
            'message': message
        }, status=status.HTTP_409_CONFLICT)
    
    @staticmethod
    def handle_server_error(exception: Exception, context: str = "服务器处理") -> Response:
        """
        处理服务器内部错误
        """
        error_id = id(exception)  # 生成错误ID用于追踪
        
        logger.error(f"Server error [{error_id}] in {context}: {str(exception)}")
        logger.error(f"Traceback [{error_id}]: {traceback.format_exc()}")
        
        if settings.DEBUG:
            return Response({
                'error': 'server_error',
                'message': f"{context}时发生错误",
                'debug_info': {
                    'exception_type': type(exception).__name__,
                    'exception_message': str(exception),
                    'error_id': error_id
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'error': 'server_error',
                'message': f"{context}时发生错误，请稍后重试",
                'error_id': error_id
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @staticmethod
    def handle_authentication_error(message: str = "身份认证失败") -> Response:
        """
        处理身份认证错误
        """
        logger.warning(f"Authentication error: {message}")
        return Response({
            'error': 'authentication_failed',
            'message': message
        }, status=status.HTTP_401_UNAUTHORIZED)

class BusinessLogicError(Exception):
    """
    业务逻辑错误异常类
    """
    def __init__(self, message: str, error_code: str = None, status_code: int = 400):
        self.message = message
        self.error_code = error_code or 'business_logic_error'
        self.status_code = status_code
        super().__init__(self.message)

class PerformanceMonitor:
    """
    性能监控工具类
    """
    
    @staticmethod
    def log_slow_query(query_time: float, query: str, threshold: float = 1.0):
        """
        记录慢查询
        """
        if query_time > threshold:
            logger.warning(f"Slow query detected: {query_time:.2f}s - {query}")
    
    @staticmethod
    def log_memory_usage(context: str):
        """
        记录内存使用情况
        """
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            
            if memory_mb > 500:  # 超过500MB记录警告
                logger.warning(f"High memory usage in {context}: {memory_mb:.2f}MB")
            else:
                logger.info(f"Memory usage in {context}: {memory_mb:.2f}MB")
        except ImportError:
            logger.debug("psutil not available for memory monitoring")
        except Exception as e:
            logger.error(f"Error monitoring memory usage: {e}")

def log_user_action(user, action: str, resource: str = None, details: Dict[str, Any] = None):
    """
    记录用户操作日志
    """
    log_data = {
        'user': str(user),
        'user_id': user.id if hasattr(user, 'id') else None,
        'action': action,
        'resource': resource,
        'details': details or {}
    }
    
    logger.info(f"User action: {log_data}")

def validate_and_log_api_request(request, required_fields: list = None, optional_fields: list = None):
    """
    验证并记录API请求
    """
    try:
        import json
        
        # 记录请求信息
        request_info = {
            'method': request.method,
            'path': request.path,
            'user': str(request.user) if hasattr(request, 'user') else 'Anonymous',
        }
        
        # 解析请求数据
        if request.method in ['POST', 'PUT', 'PATCH'] and hasattr(request, 'body'):
            try:
                data = json.loads(request.body.decode('utf-8'))
                request_info['data_keys'] = list(data.keys()) if isinstance(data, dict) else 'non-dict-data'
                
                # 验证必需字段
                if required_fields:
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        logger.warning(f"Missing required fields: {missing_fields} in request: {request_info}")
                        return False, missing_fields
                
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                logger.warning(f"Invalid JSON in request: {request_info}, error: {e}")
                return False, ['Invalid JSON format']
        
        logger.info(f"Valid API request: {request_info}")
        return True, None
        
    except Exception as e:
        logger.error(f"Error validating API request: {e}")
        return False, ['Request validation error']