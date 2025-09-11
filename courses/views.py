from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json

from .models import (
    Course, CourseSchedule, CourseEnrollment, 
    CourseSession, CourseAttendance, CourseEvaluation
)
from .serializers import (
    CourseSerializer, CourseScheduleSerializer, CourseEnrollmentSerializer,
    CourseSessionSerializer, CourseAttendanceSerializer, CourseEvaluationSerializer
)
from accounts.models import User
from campus.models import Campus, CampusArea


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_list(request):
    """课程列表API"""
    try:
        # 获取查询参数
        campus_id = request.GET.get('campus_id')
        course_type = request.GET.get('course_type')
        status_filter = request.GET.get('status')
        search = request.GET.get('search', '')
        
        # 构建查询条件
        queryset = Course.objects.all()
        
        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
        
        if course_type:
            queryset = queryset.filter(course_type=course_type)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(coach__real_name__icontains=search)
            )
        
        serializer = CourseSerializer(queryset, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': queryset.count()
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取课程列表失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course_create(request):
    """创建课程API"""
    try:
        # 检查权限：超级管理员或教练可以创建课程
        if not (request.user.is_super_admin or request.user.is_superuser or 
                request.user.user_type == 'coach'):
            return Response({
                'success': False,
                'message': '没有权限创建课程'
            }, status=status.HTTP_403_FORBIDDEN)
        
        data = json.loads(request.body) if request.body else request.data
        
        serializer = CourseSerializer(data=data)
        
        if serializer.is_valid():
            course = serializer.save()
            return Response({
                'success': True,
                'message': '课程创建成功',
                'data': CourseSerializer(course).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'success': False,
            'message': f'创建课程失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_detail(request, course_id):
    """课程详情API"""
    try:
        course = get_object_or_404(Course, id=course_id)
        serializer = CourseSerializer(course)
        
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Course.DoesNotExist:
        return Response({
            'success': False,
            'message': '课程不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取课程详情失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def course_update(request, course_id):
    """更新课程API"""
    try:
        course = get_object_or_404(Course, id=course_id)
        
        # 检查权限：超级管理员、课程教练或校区管理员可以更新
        if not (request.user.is_super_admin or request.user.is_superuser or 
                course.coach == request.user or course.campus.manager == request.user):
            return Response({
                'success': False,
                'message': '没有权限更新此课程'
            }, status=status.HTTP_403_FORBIDDEN)
        
        data = json.loads(request.body) if request.body else request.data
        
        serializer = CourseSerializer(course, data=data, partial=True)
        
        if serializer.is_valid():
            updated_course = serializer.save()
            return Response({
                'success': True,
                'message': '课程更新成功',
                'data': CourseSerializer(updated_course).data
            })
        else:
            return Response({
                'success': False,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Course.DoesNotExist:
        return Response({
            'success': False,
            'message': '课程不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'更新课程失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def course_delete(request, course_id):
    """删除课程API"""
    try:
        course = get_object_or_404(Course, id=course_id)
        
        # 检查权限：超级管理员、课程教练或校区管理员可以删除
        if not (request.user.is_super_admin or request.user.is_superuser or 
                course.coach == request.user or course.campus.manager == request.user):
            return Response({
                'success': False,
                'message': '没有权限删除此课程'
            }, status=status.HTTP_403_FORBIDDEN)
        
        course_name = course.name
        course.delete()
        
        return Response({
            'success': True,
            'message': f'课程 "{course_name}" 删除成功'
        })
        
    except Course.DoesNotExist:
        return Response({
            'success': False,
            'message': '课程不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'删除课程失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course_enroll(request, course_id):
    """课程报名API"""
    try:
        course = get_object_or_404(Course, id=course_id)
        
        # 检查课程状态
        if course.status != 'published':
            return Response({
                'success': False,
                'message': '课程未发布，无法报名'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = json.loads(request.body) if request.body else request.data
        
        # 如果没有指定学员，默认为当前用户
        student_id = data.get('student_id', request.user.id)
        
        try:
            student = User.objects.get(id=student_id, user_type='student')
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': '学员不存在或用户类型不正确'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 创建报名记录
        enrollment_data = {
            'course': course.id,
            'student': student.id,
            'notes': data.get('notes', '')
        }
        
        serializer = CourseEnrollmentSerializer(data=enrollment_data)
        
        if serializer.is_valid():
            enrollment = serializer.save()
            return Response({
                'success': True,
                'message': '报名成功',
                'data': CourseEnrollmentSerializer(enrollment).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': '报名失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Course.DoesNotExist:
        return Response({
            'success': False,
            'message': '课程不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'报名失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def enrollment_list(request):
    """报名列表API"""
    try:
        # 获取查询参数
        course_id = request.GET.get('course_id')
        student_id = request.GET.get('student_id')
        status_filter = request.GET.get('status')
        
        # 构建查询条件
        queryset = CourseEnrollment.objects.all()
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # 如果是普通学员，只能查看自己的报名
        if request.user.user_type == 'student':
            queryset = queryset.filter(student=request.user)
        
        serializer = CourseEnrollmentSerializer(queryset, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': queryset.count()
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取报名列表失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enrollment_cancel(request, enrollment_id):
    """取消报名API"""
    return Response({'message': f'取消报名{enrollment_id}功能待实现'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_schedules(request, course_id):
    """课程时间表API"""
    return Response({'message': f'课程{course_id}时间表功能待实现'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def schedule_create(request):
    """创建时间表API"""
    return Response({'message': '创建时间表功能待实现'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_sessions(request, course_id):
    """课程课时API"""
    return Response({'message': f'课程{course_id}课时功能待实现'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def session_create(request):
    """创建课时API"""
    return Response({'message': '创建课时功能待实现'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def session_attendance(request, session_id):
    """课时考勤API"""
    return Response({'message': f'课时{session_id}考勤功能待实现'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def attendance_checkin(request):
    """考勤签到API"""
    return Response({'message': '考勤签到功能待实现'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course_evaluate(request, course_id):
    """课程评价API"""
    return Response({'message': f'评价课程{course_id}功能待实现'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def evaluation_list(request):
    """评价列表API"""
    return Response({'message': '评价列表功能待实现'})