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
from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
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
        data = request.data
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')
        real_name = data.get('real_name')
        user_type = data.get('user_type', 'student')
        
        # 验证必填字段
        if not all([username, password, phone, real_name]):
            return Response({
                'success': False,
                'message': '用户名、密码、手机号和真实姓名不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return Response({
                'success': False,
                'message': '用户名已存在'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查手机号是否已存在
        if User.objects.filter(phone=phone).exists():
            return Response({
                'success': False,
                'message': '手机号已被注册'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建用户
        user = User.objects.create_user(
            username=username,
            password=password,
            phone=phone,
            real_name=real_name,
            user_type=user_type,
            email=data.get('email', ''),
            gender=data.get('gender'),
            birth_date=data.get('birth_date'),
            address=data.get('address'),
            emergency_contact=data.get('emergency_contact'),
            emergency_phone=data.get('emergency_phone')
        )
        
        # 创建用户资料
        UserProfile.objects.create(
            user=user,
            bio=data.get('bio', ''),
            skills=data.get('skills', ''),
            experience_years=data.get('experience_years', 0),
            certification=data.get('certification', '')
        )
        
        return Response({
            'success': True,
            'message': '注册成功',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
        
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
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # 更新用户基本信息
        user.real_name = data.get('real_name', user.real_name)
        user.email = data.get('email', user.email)
        user.gender = data.get('gender', user.gender)
        user.birth_date = data.get('birth_date', user.birth_date)
        user.address = data.get('address', user.address)
        user.emergency_contact = data.get('emergency_contact', user.emergency_contact)
        user.emergency_phone = data.get('emergency_phone', user.emergency_phone)
        user.save()
        
        # 更新用户资料
        profile.bio = data.get('bio', profile.bio)
        profile.skills = data.get('skills', profile.skills)
        profile.experience_years = data.get('experience_years', profile.experience_years)
        profile.certification = data.get('certification', profile.certification)
        profile.save()
        
        return Response({
            'success': True,
            'message': '资料更新成功',
            'user': UserSerializer(user).data,
            'profile': UserProfileSerializer(profile).data
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'更新资料失败: {str(e)}'
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