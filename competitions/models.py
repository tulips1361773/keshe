from django.db import models
from django.contrib.auth import get_user_model
from campus.models import Campus
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.models import User

class Competition(models.Model):
    """
    比赛信息模型
    """
    COMPETITION_STATUS_CHOICES = [
        ('upcoming', '即将开始'),
        ('registration', '报名中'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    COMPETITION_TYPE_CHOICES = [
        ('monthly', '月赛'),
        ('single', '单打'),
        ('double', '双打'),
        ('team', '团体赛'),
    ]
    
    GROUP_CHOICES = [
        ('A', '甲组'),
        ('B', '乙组'),
        ('C', '丙组'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='比赛名称', default='默认比赛')
    title = models.CharField(max_length=200, verbose_name='比赛标题')
    competition_type = models.CharField(
        max_length=20,
        choices=COMPETITION_TYPE_CHOICES,
        default='monthly',
        verbose_name='比赛类型'
    )
    description = models.TextField(blank=True, verbose_name='比赛描述')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, verbose_name='举办校区')
    competition_date = models.DateTimeField(verbose_name='比赛时间')
    registration_start = models.DateTimeField(verbose_name='报名开始时间')
    registration_end = models.DateTimeField(verbose_name='报名截止时间')
    registration_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=30.00,
        validators=[MinValueValidator(0)],
        verbose_name='报名费用'
    )
    max_participants_per_group = models.IntegerField(
        default=20,
        validators=[MinValueValidator(1)],
        verbose_name='每组最大参赛人数'
    )
    status = models.CharField(
        max_length=20,
        choices=COMPETITION_STATUS_CHOICES,
        default='upcoming',
        verbose_name='比赛状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_competitions',
        verbose_name='创建者'
    )
    
    class Meta:
        verbose_name = '比赛'
        verbose_name_plural = '比赛'
        ordering = ['-competition_date']
    
    def __str__(self):
        return f"{self.title} - {self.campus.name}"
    
    @property
    def is_registration_open(self):
        """检查是否在报名期间"""
        now = timezone.now()
        return self.registration_start <= now <= self.registration_end
    
    @property
    def total_registrations(self):
        """获取总报名人数"""
        return self.registrations.filter(status='confirmed').count()
    
    def get_group_registrations(self, group):
        """获取指定组别的报名人数"""
        return self.registrations.filter(group=group, status='confirmed').count()


class CompetitionRegistration(models.Model):
    """
    比赛报名模型
    """
    REGISTRATION_STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('cancelled', '已取消'),
        ('rejected', '已拒绝'),
    ]
    
    GROUP_CHOICES = [
        ('A', '甲组'),
        ('B', '乙组'),
        ('C', '丙组'),
    ]
    
    competition = models.ForeignKey(
        Competition, 
        on_delete=models.CASCADE, 
        related_name='registrations',
        verbose_name='比赛'
    )
    participant = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'user_type': 'student'},
        related_name='competition_registrations',
        verbose_name='参赛者'
    )
    group = models.CharField(
        max_length=1,
        choices=GROUP_CHOICES,
        verbose_name='参赛组别'
    )
    status = models.CharField(
        max_length=20,
        choices=REGISTRATION_STATUS_CHOICES,
        default='pending',
        verbose_name='报名状态'
    )
    registration_time = models.DateTimeField(auto_now_add=True, verbose_name='报名时间')
    payment_status = models.BooleanField(default=False, verbose_name='缴费状态')
    notes = models.TextField(blank=True, verbose_name='备注')
    
    class Meta:
        verbose_name = '比赛报名'
        verbose_name_plural = '比赛报名'
        unique_together = ['competition', 'participant']  # 每个比赛每人只能报名一次
        ordering = ['-registration_time']
    
    def __str__(self):
        return f"{self.participant.username} - {self.competition.title} ({self.group}组)"


class CompetitionGroup(models.Model):
    """
    比赛分组模型
    """
    competition = models.ForeignKey(
        Competition, 
        on_delete=models.CASCADE, 
        related_name='groups',
        verbose_name='比赛'
    )
    group_name = models.CharField(max_length=50, verbose_name='分组名称')
    group_type = models.CharField(
        max_length=1,
        choices=Competition.GROUP_CHOICES,
        verbose_name='组别类型'
    )
    participants = models.ManyToManyField(
        User, 
        through='CompetitionGroupMember',
        verbose_name='参赛者'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '比赛分组'
        verbose_name_plural = '比赛分组'
        unique_together = ['competition', 'group_name']
    
    def __str__(self):
        return f"{self.competition.title} - {self.group_name}"


class CompetitionGroupMember(models.Model):
    """
    比赛分组成员模型
    """
    group = models.ForeignKey(
        CompetitionGroup, 
        on_delete=models.CASCADE,
        verbose_name='分组'
    )
    participant = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='参赛者'
    )
    seed_number = models.IntegerField(
        null=True, 
        blank=True,
        verbose_name='种子号'
    )
    
    class Meta:
        verbose_name = '分组成员'
        verbose_name_plural = '分组成员'
        unique_together = ['group', 'participant']
    
    def __str__(self):
        return f"{self.group.group_name} - {self.participant.username}"


class CompetitionMatch(models.Model):
    """
    比赛对战模型
    """
    MATCH_STATUS_CHOICES = [
        ('scheduled', '已安排'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    MATCH_TYPE_CHOICES = [
        ('group_stage', '小组赛'),
        ('knockout', '淘汰赛'),
        ('final', '决赛'),
    ]
    
    competition = models.ForeignKey(
        Competition, 
        on_delete=models.CASCADE, 
        related_name='matches',
        verbose_name='比赛'
    )
    group = models.ForeignKey(
        CompetitionGroup, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name='分组'
    )
    player1 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='matches_as_player1',
        verbose_name='选手1'
    )
    player2 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='matches_as_player2',
        verbose_name='选手2'
    )
    match_type = models.CharField(
        max_length=20,
        choices=MATCH_TYPE_CHOICES,
        default='group_stage',
        verbose_name='比赛类型'
    )
    round_number = models.IntegerField(default=1, verbose_name='轮次')
    table_number = models.IntegerField(null=True, blank=True, verbose_name='球台号')
    scheduled_time = models.DateTimeField(null=True, blank=True, verbose_name='预定时间')
    actual_start_time = models.DateTimeField(null=True, blank=True, verbose_name='实际开始时间')
    actual_end_time = models.DateTimeField(null=True, blank=True, verbose_name='实际结束时间')
    
    # 比分记录
    player1_score = models.IntegerField(default=0, verbose_name='选手1得分')
    player2_score = models.IntegerField(default=0, verbose_name='选手2得分')
    winner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='won_matches',
        verbose_name='获胜者'
    )
    
    status = models.CharField(
        max_length=20,
        choices=MATCH_STATUS_CHOICES,
        default='scheduled',
        verbose_name='比赛状态'
    )
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '比赛对战'
        verbose_name_plural = '比赛对战'
        ordering = ['scheduled_time', 'round_number']
    
    def __str__(self):
        return f"{self.player1.username} vs {self.player2.username} - {self.competition.title}"
    
    @property
    def duration(self):
        """获取比赛时长"""
        if self.actual_start_time and self.actual_end_time:
            return self.actual_end_time - self.actual_start_time
        return None


class CompetitionResult(models.Model):
    """
    比赛结果统计模型
    """
    competition = models.ForeignKey(
        Competition, 
        on_delete=models.CASCADE, 
        related_name='results',
        verbose_name='比赛'
    )
    participant = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='competition_results',
        verbose_name='参赛者'
    )
    group = models.CharField(
        max_length=1,
        choices=Competition.GROUP_CHOICES,
        verbose_name='参赛组别'
    )
    
    # 统计数据
    matches_played = models.IntegerField(default=0, verbose_name='比赛场次')
    matches_won = models.IntegerField(default=0, verbose_name='获胜场次')
    matches_lost = models.IntegerField(default=0, verbose_name='失败场次')
    total_score_for = models.IntegerField(default=0, verbose_name='总得分')
    total_score_against = models.IntegerField(default=0, verbose_name='总失分')
    
    # 排名
    group_rank = models.IntegerField(null=True, blank=True, verbose_name='组内排名')
    overall_rank = models.IntegerField(null=True, blank=True, verbose_name='总排名')
    
    # 奖项
    award = models.CharField(max_length=100, blank=True, verbose_name='获得奖项')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '比赛结果'
        verbose_name_plural = '比赛结果'
        unique_together = ['competition', 'participant']
        ordering = ['group', 'group_rank']
    
    def __str__(self):
        return f"{self.participant.username} - {self.competition.title} ({self.group}组)"
    
    @property
    def win_rate(self):
        """获胜率"""
        if self.matches_played == 0:
            return 0
        return round((self.matches_won / self.matches_played) * 100, 2)
    
    @property
    def score_difference(self):
        """净胜分"""
        return self.total_score_for - self.total_score_against
