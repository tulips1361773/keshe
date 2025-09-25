from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
import random
from logs.utils import log_user_action
from logs.decorators import log_user_operation

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

    def create(self, request, *args, **kwargs):
        """创建比赛"""
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            # 记录创建比赛的日志
            competition = Competition.objects.get(id=response.data['id'])
            log_user_action(
                user=request.user,
                action_type='create',
                resource_type='competition',
                resource_id=competition.id,
                description=f'创建比赛: {competition.title}',
                request=request
            )
        return response

    def update(self, request, *args, **kwargs):
        """更新比赛"""
        competition = self.get_object()
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            # 记录更新比赛的日志
            log_user_action(
                user=request.user,
                action_type='update',
                resource_type='competition',
                resource_id=competition.id,
                description=f'更新比赛: {competition.title}',
                request=request
            )
        return response

    def destroy(self, request, *args, **kwargs):
        """删除比赛"""
        competition = self.get_object()
        competition_title = competition.title
        competition_id = competition.id
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            # 记录删除比赛的日志
            log_user_action(
                user=request.user,
                action_type='delete',
                resource_type='competition',
                resource_id=competition_id,
                description=f'删除比赛: {competition_title}',
                request=request
            )
        return response

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
        from payments.models import UserAccount, AccountTransaction
        from decimal import Decimal
        
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
        
        # 检查用户账户余额
        try:
            student_account = UserAccount.objects.get(user=student)
        except UserAccount.DoesNotExist:
            # 如果用户没有账户，创建一个余额为0的账户
            student_account = UserAccount.objects.create(
                user=student,
                balance=Decimal('0.00')
            )
        
        # 检查余额是否足够支付报名费
        registration_fee = competition.registration_fee
        if student_account.available_balance < registration_fee:
            return Response({
                'error': f'账户余额不足。当前可用余额：¥{student_account.available_balance:.2f}，报名费：¥{registration_fee:.2f}。请先充值。',
                'current_balance': float(student_account.available_balance),
                'required_amount': float(registration_fee),
                'need_recharge': True
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 扣除报名费
        student_account.balance -= registration_fee
        student_account.save()
        
        # 创建交易记录
        AccountTransaction.objects.create(
            account=student_account,
            transaction_type='payment',
            amount=registration_fee,
            balance_before=student_account.balance + registration_fee,
            balance_after=student_account.balance,
            description=f'比赛报名费 - {competition.name}（{competition.title}）'
        )
        
        # 创建报名记录
        registration = CompetitionRegistration.objects.create(
            competition=competition,
            participant=student,
            group='A',  # 默认分配到甲组
            status='confirmed',
            payment_status=True  # 标记为已缴费
        )
        
        serializer = CompetitionRegistrationSerializer(registration)
        return Response({
            'message': f'报名成功！已扣除报名费¥{registration_fee:.2f}',
            'registration': serializer.data,
            'remaining_balance': float(student_account.balance)
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def cancel_registration(self, request, pk=None):
        """
        取消比赛报名
        """
        from payments.models import UserAccount, AccountTransaction
        from decimal import Decimal
        
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
        if competition.status not in ['registration', 'upcoming']:
            return Response(
                {'error': '比赛已开始，无法取消报名'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 处理退费逻辑
        refund_amount = Decimal('0.00')
        if registration.payment_status:
            # 获取用户账户
            try:
                student_account = UserAccount.objects.get(user=user)
                
                # 计算退费金额（可以根据取消时间设置不同的退费比例）
                now = timezone.now()
                if now <= competition.registration_end:
                    # 报名期内取消，全额退费
                    refund_amount = competition.registration_fee
                elif now <= competition.competition_date - timedelta(days=1):
                    # 比赛前一天取消，退费80%
                    refund_amount = competition.registration_fee * Decimal('0.8')
                else:
                    # 比赛当天取消，不退费
                    refund_amount = Decimal('0.00')
                
                if refund_amount > 0:
                    # 退费到账户
                    student_account.balance += refund_amount
                    student_account.save()
                    
                    # 创建退费交易记录
                    AccountTransaction.objects.create(
                        account=student_account,
                        transaction_type='refund',
                        amount=refund_amount,
                        balance_before=student_account.balance - refund_amount,
                        balance_after=student_account.balance,
                        description=f'比赛报名费退费 - {competition.name}（{competition.title}）'
                    )
                    
            except UserAccount.DoesNotExist:
                # 如果没有账户，不处理退费
                pass
        
        registration.delete()
        
        if refund_amount > 0:
            return Response({
                'message': f'取消报名成功，已退费¥{refund_amount:.2f}',
                'refund_amount': float(refund_amount)
            }, status=status.HTTP_200_OK)
        else:
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
        管理员和比赛创建者（教练）可以操作
        """
        competition = self.get_object()
        user = request.user
        
        # 检查权限：管理员或比赛创建者
        if not (user.is_superuser or 
                user.user_type in ['super_admin', 'campus_admin'] or
                (user.user_type == 'coach' and competition.created_by == user)):
            return Response(
                {'error': '权限不足，只有管理员或比赛创建者可以创建分组'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if competition.status not in ['registration', 'preparation']:
            return Response(
                {'error': '只能在报名阶段或准备阶段创建分组'},
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
                    group_type='A'  # 默认设置为A组，可以根据需要调整
                )
                
                # 添加组员
                for registration in group_participants:
                    CompetitionGroupMember.objects.create(
                        group=group,
                        participant=registration.participant
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
        ).prefetch_related('competitiongroupmember_set__participant')
        
        serializer = CompetitionGroupSerializer(groups, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def generate_matches(self, request, pk=None):
        """
        生成比赛对阵（支持全循环和小组循环+交叉淘汰）
        管理员和比赛创建者（教练）可以操作
        """
        competition = self.get_object()
        user = request.user
        
        # 检查权限：管理员或比赛创建者
        if not (user.is_superuser or 
                user.user_type in ['super_admin', 'campus_admin'] or
                (user.user_type == 'coach' and competition.created_by == user)):
            return Response(
                {'error': '权限不足，只有管理员或比赛创建者可以生成对阵'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if competition.status not in ['upcoming', 'registration', 'preparation']:
            return Response(
                {'error': '比赛状态不正确，无法生成对阵'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取比赛类型和对阵模式
        match_format = request.data.get('match_format', 'round_robin')  # round_robin 或 group_knockout
        
        # 删除已有的比赛对阵
        CompetitionMatch.objects.filter(competition=competition).delete()
        
        # 获取所有确认报名的参赛者
        registrations = CompetitionRegistration.objects.filter(
            competition=competition, 
            status='confirmed'
        ).select_related('participant')
        
        if registrations.count() < 2:
            return Response(
                {'error': '参赛人数不足，至少需要2人'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        matches_created = []
        
        with transaction.atomic():
            if match_format == 'round_robin':
                # 全循环赛制
                matches_created = self._generate_round_robin_matches(competition, registrations)
            elif match_format == 'group_knockout':
                # 小组循环+交叉淘汰赛制
                matches_created = self._generate_group_knockout_matches(competition, registrations)
            else:
                return Response(
                    {'error': '不支持的对阵模式'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # 更新比赛状态
        competition.status = 'in_progress'
        competition.save()
        
        serializer = CompetitionMatchSerializer(matches_created, many=True)
        return Response({
            'message': f'成功生成{len(matches_created)}场比赛',
            'match_format': match_format,
            'total_matches': len(matches_created),
            'matches': serializer.data
        })
    
    def _generate_round_robin_matches(self, competition, registrations):
        """生成全循环赛对阵"""
        participants = [reg.participant for reg in registrations]
        matches_created = []
        match_number = 1
        
        # 计算比赛开始时间
        start_time = competition.competition_date
        
        # 全循环：每个人都要和其他所有人比赛一场
        for i in range(len(participants)):
            for j in range(i + 1, len(participants)):
                # 计算球台号（假设有8个球台）
                table_number = ((match_number - 1) % 8) + 1
                
                # 计算比赛时间（每场比赛间隔30分钟）
                scheduled_time = start_time + timedelta(minutes=(match_number - 1) * 30)
                
                match = CompetitionMatch.objects.create(
                    competition=competition,
                    player1=participants[i],
                    player2=participants[j],
                    match_type='group_stage',
                    round_number=1,
                    table_number=table_number,
                    scheduled_time=scheduled_time,
                    status='scheduled'
                )
                matches_created.append(match)
                match_number += 1
        
        return matches_created
    
    def _generate_group_knockout_matches(self, competition, registrations):
        """生成小组循环+交叉淘汰赛对阵"""
        participants = [reg.participant for reg in registrations]
        matches_created = []
        
        # 分组（每组4-6人）
        group_size = min(6, max(4, len(participants) // 4))  # 动态调整组大小
        groups = []
        
        # 随机分组
        import random
        random.shuffle(participants)
        
        for i in range(0, len(participants), group_size):
            group = participants[i:i + group_size]
            if len(group) >= 2:  # 确保每组至少2人
                groups.append(group)
        
        # 如果最后一组人数太少，合并到前一组
        if len(groups) > 1 and len(groups[-1]) < 2:
            groups[-2].extend(groups[-1])
            groups.pop()
        
        match_number = 1
        start_time = competition.competition_date
        
        # 第一阶段：小组循环赛
        group_winners = []
        for group_idx, group in enumerate(groups):
            group_letter = chr(ord('A') + group_idx)
            
            # 组内循环赛
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    table_number = ((match_number - 1) % 8) + 1
                    scheduled_time = start_time + timedelta(minutes=(match_number - 1) * 30)
                    
                    match = CompetitionMatch.objects.create(
                        competition=competition,
                        player1=group[i],
                        player2=group[j],
                        match_type='group_stage',
                        round_number=1,
                        table_number=table_number,
                        scheduled_time=scheduled_time,
                        status='scheduled',
                        notes=f'小组{group_letter}循环赛'
                    )
                    matches_created.append(match)
                    match_number += 1
            
            # 记录每组的第一名（实际应该根据比赛结果确定）
            group_winners.append(group[0])  # 临时设置第一个为组内第一
        
        # 第二阶段：交叉淘汰赛（如果有多个组）
        if len(groups) > 1:
            knockout_participants = group_winners
            round_number = 2
            
            while len(knockout_participants) > 1:
                next_round = []
                
                # 配对进行淘汰赛
                for i in range(0, len(knockout_participants), 2):
                    if i + 1 < len(knockout_participants):
                        table_number = ((match_number - 1) % 8) + 1
                        scheduled_time = start_time + timedelta(minutes=(match_number - 1) * 30)
                        
                        match = CompetitionMatch.objects.create(
                            competition=competition,
                            player1=knockout_participants[i],
                            player2=knockout_participants[i + 1],
                            match_type='knockout' if round_number < len(groups) + 1 else 'final',
                            round_number=round_number,
                            table_number=table_number,
                            scheduled_time=scheduled_time,
                            status='scheduled',
                            notes=f'第{round_number}轮淘汰赛'
                        )
                        matches_created.append(match)
                        match_number += 1
                        
                        # 临时设置第一个选手晋级（实际应该根据比赛结果）
                        next_round.append(knockout_participants[i])
                    else:
                        # 奇数情况，直接晋级
                        next_round.append(knockout_participants[i])
                
                knockout_participants = next_round
                round_number += 1
        
        return matches_created
    
    @action(detail=True, methods=['get'])
    def my_matches(self, request, pk=None):
        """
        获取当前用户在该比赛中的对阵信息
        """
        competition = self.get_object()
        user = request.user
        
        if user.user_type != 'student':
            return Response(
                {'error': '只有学员可以查看个人比赛信息'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 检查用户是否报名了该比赛
        try:
            registration = CompetitionRegistration.objects.get(
                competition=competition,
                participant=user,
                status='confirmed'
            )
        except CompetitionRegistration.DoesNotExist:
            return Response(
                {'error': '您未报名该比赛'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 获取用户的所有比赛
        matches = CompetitionMatch.objects.filter(
            competition=competition
        ).filter(
            models.Q(player1=user) | models.Q(player2=user)
        ).select_related(
            'player1', 'player2', 'winner'
        ).order_by('round_number', 'scheduled_time')
        
        # 序列化比赛数据
        match_data = []
        for match in matches:
            opponent = match.player2 if match.player1 == user else match.player1
            is_player1 = match.player1 == user
            
            match_info = {
                'id': match.id,
                'opponent_name': opponent.username,
                'opponent_real_name': getattr(opponent, 'real_name', ''),
                'match_type': match.get_match_type_display(),
                'round_number': match.round_number,
                'table_number': match.table_number,
                'scheduled_time': match.scheduled_time,
                'status': match.get_status_display(),
                'my_score': match.player1_score if is_player1 else match.player2_score,
                'opponent_score': match.player2_score if is_player1 else match.player1_score,
                'result': None,
                'notes': match.notes
            }
            
            # 确定比赛结果
            if match.status == 'completed' and match.winner:
                if match.winner == user:
                    match_info['result'] = 'win'
                else:
                    match_info['result'] = 'loss'
            elif match.status == 'completed' and not match.winner:
                match_info['result'] = 'draw'
            
            match_data.append(match_info)
        
        return Response({
            'competition': {
                'id': competition.id,
                'name': competition.name,
                'title': competition.title,
                'status': competition.get_status_display()
            },
            'registration': {
                'group': registration.group,
                'registration_time': registration.created_at
            },
            'matches': match_data,
            'statistics': {
                'total_matches': len(match_data),
                'completed_matches': len([m for m in match_data if m['result'] is not None]),
                'wins': len([m for m in match_data if m['result'] == 'win']),
                'losses': len([m for m in match_data if m['result'] == 'loss']),
                'draws': len([m for m in match_data if m['result'] == 'draw'])
            }
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
        ).order_by('round_number', 'scheduled_time')
        
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
        ).order_by('match__round_number', 'match__scheduled_time')
        
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
