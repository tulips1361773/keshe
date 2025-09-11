from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # 课程管理API
    path('api/list/', views.course_list, name='api_course_list'),
    path('api/create/', views.course_create, name='api_course_create'),
    path('api/<int:course_id>/', views.course_detail, name='api_course_detail'),
    path('api/<int:course_id>/update/', views.course_update, name='api_course_update'),
    path('api/<int:course_id>/delete/', views.course_delete, name='api_course_delete'),
    
    # 课程报名API
    path('api/<int:course_id>/enroll/', views.course_enroll, name='api_course_enroll'),
    path('api/enrollments/', views.enrollment_list, name='api_enrollment_list'),
    path('api/enrollments/<int:enrollment_id>/cancel/', views.enrollment_cancel, name='api_enrollment_cancel'),
    
    # 课程时间表API
    path('api/<int:course_id>/schedules/', views.course_schedules, name='api_course_schedules'),
    path('api/schedules/create/', views.schedule_create, name='api_schedule_create'),
    
    # 课程课时API
    path('api/<int:course_id>/sessions/', views.course_sessions, name='api_course_sessions'),
    path('api/sessions/create/', views.session_create, name='api_session_create'),
    
    # 考勤管理API
    path('api/sessions/<int:session_id>/attendance/', views.session_attendance, name='api_session_attendance'),
    path('api/attendance/checkin/', views.attendance_checkin, name='api_attendance_checkin'),
    
    # 课程评价API
    path('api/<int:course_id>/evaluate/', views.course_evaluate, name='api_course_evaluate'),
    path('api/evaluations/', views.evaluation_list, name='api_evaluation_list'),
]