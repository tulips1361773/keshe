from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Campus, CampusArea, CampusStudent, CampusCoach
from .serializers import (
    CampusSerializer, CampusAreaSerializer,
    CampusStudentSerializer, CampusCoachSerializer
)
from accounts.models import User
import json


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def campus_list(request):
    """校区列表API"""
    try:
        # 获取查询参数
        search = request.GET.get('search', '')
        is_active = request.GET.get('is_active')
        
        # 构建查询条件
        queryset = Campus.objects.all()
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(address__icontains=search)
            )
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # 序列化数据
        serializer = CampusSerializer(queryset, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': queryset.count()
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取校区列表失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def campus_create(request):
    """创建校区API"""
    try:
        # 检查权限：只有超级管理员可以创建校区
        if not request.user.is_super_admin and not request.user.is_superuser:
            return Response({
                'success': False,
                'message': '只有超级管理员可以创建校区'
            }, status=status.HTTP_403_FORBIDDEN)
        
        data = json.loads(request.body) if request.body else request.data
        serializer = CampusSerializer(data=data)
        
        if serializer.is_valid():
            campus = serializer.save()
            return Response({
                'success': True,
                'message': '校区创建成功',
                'data': CampusSerializer(campus).data
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
            'message': f'创建校区失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def campus_detail(request, campus_id):
    """校区详情API"""
    try:
        campus = get_object_or_404(Campus, id=campus_id)
        serializer = CampusSerializer(campus)
        
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Campus.DoesNotExist:
        return Response({
            'success': False,
            'message': '校区不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取校区详情失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def campus_update(request, campus_id):
    """更新校区API"""
    try:
        campus = get_object_or_404(Campus, id=campus_id)
        
        # 检查权限：超级管理员或校区管理员可以更新
        if not (request.user.is_super_admin or request.user.is_superuser or 
                campus.manager == request.user):
            return Response({
                'success': False,
                'message': '没有权限更新此校区'
            }, status=status.HTTP_403_FORBIDDEN)
        
        data = json.loads(request.body) if request.body else request.data
        serializer = CampusSerializer(campus, data=data, partial=True)
        
        if serializer.is_valid():
            campus = serializer.save()
            return Response({
                'success': True,
                'message': '校区更新成功',
                'data': CampusSerializer(campus).data
            })
        else:
            return Response({
                'success': False,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except Campus.DoesNotExist:
        return Response({
            'success': False,
            'message': '校区不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'更新校区失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def campus_delete(request, campus_id):
    """删除校区API"""
    try:
        campus = get_object_or_404(Campus, id=campus_id)
        
        # 检查权限：只有超级管理员可以删除校区
        if not request.user.is_super_admin and not request.user.is_superuser:
            return Response({
                'success': False,
                'message': '只有超级管理员可以删除校区'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 检查是否有关联数据
        if campus.students.exists() or campus.coaches.exists():
            return Response({
                'success': False,
                'message': '校区下还有学员或教练，无法删除'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        campus_name = campus.name
        campus.delete()
        
        return Response({
            'success': True,
            'message': f'校区 {campus_name} 删除成功'
        })
    except Campus.DoesNotExist:
        return Response({
            'success': False,
            'message': '校区不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'删除校区失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def campus_areas(request, campus_id):
    """校区分区列表API"""
    try:
        campus = get_object_or_404(Campus, id=campus_id)
        areas = CampusArea.objects.filter(campus=campus)
        serializer = CampusAreaSerializer(areas, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': areas.count()
        })
    except Campus.DoesNotExist:
        return Response({
            'success': False,
            'message': '校区不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取校区分区列表失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def campus_area_create(request, campus_id):
    """创建校区分区API"""
    try:
        campus = get_object_or_404(Campus, id=campus_id)
        
        # 检查权限：超级管理员或校区管理员可以创建分区
        if not (request.user.is_super_admin or request.user.is_superuser or 
                campus.manager == request.user):
            return Response({
                'success': False,
                'message': '没有权限在此校区创建分区'
            }, status=status.HTTP_403_FORBIDDEN)
        
        data = json.loads(request.body) if request.body else request.data
        data['campus'] = campus.id
        
        serializer = CampusAreaSerializer(data=data)
        
        if serializer.is_valid():
            area = serializer.save()
            return Response({
                'success': True,
                'message': '分区创建成功',
                'data': CampusAreaSerializer(area).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except Campus.DoesNotExist:
        return Response({
            'success': False,
            'message': '校区不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'创建分区失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def campus_students(request, campus_id):
    """校区学员列表API"""
    try:
        campus = get_object_or_404(Campus, id=campus_id)
        
        # 获取查询参数
        search = request.GET.get('search', '')
        membership_type = request.GET.get('membership_type')
        is_active = request.GET.get('is_active')
        
        # 构建查询条件
        queryset = CampusStudent.objects.filter(campus=campus)
        
        if search:
            queryset = queryset.filter(
                Q(student__username__icontains=search) |
                Q(student__first_name__icontains=search) |
                Q(student__last_name__icontains=search) |
                Q(student__phone__icontains=search)
            )
        
        if membership_type:
            queryset = queryset.filter(membership_type=membership_type)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        serializer = CampusStudentSerializer(queryset, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': queryset.count()
        })
    except Campus.DoesNotExist:
        return Response({
            'success': False,
            'message': '校区不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取校区学员列表失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def campus_student_add(request, campus_id):
    """添加学员到校区API"""
    try:
        campus = get_object_or_404(Campus, id=campus_id)
        
        # 检查权限：超级管理员或校区管理员可以添加学员
        if not (request.user.is_super_admin or request.user.is_superuser or 
                campus.manager == request.user):
            return Response({
                'success': False,
                'message': '没有权限添加学员到此校区'
            }, status=status.HTTP_403_FORBIDDEN)
        
        data = json.loads(request.body) if request.body else request.data
        
        # 获取学员用户
        student_id = data.get('student_id')
        if not student_id:
            return Response({
                'success': False,
                'message': '学员ID不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = User.objects.get(id=student_id, user_type='student')
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': '学员不存在或用户类型不正确'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 检查学员是否已在此校区
        if CampusStudent.objects.filter(campus=campus, student=student).exists():
            return Response({
                'success': False,
                'message': '该学员已在此校区'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建校区学员关联
        student_data = {
            'campus': campus.id,
            'student': student.id,
            'membership_type': data.get('membership_type', 'monthly'),
            'notes': data.get('notes', '')
        }
        
        serializer = CampusStudentSerializer(data=student_data)
        
        if serializer.is_valid():
            campus_student = serializer.save()
            return Response({
                'success': True,
                'message': '学员添加成功',
                'data': CampusStudentSerializer(campus_student).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Campus.DoesNotExist:
        return Response({
            'success': False,
            'message': '校区不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'添加学员失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def campus_coaches(request, campus_id):
    """校区教练列表API"""
    try:
        campus = get_object_or_404(Campus, id=campus_id)
        
        # 获取查询参数
        search = request.GET.get('search', '')
        is_active = request.GET.get('is_active')
        
        # 构建查询条件
        queryset = CampusCoach.objects.filter(campus=campus)
        
        if search:
            queryset = queryset.filter(
                Q(coach__username__icontains=search) |
                Q(coach__first_name__icontains=search) |
                Q(coach__last_name__icontains=search) |
                Q(coach__phone__icontains=search)
            )
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        serializer = CampusCoachSerializer(queryset, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': queryset.count()
        })
    except Campus.DoesNotExist:
        return Response({
            'success': False,
            'message': '校区不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取校区教练列表失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def campus_coach_add(request, campus_id):
    """添加教练到校区API"""
    try:
        campus = get_object_or_404(Campus, id=campus_id)
        
        # 检查权限：超级管理员或校区管理员可以添加教练
        if not (request.user.is_super_admin or request.user.is_superuser or 
                campus.manager == request.user):
            return Response({
                'success': False,
                'message': '没有权限添加教练到此校区'
            }, status=status.HTTP_403_FORBIDDEN)
        
        data = json.loads(request.body) if request.body else request.data
        
        # 获取教练用户
        coach_id = data.get('coach_id')
        if not coach_id:
            return Response({
                'success': False,
                'message': '教练ID不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            coach = User.objects.get(id=coach_id, user_type='coach')
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': '教练不存在或用户类型不正确'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 检查教练是否已在此校区
        if CampusCoach.objects.filter(campus=campus, coach=coach).exists():
            return Response({
                'success': False,
                'message': '该教练已在此校区'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建校区教练关联
        coach_data = {
            'campus': campus.id,
            'coach': coach.id,
            'specialties': data.get('specialties', ''),
            'max_students': data.get('max_students', 20),
            'hourly_rate': data.get('hourly_rate', 0.00),
            'notes': data.get('notes', '')
        }
        
        serializer = CampusCoachSerializer(data=coach_data)
        
        if serializer.is_valid():
            campus_coach = serializer.save()
            return Response({
                'success': True,
                'message': '教练添加成功',
                'data': CampusCoachSerializer(campus_coach).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Campus.DoesNotExist:
        return Response({
            'success': False,
            'message': '校区不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'添加教练失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)