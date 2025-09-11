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
    try:
        from django.utils import timezone
        from django.db import transaction
        
        enrollment = get_object_or_404(CourseEnrollment, id=enrollment_id)
        
        # 权限检查：只有学员本人或管理员可以取消报名
        if enrollment.student != request.user and not request.user.is_staff:
            return Response({
                'success': False,
                'message': '没有权限取消此报名'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 检查报名状态
        if enrollment.status == 'cancelled':
            return Response({
                'success': False,
                'message': '报名已经取消'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if enrollment.status == 'completed':
            return Response({
                'success': False,
                'message': '课程已完成，无法取消报名'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查课程是否已开始
        if enrollment.course.start_date <= timezone.now().date():
            return Response({
                'success': False,
                'message': '课程已开始，无法取消报名'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            # 更新报名状态
            enrollment.status = 'cancelled'
            enrollment.save()
            
            # 如果有支付记录，可能需要处理退款（这里简化处理）
            if enrollment.payment_status == 'paid':
                enrollment.payment_status = 'refunded'
                enrollment.save()
        
        return Response({
            'success': True,
            'message': '取消报名成功',
            'data': CourseEnrollmentSerializer(enrollment).data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'取消报名失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_schedules(request, course_id):
    """课程时间表API"""
    try:
        course = get_object_or_404(Course, id=course_id)
        schedules = CourseSchedule.objects.filter(course=course, is_active=True).order_by('weekday', 'start_time')
        serializer = CourseScheduleSerializer(schedules, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': schedules.count()
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取课程时间表失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def schedule_create(request):
    """创建时间表API"""
    try:
        data = request.data
        course_id = data.get('course_id')
        
        # 验证课程存在且用户有权限
        course = get_object_or_404(Course, id=course_id)
        if course.coach != request.user and not request.user.is_staff:
            return Response({
                'success': False,
                'message': '没有权限为此课程创建时间表'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 创建时间表
        schedule_data = {
            'course': course.id,
            'weekday': data.get('weekday'),
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time')
        }
        
        serializer = CourseScheduleSerializer(data=schedule_data)
        if serializer.is_valid():
            schedule = serializer.save()
            return Response({
                'success': True,
                'message': '时间表创建成功',
                'data': CourseScheduleSerializer(schedule).data
            })
        else:
            return Response({
                'success': False,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'success': False,
            'message': f'创建时间表失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_sessions(request, course_id):
    """课程课时API"""
    try:
        course = get_object_or_404(Course, id=course_id)
        
        # 权限检查：教练可以看到自己的课程，学员可以看到已报名的课程
        if course.coach != request.user and not request.user.is_staff:
            # 检查学员是否已报名此课程
            enrollment = CourseEnrollment.objects.filter(
                course=course,
                student=request.user,
                status='confirmed'
            ).first()
            if not enrollment:
                return Response({
                    'success': False,
                    'message': '没有权限查看此课程的课时信息'
                }, status=status.HTTP_403_FORBIDDEN)
        
        sessions = CourseSession.objects.filter(course=course).order_by('session_number')
        serializer = CourseSessionSerializer(sessions, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': sessions.count()
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取课程课时失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def session_create(request):
    """创建课时API"""
    try:
        data = request.data
        course_id = data.get('course_id')
        
        # 验证课程存在且用户有权限
        course = get_object_or_404(Course, id=course_id)
        if course.coach != request.user and not request.user.is_staff:
            return Response({
                'success': False,
                'message': '没有权限为此课程创建课时'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 创建课时
        session_data = {
            'course': course.id,
            'session_number': data.get('session_number'),
            'scheduled_date': data.get('scheduled_date'),
            'scheduled_time': data.get('scheduled_time'),
            'content': data.get('content', ''),
            'homework': data.get('homework', ''),
            'notes': data.get('notes', '')
        }
        
        serializer = CourseSessionSerializer(data=session_data)
        if serializer.is_valid():
            session = serializer.save()
            return Response({
                'success': True,
                'message': '课时创建成功',
                'data': CourseSessionSerializer(session).data
            })
        else:
            return Response({
                'success': False,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'success': False,
            'message': f'创建课时失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def session_attendance(request, session_id):
    """课时考勤API"""
    try:
        session = get_object_or_404(CourseSession, id=session_id)
        
        # 权限检查：教练可以看到自己课程的考勤，学员只能看到自己的考勤
        if session.course.coach != request.user and not request.user.is_staff:
            # 学员只能查看自己的考勤记录
            attendances = CourseAttendance.objects.filter(
                session=session,
                student=request.user
            )
        else:
            # 教练和管理员可以查看所有考勤记录
            attendances = CourseAttendance.objects.filter(session=session)
        
        serializer = CourseAttendanceSerializer(attendances, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': attendances.count()
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取课时考勤失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def attendance_checkin(request):
    """考勤签到API"""
    try:
        from django.utils import timezone
        
        data = request.data
        session_id = data.get('session_id')
        attendance_status = data.get('status', 'present')
        
        # 验证课时存在
        session = get_object_or_404(CourseSession, id=session_id)
        
        # 检查用户是否有权限签到（必须是该课程的学员或教练）
        if session.course.coach == request.user:
            # 教练可以为学员签到
            student_id = data.get('student_id')
            if not student_id:
                return Response({
                    'success': False,
                    'message': '教练签到需要指定学员ID'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            student = get_object_or_404(User, id=student_id, user_type='student')
            
            # 验证学员是否报名了该课程
            enrollment = CourseEnrollment.objects.filter(
                course=session.course,
                student=student,
                status='confirmed'
            ).first()
            if not enrollment:
                return Response({
                    'success': False,
                    'message': '该学员未报名此课程'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 学员自己签到
            student = request.user
            
            # 验证学员是否报名了该课程
            enrollment = CourseEnrollment.objects.filter(
                course=session.course,
                student=student,
                status='confirmed'
            ).first()
            if not enrollment:
                return Response({
                    'success': False,
                    'message': '您未报名此课程，无法签到'
                }, status=status.HTTP_403_FORBIDDEN)
        
        # 创建或更新考勤记录
        attendance, created = CourseAttendance.objects.get_or_create(
            session=session,
            student=student,
            defaults={
                'status': attendance_status,
                'check_in_time': timezone.now() if attendance_status == 'present' else None,
                'notes': data.get('notes', '')
            }
        )
        
        if not created:
            # 更新现有记录
            attendance.status = attendance_status
            if attendance_status == 'present' and not attendance.check_in_time:
                attendance.check_in_time = timezone.now()
            attendance.notes = data.get('notes', attendance.notes)
            attendance.save()
        
        serializer = CourseAttendanceSerializer(attendance)
        
        return Response({
            'success': True,
            'message': '签到成功' if created else '考勤记录已更新',
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'签到失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course_evaluate(request, course_id):
    """课程评价API"""
    try:
        from django.db import transaction
        from .models import CourseEvaluation
        
        # 验证课程存在
        course = get_object_or_404(Course, id=course_id)
        
        # 检查用户是否有权限评价该课程（需要是该课程的学员且课程已结束）
        enrollment = CourseEnrollment.objects.filter(
            course=course,
            student=request.user,
            status='confirmed'
        ).first()
        
        if not enrollment:
            return Response({
                'code': 400,
                'message': '您没有权限评价该课程'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查课程是否已结束
        if course.end_time > timezone.now():
            return Response({
                'code': 400,
                'message': '课程尚未结束，无法评价'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查是否已经评价过
        existing_evaluation = CourseEvaluation.objects.filter(
            course=course,
            student=request.user
        ).first()
        
        data = request.data
        rating = data.get('rating')
        comment = data.get('comment', '')
        coach_rating = data.get('coach_rating', rating)
        facility_rating = data.get('facility_rating', rating)
        is_anonymous = data.get('is_anonymous', False)
        
        # 验证评分范围
        if not (1 <= rating <= 5):
            return Response({
                'code': 400,
                'message': '评分必须在1-5之间'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            if existing_evaluation:
                # 更新现有评价
                existing_evaluation.rating = rating
                existing_evaluation.comment = comment
                existing_evaluation.coach_rating = coach_rating
                existing_evaluation.facility_rating = facility_rating
                existing_evaluation.is_anonymous = is_anonymous
                existing_evaluation.save()
                evaluation = existing_evaluation
                message = '评价更新成功'
            else:
                # 创建新评价
                evaluation = CourseEvaluation.objects.create(
                    course=course,
                    student=request.user,
                    rating=rating,
                    comment=comment,
                    coach_rating=coach_rating,
                    facility_rating=facility_rating,
                    is_anonymous=is_anonymous
                )
                message = '评价提交成功'
        
        from .serializers import CourseEvaluationSerializer
        serializer = CourseEvaluationSerializer(evaluation)
        
        return Response({
            'code': 200,
            'message': message,
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'评价失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def evaluation_list(request):
    """评价列表API"""
    if request.method == 'GET':
        try:
            from django.core.paginator import Paginator
            from .models import CourseEvaluation
            from .serializers import CourseEvaluationSerializer
            
            evaluations = CourseEvaluation.objects.select_related(
                'course', 'student', 'course__coach'
            ).order_by('-created_at')
            
            # 筛选条件
            course_id = request.GET.get('course')
            coach_id = request.GET.get('coach')
            rating = request.GET.get('rating')
            
            if course_id:
                evaluations = evaluations.filter(course_id=course_id)
            if coach_id:
                evaluations = evaluations.filter(course__coach_id=coach_id)
            if rating:
                evaluations = evaluations.filter(rating=rating)
            
            # 如果不是管理员，只能看到自己的评价或公开的评价
            if not request.user.is_staff:
                evaluations = evaluations.filter(
                    Q(student=request.user) | Q(is_anonymous=False)
                )
            
            # 分页
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            paginator = Paginator(evaluations, page_size)
            page_obj = paginator.get_page(page)
            
            serializer = CourseEvaluationSerializer(page_obj.object_list, many=True)
            
            return Response({
                'code': 200,
                'message': '获取评价列表成功',
                'data': {
                    'results': serializer.data,
                    'count': paginator.count,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': paginator.num_pages
                }
            })
            
        except Exception as e:
            return Response({
                'code': 400,
                'message': f'获取评价列表失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'POST':
        try:
            from django.db import transaction
            from .models import CourseEvaluation
            from .serializers import CourseEvaluationSerializer
            
            data = request.data
            course_id = data.get('course')
            rating = data.get('rating')
            comment = data.get('comment', '')
            coach_rating = data.get('coach_rating', rating)
            facility_rating = data.get('facility_rating', rating)
            is_anonymous = data.get('is_anonymous', False)
            
            # 验证课程存在
            course = get_object_or_404(Course, id=course_id)
            
            # 检查用户是否有权限评价该课程
            enrollment = CourseEnrollment.objects.filter(
                course=course,
                student=request.user,
                status__in=['confirmed', 'completed']
            ).first()
            
            if not enrollment:
                return Response({
                    'code': 400,
                    'message': '您没有权限评价该课程，只能评价已报名的课程'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 检查是否已经评价过
            existing_evaluation = CourseEvaluation.objects.filter(
                course=course,
                student=request.user
            ).first()
            
            # 验证评分范围
            if not (1 <= rating <= 5):
                return Response({
                    'code': 400,
                    'message': '评分必须在1-5之间'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                if existing_evaluation:
                    # 更新现有评价
                    existing_evaluation.rating = rating
                    existing_evaluation.comment = comment
                    existing_evaluation.coach_rating = coach_rating
                    existing_evaluation.facility_rating = facility_rating
                    existing_evaluation.is_anonymous = is_anonymous
                    existing_evaluation.save()
                    evaluation = existing_evaluation
                    message = '评价更新成功'
                else:
                    # 创建新评价
                    evaluation = CourseEvaluation.objects.create(
                        course=course,
                        student=request.user,
                        rating=rating,
                        comment=comment,
                        coach_rating=coach_rating,
                        facility_rating=facility_rating,
                        is_anonymous=is_anonymous
                    )
                    message = '评价提交成功'
            
            serializer = CourseEvaluationSerializer(evaluation)
            
            return Response({
                'code': 200,
                'message': message,
                'data': serializer.data
            })
            
        except Exception as e:
            return Response({
                'code': 400,
                'message': f'评价失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)