from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import (
    NotificationSerializer, 
    NotificationCreateSerializer,
    NotificationStatsSerializer,
    BulkNotificationSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_list(request):
    """获取消息通知列表"""
    try:
        notifications = Notification.objects.filter(
            recipient=request.user
        ).select_related('sender').order_by('-created_at')
        
        # 筛选条件
        message_type = request.GET.get('message_type')
        is_read = request.GET.get('is_read')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        if message_type:
            notifications = notifications.filter(message_type=message_type)
        
        if is_read is not None:
            is_read_bool = is_read.lower() in ['true', '1', 'yes']
            notifications = notifications.filter(is_read=is_read_bool)
        
        if date_from:
            notifications = notifications.filter(created_at__gte=date_from)
        
        if date_to:
            notifications = notifications.filter(created_at__lte=date_to)
        
        # 分页
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        paginator = Paginator(notifications, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = NotificationSerializer(page_obj.object_list, many=True)
        
        return Response({
            'code': 200,
            'message': '获取消息列表成功',
            'results': serializer.data,
            'count': paginator.count,
            'page': page,
            'page_size': page_size,
            'total_pages': paginator.num_pages
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取消息列表失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_stats(request):
    """获取消息统计信息"""
    try:
        stats = Notification.get_stats(request.user)
        serializer = NotificationStatsSerializer(stats)
        
        return Response({
            'code': 200,
            'message': '获取统计信息成功',
            **serializer.data
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取统计信息失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_detail(request, notification_id):
    """获取消息详情"""
    try:
        notification = Notification.objects.select_related('sender').get(
            id=notification_id,
            recipient=request.user
        )
        
        serializer = NotificationSerializer(notification)
        
        return Response({
            'code': 200,
            'message': '获取消息详情成功',
            'data': serializer.data
        })
        
    except Notification.DoesNotExist:
        return Response({
            'code': 404,
            'message': '消息不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取消息详情失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id):
    """标记消息为已读"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        
        notification.mark_as_read()
        
        return Response({
            'code': 200,
            'message': '消息已标记为已读'
        })
        
    except Notification.DoesNotExist:
        return Response({
            'code': 404,
            'message': '消息不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'标记失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_as_read(request):
    """标记所有消息为已读"""
    try:
        with transaction.atomic():
            updated_count = Notification.objects.filter(
                recipient=request.user,
                is_read=False
            ).update(
                is_read=True,
                read_at=timezone.now()
            )
        
        return Response({
            'code': 200,
            'message': f'已标记 {updated_count} 条消息为已读'
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'批量标记失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    """删除消息"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        
        notification.delete()
        
        return Response({
            'code': 200,
            'message': '消息已删除'
        })
        
    except Notification.DoesNotExist:
        return Response({
            'code': 404,
            'message': '消息不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'删除失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_all_notifications(request):
    """清空所有消息"""
    try:
        with transaction.atomic():
            deleted_count, _ = Notification.objects.filter(
                recipient=request.user
            ).delete()
        
        return Response({
            'code': 200,
            'message': f'已清空 {deleted_count} 条消息'
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'清空失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_notification(request):
    """创建消息通知（管理员功能）"""
    try:
        # 检查权限
        if not request.user.is_staff:
            return Response({
                'code': 403,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = NotificationCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            notification = serializer.save()
            response_serializer = NotificationSerializer(notification)
            
            return Response({
                'code': 200,
                'message': '消息创建成功',
                'data': response_serializer.data
            })
        else:
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'创建消息失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_create_notifications(request):
    """批量创建消息通知（管理员功能）"""
    try:
        # 检查权限
        if not request.user.is_staff:
            return Response({
                'code': 403,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = BulkNotificationSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            notifications = serializer.save()
            
            return Response({
                'code': 200,
                'message': f'批量创建 {len(notifications)} 条消息成功'
            })
        else:
            return Response({
                'code': 400,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'批量创建消息失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_count(request):
    """获取未读消息数量"""
    try:
        count = Notification.get_unread_count(request.user)
        
        return Response({
            'code': 200,
            'message': '获取未读消息数量成功',
            'count': count
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取未读消息数量失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
