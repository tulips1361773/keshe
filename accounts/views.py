from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User, UserProfile, Coach
from .serializers import (
    UserSerializer, UserProfileSerializer, CoachSerializer, CoachApprovalSerializer,
    UserRegistrationSerializer, UserProfileUpdateSerializer
)
from django.db.models import Count, Q
from courses.models import Course, CourseEnrollment
from reservations.models import Booking
from notifications.models import Notification
import json


@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """获取CSRF token API"""
    token = get_token(request)
    return Response({
        'csrfToken': token
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """用户登录API"""
    try:
        data = request.data
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return Response({
                'success': False,
                'message': '用户名和密码不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # 检查教练员审核状态
                if user.user_type == 'coach' and not user.is_active_member:
                    return Response({
                        'success': False,
                        'message': '教练员账户待审核，请联系管理员'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'success': True,
                    'message': '登录成功',
                    'token': token.key,
                    'user': UserSerializer(user).data
                })
            else:
                return Response({
                    'success': False,
                    'message': '账户已被禁用'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'success': False,
                'message': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'登录失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_avatar(request):
    """上传用户头像API"""
    try:
        if 'avatar' not in request.FILES:
            return Response({
                'success': False,
                'message': '请选择要上传的头像文件'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        avatar_file = request.FILES['avatar']
        
        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if avatar_file.content_type not in allowed_types:
            return Response({
                'success': False,
                'message': '不支持的文件类型，请上传 JPG、PNG、GIF 或 WebP 格式的图片'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证文件大小 (5MB)
        if avatar_file.size > 5 * 1024 * 1024:
            return Response({
                'success': False,
                'message': '文件大小不能超过5MB'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 生成文件名
        import uuid
        import os
        from django.conf import settings
        
        file_extension = os.path.splitext(avatar_file.name)[1]
        new_filename = f"avatar_{request.user.id}_{uuid.uuid4().hex[:8]}{file_extension}"
        
        # 保存文件
        avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
        os.makedirs(avatar_dir, exist_ok=True)
        
        file_path = os.path.join(avatar_dir, new_filename)
        
        with open(file_path, 'wb+') as destination:
            for chunk in avatar_file.chunks():
                destination.write(chunk)
        
        # 更新用户头像字段
        avatar_relative_path = f"avatars/{new_filename}"
        request.user.avatar = avatar_relative_path
        request.user.save()
        
        # 返回完整的URL路径
        avatar_url = f"/media/{avatar_relative_path}"
        
        return Response({
            'success': True,
            'message': '头像上传成功',
            'avatar_url': avatar_url
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'头像上传失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """用户登出API"""
    try:
        # 删除用户的token
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response({
            'success': True,
            'message': '登出成功'
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'登出失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    """用户注册API"""
    try:
        # 使用序列化器进行验证和创建
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'message': '注册成功',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        else:
            # 提取第一个错误信息
            error_messages = []
            for field, errors in serializer.errors.items():
                if isinstance(errors, list):
                    error_messages.extend(errors)
                else:
                    error_messages.append(str(errors))
            
            return Response({
                'success': False,
                'message': error_messages[0] if error_messages else '注册数据验证失败'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'注册失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """获取用户资料API"""
    try:
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
            'profile': UserProfileSerializer(profile).data
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取用户资料失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """更新用户资料API"""
    try:
        data = json.loads(request.body)
        user = request.user
        
        # 使用序列化器进行验证和更新
        serializer = UserProfileUpdateSerializer(
            user, 
            data=data, 
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            updated_user = serializer.save()
            profile, created = UserProfile.objects.get_or_create(user=updated_user)
            
            return Response({
                'success': True,
                'message': '资料更新成功',
                'user': UserSerializer(updated_user).data,
                'profile': UserProfileSerializer(profile).data
            })
        else:
            # 提取第一个错误信息
            error_messages = []
            for field, errors in serializer.errors.items():
                if isinstance(errors, list):
                    error_messages.extend(errors)
                else:
                    error_messages.append(str(errors))
            
            return Response({
                'success': False,
                'message': error_messages[0] if error_messages else '数据验证失败'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'success': False,
            'message': f'更新资料失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """修改密码API"""
    try:
        data = json.loads(request.body)
        user = request.user
        
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        # 验证必填字段
        if not all([old_password, new_password, confirm_password]):
            return Response({
                'success': False,
                'message': '所有密码字段都不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证旧密码
        if not user.check_password(old_password):
            return Response({
                'success': False,
                'message': '原密码错误'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证新密码确认
        if new_password != confirm_password:
            return Response({
                'success': False,
                'message': '新密码与确认密码不一致'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证新密码强度（8-16位，包含字母、数字和特殊字符）
        import re
        if len(new_password) < 8 or len(new_password) > 16:
            return Response({
                'success': False,
                'message': '密码长度必须为8-16位'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not re.search(r'[a-zA-Z]', new_password):
            return Response({
                'success': False,
                'message': '密码必须包含字母'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not re.search(r'\d', new_password):
            return Response({
                'success': False,
                'message': '密码必须包含数字'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            return Response({
                'success': False,
                'message': '密码必须包含特殊字符'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新密码
        user.set_password(new_password)
        user.save()
        
        return Response({
            'success': True,
            'message': '密码修改成功'
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'修改密码失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """获取用户统计数据API"""
    try:
        user = request.user
        
        # 根据用户类型获取不同的统计数据
        if user.user_type == 'student':
            # 学生统计数据
            total_courses = CourseEnrollment.objects.filter(student=user).count()
            active_courses = CourseEnrollment.objects.filter(
                student=user, 
                status='confirmed'
            ).count()
            completed_courses = CourseEnrollment.objects.filter(
                student=user, 
                status='completed'
            ).count()
            total_bookings = Booking.objects.filter(
                relation__student=user
            ).count()
            
            stats = {
                'total_courses': total_courses,
                'active_courses': active_courses,
                'completed_courses': completed_courses,
                'total_bookings': total_bookings
            }
            
        elif user.user_type == 'coach':
            # 教练统计数据
            total_courses = Course.objects.filter(coach=user).count()
            active_courses = Course.objects.filter(
                coach=user, 
                status='published'
            ).count()
            total_students = CourseEnrollment.objects.filter(
                course__coach=user
            ).values('student').distinct().count()
            total_bookings = Booking.objects.filter(
                relation__coach=user
            ).count()
            
            stats = {
                'total_courses': total_courses,
                'active_courses': active_courses,
                'total_students': total_students,
                'total_bookings': total_bookings
            }
            
        else:
            # 管理员或其他用户类型的统计数据
            total_users = User.objects.filter(is_active=True).count()
            total_students = User.objects.filter(user_type='student', is_active=True).count()
            total_coaches = User.objects.filter(user_type='coach', is_active=True).count()
            total_courses = Course.objects.count()
            total_enrollments = CourseEnrollment.objects.count()
            total_bookings = Booking.objects.count()
            
            stats = {
                'total_users': total_users,
                'total_students': total_students,
                'total_coaches': total_coaches,
                'total_courses': total_courses,
                'total_enrollments': total_enrollments,
                'total_bookings': total_bookings
            }
        
        return Response({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取统计数据失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 传统Django视图
def login_view(request):
    """登录页面"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, '登录成功！')
                return redirect('dashboard')
            else:
                messages.error(request, '账户已被禁用')
        else:
            messages.error(request, '用户名或密码错误')
    
    return render(request, 'accounts/login.html')


@login_required
def dashboard_view(request):
    """用户仪表板"""
    return render(request, 'accounts/dashboard.html', {
        'user': request.user
    })


@login_required
def profile_view(request):
    """用户资料页面"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'profile': profile
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_coaches(request):
    """获取待审核教练员列表API"""
    try:
        # 检查权限：只有校区管理员和超级管理员可以查看
        if not (request.user.is_super_admin or request.user.is_superuser or 
                request.user.user_type == 'campus_admin'):
            return Response({
                'success': False,
                'message': '没有权限查看待审核教练员'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 获取待审核的教练员
        queryset = Coach.objects.filter(status='pending')
        
        # 如果是校区管理员，只能看到自己校区的教练员
        if request.user.user_type == 'campus_admin':
            queryset = queryset.filter(user__campus=request.user.campus)
        
        serializer = CoachSerializer(queryset, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data,
            'count': queryset.count()
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取待审核教练员失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_coach(request, coach_id):
    """审核教练员API"""
    try:
        # 检查权限：只有校区管理员和超级管理员可以审核
        if not (request.user.is_super_admin or request.user.is_superuser or 
                request.user.user_type == 'campus_admin'):
            return Response({
                'success': False,
                'message': '没有权限审核教练员'
            }, status=status.HTTP_403_FORBIDDEN)
        
        coach = get_object_or_404(Coach, id=coach_id)
        
        # 如果是校区管理员，只能审核自己校区的教练员
        if (request.user.user_type == 'campus_admin' and 
            coach.user.campus != request.user.campus):
            return Response({
                'success': False,
                'message': '只能审核本校区的教练员'
            }, status=status.HTTP_403_FORBIDDEN)
        
        data = json.loads(request.body) if request.body else request.data
        
        serializer = CoachApprovalSerializer(
            coach, 
            data=data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            updated_coach = serializer.save()
            
            # 如果审核通过，激活用户账户并设置会员状态
            if updated_coach.status == 'approved':
                updated_coach.user.is_active = True
                updated_coach.user.is_active_member = True  # 关键修复：设置会员激活状态
                updated_coach.user.save()
            elif updated_coach.status == 'rejected':
                # 如果审核拒绝，确保用户无法登录
                updated_coach.user.is_active_member = False
                updated_coach.user.save()
            
            return Response({
                'success': True,
                'message': '教练员审核成功',
                'data': CoachSerializer(updated_coach).data
            })
        else:
            return Response({
                'success': False,
                'message': '数据验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Coach.DoesNotExist:
        return Response({
            'success': False,
            'message': '教练员不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'审核教练员失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def coach_list(request):
    """获取教练员列表API"""
    try:
        from django.core.paginator import Paginator
        
        # 获取查询参数
        status_filter = request.GET.get('status', 'approved')
        level_filter = request.GET.get('level')
        campus_id = request.GET.get('campus_id')
        search = request.GET.get('search', '')
        ordering = request.GET.get('ordering', '-created_at')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 12))
        
        # 构建查询条件
        queryset = Coach.objects.select_related('user').all()
        
        # 状态筛选
        if status_filter and status_filter != 'all':
            queryset = queryset.filter(status=status_filter)
        
        # 等级筛选
        if level_filter and level_filter != 'all':
            queryset = queryset.filter(coach_level=level_filter)
        
        # 校区筛选
        if campus_id:
            queryset = queryset.filter(user__campus_id=campus_id)
        
        # 搜索筛选
        if search:
            queryset = queryset.filter(
                Q(user__real_name__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__phone__icontains=search) |
                Q(achievements__icontains=search)
            )
        
        # 排序
        if ordering:
            if ordering == '-rating':
                # 按评分排序（暂时使用创建时间，后续可以添加评分字段）
                queryset = queryset.order_by('-created_at')
            elif ordering == '-experience_years':
                # 按经验排序（暂时使用创建时间，后续可以添加经验字段）
                queryset = queryset.order_by('-created_at')
            elif ordering == 'real_name':
                queryset = queryset.order_by('user__real_name')
            else:
                queryset = queryset.order_by(ordering)
        
        # 分页
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = CoachSerializer(page_obj.object_list, many=True)
        
        return Response({
            'success': True,
            'results': serializer.data,
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': page,
            'page_size': page_size,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous()
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取教练员列表失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def coach_detail(request, coach_id):
    """获取教练员详情API"""
    try:
        from django.shortcuts import get_object_or_404
        
        coach = get_object_or_404(Coach.objects.select_related('user'), id=coach_id)
        coach_data = CoachSerializer(coach).data
        
        # 添加额外的统计信息
        coach_data['rating'] = 4.5  # 模拟评分，后续可以从评价系统获取
        coach_data['rating_count'] = 25  # 模拟评价数量
        coach_data['student_count'] = 15  # 模拟学员数量
        coach_data['experience_years'] = 5  # 模拟经验年数
        
        # 添加技能标签（模拟数据）
        coach_data['skills'] = ['乒乓球基础教学', '技术指导', '比赛训练', '青少年培训']
        
        # 添加课程信息（模拟数据）
        coach_data['courses'] = [
            {
                'id': 1,
                'title': '乒乓球基础入门课程',
                'description': '适合初学者的乒乓球基础课程',
                'price': 200,
                'student_count': 12
            },
            {
                'id': 2,
                'title': '乒乓球进阶技巧课程',
                'description': '提升乒乓球技巧的进阶课程',
                'price': 300,
                'student_count': 8
            }
        ]
        
        # 添加学员评价（模拟数据）
        coach_data['reviews'] = [
            {
                'id': 1,
                'student_name': '张同学',
                'student_avatar': '/default-avatar.png',
                'rating': 5,
                'content': '教练非常专业，教学方法很好，进步很快！',
                'created_at': '2024-01-15T10:30:00Z'
            },
            {
                'id': 2,
                'student_name': '李同学',
                'student_avatar': '/default-avatar.png',
                'rating': 4,
                'content': '教练很耐心，技术指导很到位。',
                'created_at': '2024-01-10T14:20:00Z'
            }
        ]
        
        return Response(coach_data)
        
    except Coach.DoesNotExist:
        return Response({
            'success': False,
            'message': '教练员不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取教练员详情失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)