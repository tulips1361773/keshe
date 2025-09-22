from rest_framework import serializers
from .models import (
    Competition, CompetitionRegistration, CompetitionGroup,
    CompetitionGroupMember, CompetitionMatch, CompetitionResult
)
from accounts.serializers import UserSerializer
from campus.serializers import CampusSerializer


class CompetitionSerializer(serializers.ModelSerializer):
    """
    比赛序列化器
    """
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    registration_count = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    competition_type_display = serializers.CharField(source='get_competition_type_display', read_only=True)
    
    class Meta:
        model = Competition
        fields = [
            'id', 'name', 'title', 'competition_type', 'competition_type_display', 
            'description', 'campus', 'campus_name', 'competition_date',
            'registration_start', 'registration_end', 'registration_fee',
            'max_participants_per_group', 'status', 'status_display',
            'created_by', 'created_by_name', 'created_at', 'updated_at', 'registration_count'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def get_registration_count(self, obj):
        """获取报名人数"""
        return obj.registrations.count()
    
    def create(self, validated_data):
        """创建比赛时自动设置创建者"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class CompetitionRegistrationSerializer(serializers.ModelSerializer):
    """
    比赛报名序列化器
    """
    student_name = serializers.CharField(source='participant.username', read_only=True)
    student_real_name = serializers.CharField(source='participant.real_name', read_only=True)
    student_phone = serializers.CharField(source='participant.phone', read_only=True)
    competition_name = serializers.CharField(source='competition.title', read_only=True)
    
    class Meta:
        model = CompetitionRegistration
        fields = [
            'id', 'competition', 'competition_name', 'participant', 'student_name',
            'student_real_name', 'student_phone', 'group', 'status', 'registration_time',
            'notes'
        ]
        read_only_fields = ['registration_time', 'payment_time']


class CompetitionGroupMemberSerializer(serializers.ModelSerializer):
    """
    比赛分组成员序列化器
    """
    student_name = serializers.CharField(source='student.username', read_only=True)
    student_real_name = serializers.CharField(source='student.real_name', read_only=True)
    
    class Meta:
        model = CompetitionGroupMember
        fields = [
            'id', 'student', 'student_name', 'student_real_name', 'joined_at'
        ]


class CompetitionGroupSerializer(serializers.ModelSerializer):
    """
    比赛分组序列化器
    """
    members = CompetitionGroupMemberSerializer(many=True, read_only=True)
    competition_name = serializers.CharField(source='competition.title', read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CompetitionGroup
        fields = [
            'id', 'competition', 'competition_name', 'group_name', 'group_number',
            'members', 'member_count', 'created_at'
        ]
    
    def get_member_count(self, obj):
        """获取组员数量"""
        return obj.members.count()


class CompetitionMatchSerializer(serializers.ModelSerializer):
    """
    比赛对阵序列化器
    """
    player1_name = serializers.CharField(source='player1.username', read_only=True)
    player1_real_name = serializers.CharField(source='player1.real_name', read_only=True)
    player2_name = serializers.CharField(source='player2.username', read_only=True)
    player2_real_name = serializers.CharField(source='player2.real_name', read_only=True)
    competition_name = serializers.CharField(source='competition.name', read_only=True)
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    winner_name = serializers.CharField(source='winner.user.username', read_only=True)
    
    class Meta:
        model = CompetitionMatch
        fields = [
            'id', 'competition', 'competition_name', 'group', 'group_name',
            'player1', 'player1_name', 'player1_real_name',
            'player2', 'player2_name', 'player2_real_name',
            'round_number', 'scheduled_time',
            'actual_start_time', 'actual_end_time', 'table_number',
            'status', 'status_display', 'winner', 'winner_name', 'notes'
        ]
        read_only_fields = ['actual_start_time', 'actual_end_time', 'winner']


class CompetitionResultSerializer(serializers.ModelSerializer):
    """
    比赛结果序列化器
    """
    match_info = CompetitionMatchSerializer(source='match', read_only=True)
    recorded_by_name = serializers.CharField(source='recorded_by.username', read_only=True)
    winner_name = serializers.CharField(source='winner.user.username', read_only=True)
    
    class Meta:
        model = CompetitionResult
        fields = [
            'id', 'match', 'match_info', 'player1_score', 'player2_score',
            'winner', 'winner_name', 'recorded_by', 'recorded_by_name',
            'recorded_at', 'notes'
        ]
        read_only_fields = ['recorded_by', 'recorded_at']
    
    def create(self, validated_data):
        """创建比赛结果时自动设置记录者"""
        validated_data['recorded_by'] = self.context['request'].user
        return super().create(validated_data)


class CompetitionListSerializer(serializers.ModelSerializer):
    """
    比赛列表序列化器（简化版）
    """
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    registration_count = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    competition_type_display = serializers.CharField(source='get_competition_type_display', read_only=True)
    
    class Meta:
        model = Competition
        fields = [
            'id', 'name', 'competition_type', 'competition_type_display',
            'campus_name', 'start_date', 'registration_deadline',
            'max_participants', 'registration_fee', 'status', 'status_display',
            'registration_count', 'is_active'
        ]
    
    def get_registration_count(self, obj):
        """获取报名人数"""
        return obj.registrations.count()


class CompetitionStatsSerializer(serializers.Serializer):
    """
    比赛统计序列化器
    """
    total_competitions = serializers.IntegerField()
    active_competitions = serializers.IntegerField()
    completed_competitions = serializers.IntegerField()
    total_participants = serializers.IntegerField()
    total_matches = serializers.IntegerField()
    completed_matches = serializers.IntegerField()