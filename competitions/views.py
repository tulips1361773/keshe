from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
import random

from .models import (
    Competition, CompetitionRegistration, CompetitionGroup, 
    CompetitionGroupMember, CompetitionMatch, CompetitionResult
)
from .serializers import (
    CompetitionSerializer, CompetitionRegistrationSerializer,
    CompetitionGroupSerializer, CompetitionMatchSerializer,
    CompetitionResultSerializer
)
# Student模型已整合到User模型中，通过user_type字段区分


class CompetitionViewSet(viewsets.ModelViewSet):
    """
    比赛管理视图集
    提供比赛的增删改查、报名、分组、排赛等功能
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """根据用户角色返回不同的比赛列表"""
        user = self.request.user
        if user.is_superuser or user.user_type == 'super_admin':
            return Competition.objects.all()
        elif user.user_type == 'campus_admin':
            # 校区管理员只能看到自己校区的比赛
            return Competition.objects.filter(campus=user.campus)
        else:
            # 学员和教练员只能看到所有比赛
            return Competition.objects.all()

    @action(detail=False, methods=['get'], url_path='my-registrations')
    def my_registrations(self, request):
        """
        获取当前用户的报名记录
        """
        user = request.user
        if user.user_type != 'student':
            return Response({'detail': '只有学员可以查看报名记录'}, status=status.HTTP_403_FORBIDDEN)
        
        registrations = CompetitionRegistration.objects.filter(
            participant=user
        ).select_related('competition')
        
        serializer = CompetitionRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        """
        学员报名参加比赛
        """
        competition = self.get_object()
        user = request.user
        
        # 检查用户是否为学员
        if user.user_type != 'student':
            return Response(
                {'error': '只有学员可以报名参加比赛'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 直接使用user对象，因为Student信息已整合到User模型中
        student = user
        
        # 检查比赛状态
        if competition.status != 'registration':
            return Response(
                {'error': '比赛不在报名阶段'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查报名截止时间
        if timezone.now() > competition.registration_end:
            return Response(
                {'error': '报名时间已截止'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查是否已经报名
        if CompetitionRegistration.objects.filter(
            competition=competition, participant=student
        ).exists():
            return Response(
                {'error': '您已经报名了这个比赛'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查报名人数限制
        current_registrations = CompetitionRegistration.objects.filter(
            competition=competition
        ).count()
        if current_registrations >= competition.max_participants_per_group:
            return Response(
                {'error': '报名人数已满'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建报名记录
        registration = CompetitionRegistration.objects.create(
            competition=competition,
            participant=student,
            group='A',  # 默认分配到甲组
            status='confirmed'
        )
        
        serializer = CompetitionRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def cancel_registration(self, request, pk=None):
        """
        取消比赛报名
        """
        competition = self.get_object()
        user = request.user
        
        if user.user_type != 'student':
            return Response(
                {'error': '只有学员可以取消报名'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            registration = CompetitionRegistration.objects.get(
                competition=competition, participant=user
            )
        except CompetitionRegistration.DoesNotExist:
            return Response(
                {'error': '未找到报名记录'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 检查是否可以取消报名
        if competition.status not in ['registration', 'preparation']:
            return Response(
                {'error': '比赛已开始，无法取消报名'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        registration.delete()
        return Response(
            {'message': '取消报名成功'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        """
        获取比赛报名列表
        """
        competition = self.get_object()
        registrations = CompetitionRegistration.objects.filter(
            competition=competition
        ).select_related('participant')
        
        serializer = CompetitionRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def create_groups(self, request, pk=None):
        """
        创建比赛分组
        只有管理员可以操作
        """
        competition = self.get_object()
        user = request.user
        
        if not (user.is_superuser or user.user_type in ['super_admin', 'campus_admin']):
            return Response(
                {'error': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if competition.status != 'registration':
            return Response(
                {'error': '只能在报名阶段创建分组'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取所有报名的学员
        registrations = CompetitionRegistration.objects.filter(
            competition=competition
        ).select_related('participant')
        
        if registrations.count() < 2:
            return Response(
                {'error': '报名人数不足，无法创建分组'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 删除已有的分组
        CompetitionGroup.objects.filter(competition=competition).delete()
        
        # 根据比赛类型创建分组
        participants = list(registrations)
        random.shuffle(participants)  # 随机打乱
        
        group_size = request.data.get('group_size', 4)  # 默认每组4人
        groups_created = []
        
        with transaction.atomic():
            group_number = 1
            for i in range(0, len(participants), group_size):
                group_participants = participants[i:i + group_size]
                
                # 创建分组
                group = CompetitionGroup.objects.create(
                    competition=competition,
                    group_name=f"第{group_number}组",
                    group_number=group_number
                )
                
                # 添加组员
                for registration in group_participants:
                    CompetitionGroupMember.objects.create(
                        group=group,
                        student=registration.student
                    )
                
                groups_created.append(group)
                group_number += 1
        
        # 更新比赛状态
        competition.status = 'preparation'
        competition.save()
        
        serializer = CompetitionGroupSerializer(groups_created, many=True)
        return Response({
            'message': f'成功创建{len(groups_created)}个分组',
            'groups': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def groups(self, request, pk=None):
        """
        获取比赛分组信息
        """
        competition = self.get_object()
        groups = CompetitionGroup.objects.filter(
            competition=competition
        ).prefetch_related('members__student__user')
        
        serializer = CompetitionGroupSerializer(groups, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def generate_matches(self, request, pk=None):
        """
        生成比赛对阵
        """
        competition = self.get_object()
        user = request.user
        
        if not (user.is_superuser or user.user_type in ['super_admin', 'campus_admin']):
            return Response(
                {'error': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if competition.status != 'preparation':
            return Response(
                {'error': '请先完成分组'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 删除已有的比赛对阵
        CompetitionMatch.objects.filter(competition=competition).delete()
        
        groups = CompetitionGroup.objects.filter(
            competition=competition
        ).prefetch_related('members__student')
        
        matches_created = []
        
        with transaction.atomic():
            match_number = 1
            
            for group in groups:
                members = list(group.members.all())
                
                # 生成组内循环赛
                for i in range(len(members)):
                    for j in range(i + 1, len(members)):
                        match = CompetitionMatch.objects.create(
                            competition=competition,
                            group=group,
                            player1=members[i].student,
                            player2=members[j].student,
                            match_number=match_number,
                            round_number=1,
                            scheduled_time=competition.start_date + timedelta(hours=match_number)
                        )
                        matches_created.append(match)
                        match_number += 1
        
        # 更新比赛状态
        competition.status = 'in_progress'
        competition.save()
        
        serializer = CompetitionMatchSerializer(matches_created, many=True)
        return Response({
            'message': f'成功生成{len(matches_created)}场比赛',
            'matches': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        """
        获取比赛对阵信息
        """
        competition = self.get_object()
        matches = CompetitionMatch.objects.filter(
            competition=competition
        ).select_related(
            'player1', 'player2', 'group'
        ).order_by('round_number', 'id')
        
        serializer = CompetitionMatchSerializer(matches, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """
        获取比赛结果
        """
        competition = self.get_object()
        results = CompetitionResult.objects.filter(
            match__competition=competition
        ).select_related(
            'match__player1__user', 'match__player2__user'
        ).order_by('match__match_number')
        
        serializer = CompetitionResultSerializer(results, many=True)
        return Response(serializer.data)


class CompetitionMatchViewSet(viewsets.ModelViewSet):
    """
    比赛对阵管理视图集
    """
    queryset = CompetitionMatch.objects.all()
    serializer_class = CompetitionMatchSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def record_result(self, request, pk=None):
        """
        记录比赛结果
        """
        match = self.get_object()
        user = request.user
        
        # 检查权限
        if not (user.is_superuser or user.user_type in ['super_admin', 'campus_admin', 'coach']):
            return Response(
                {'error': '权限不足'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 检查比赛状态
        if match.status != 'scheduled':
            return Response(
                {'error': '比赛状态不正确'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取比赛结果数据
        player1_score = request.data.get('player1_score')
        player2_score = request.data.get('player2_score')
        
        if player1_score is None or player2_score is None:
            return Response(
                {'error': '请提供完整的比分'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 确定获胜者
        if player1_score > player2_score:
            winner = match.player1
        elif player2_score > player1_score:
            winner = match.player2
        else:
            winner = None  # 平局
        
        with transaction.atomic():
            # 创建比赛结果
            result = CompetitionResult.objects.create(
                match=match,
                player1_score=player1_score,
                player2_score=player2_score,
                winner=winner,
                recorded_by=user
            )
            
            # 更新比赛状态
            match.status = 'completed'
            match.actual_start_time = timezone.now()
            match.actual_end_time = timezone.now()
            match.save()
        
        serializer = CompetitionResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
