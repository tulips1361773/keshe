from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# 临时占位视图，后续会完善

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_list(request):
    """课程列表API"""
    return Response({'message': '课程列表功能待实现'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course_create(request):
    """创建课程API"""
    return Response({'message': '创建课程功能待实现'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_detail(request, course_id):
    """课程详情API"""
    return Response({'message': f'课程{course_id}详情功能待实现'})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def course_update(request, course_id):
    """更新课程API"""
    return Response({'message': f'更新课程{course_id}功能待实现'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def course_delete(request, course_id):
    """删除课程API"""
    return Response({'message': f'删除课程{course_id}功能待实现'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course_enroll(request, course_id):
    """课程报名API"""
    return Response({'message': f'报名课程{course_id}功能待实现'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def enrollment_list(request):
    """报名列表API"""
    return Response({'message': '报名列表功能待实现'})

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