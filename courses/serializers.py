from rest_framework import serializers
from django.utils import timezone
from .models import (
    Course, CourseSchedule, CourseEnrollment, 
    CourseSession, CourseAttendance, CourseEvaluation
)
from accounts.models import User
from campus.models import Campus, CampusArea


class CourseSerializer(serializers.ModelSerializer):
    """课程序列化器"""
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    coach_name = serializers.CharField(source='coach.real_name', read_only=True)
    area_name = serializers.CharField(source='area.name', read_only=True)
    current_enrollments_count = serializers.ReadOnlyField()
    available_spots = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate(self, data):
        """验证课程数据"""
        # 验证日期
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] >= data['end_date']:
                raise serializers.ValidationError('结束日期必须晚于开始日期')
        
        # 验证教练是否属于该校区
        campus = data.get('campus')
        coach = data.get('coach')
        if campus and coach:
            from campus.models import CampusCoach
            if not CampusCoach.objects.filter(campus=campus, coach=coach, is_active=True).exists():
                raise serializers.ValidationError('该教练不属于此校区或未激活')
        
        # 验证区域是否属于该校区
        area = data.get('area')
        if campus and area:
            if area.campus != campus:
                raise serializers.ValidationError('该区域不属于此校区')
        
        return data


class CourseScheduleSerializer(serializers.ModelSerializer):
    """课程时间表序列化器"""
    course_name = serializers.CharField(source='course.name', read_only=True)
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    
    class Meta:
        model = CourseSchedule
        fields = '__all__'
    
    def validate(self, data):
        """验证时间表数据"""
        if data.get('start_time') and data.get('end_time'):
            if data['start_time'] >= data['end_time']:
                raise serializers.ValidationError('结束时间必须晚于开始时间')
        return data


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    """课程报名序列化器"""
    course_name = serializers.CharField(source='course.name', read_only=True)
    student_name = serializers.CharField(source='student.real_name', read_only=True)
    student_phone = serializers.CharField(source='student.phone', read_only=True)
    remaining_amount = serializers.ReadOnlyField()
    
    class Meta:
        model = CourseEnrollment
        fields = '__all__'
        read_only_fields = ('enrollment_date', 'created_at', 'updated_at')
    
    def validate(self, data):
        """验证报名数据"""
        course = data.get('course')
        student = data.get('student')
        
        # 检查课程是否已满
        if course and course.is_full:
            raise serializers.ValidationError('课程已满，无法报名')
        
        # 检查学员是否已报名
        if course and student:
            if CourseEnrollment.objects.filter(course=course, student=student).exists():
                raise serializers.ValidationError('学员已报名此课程')
        
        return data


class CourseSessionSerializer(serializers.ModelSerializer):
    """课程课时序列化器"""
    course_name = serializers.CharField(source='course.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = CourseSession
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CourseAttendanceSerializer(serializers.ModelSerializer):
    """课程考勤序列化器"""
    student_name = serializers.CharField(source='student.real_name', read_only=True)
    student_phone = serializers.CharField(source='student.phone', read_only=True)
    session_info = serializers.CharField(source='session.__str__', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = CourseAttendance
        fields = '__all__'
        read_only_fields = ('created_at',)


class CourseEvaluationSerializer(serializers.ModelSerializer):
    """课程评价序列化器"""
    course_name = serializers.CharField(source='course.name', read_only=True)
    student_name = serializers.CharField(source='student.real_name', read_only=True)
    
    class Meta:
        model = CourseEvaluation
        fields = '__all__'
        read_only_fields = ('created_at',)
    
    def validate(self, data):
        """验证评价数据"""
        course = data.get('course')
        student = data.get('student')
        
        # 检查学员是否已报名此课程
        if course and student:
            if not CourseEnrollment.objects.filter(
                course=course, 
                student=student, 
                status__in=['confirmed', 'completed']
            ).exists():
                raise serializers.ValidationError('只有已确认或已完成的课程才能评价')
        
        return data