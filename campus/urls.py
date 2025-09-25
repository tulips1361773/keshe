from django.urls import path
from . import views

app_name = 'campus'

urlpatterns = [
    # 校区管理API
    path('api/list/', views.campus_list, name='api_campus_list'),
    path('api/create/', views.campus_create, name='api_campus_create'),
    path('api/<int:campus_id>/', views.campus_detail, name='api_campus_detail'),
    path('api/<int:campus_id>/update/', views.campus_update, name='api_campus_update'),
    path('api/<int:campus_id>/delete/', views.campus_delete, name='api_campus_delete'),
    path('api/<int:campus_id>/assign-manager/', views.campus_assign_manager, name='api_campus_assign_manager'),
    path('api/available-managers/', views.available_managers, name='api_available_managers'),
    
    # 校区分区API
    path('api/<int:campus_id>/areas/', views.campus_areas, name='api_campus_areas'),
    path('api/<int:campus_id>/areas/create/', views.campus_area_create, name='api_campus_area_create'),
    path('api/<int:campus_id>/areas/<int:area_id>/update/', views.campus_area_update, name='api_campus_area_update'),
    path('api/<int:campus_id>/areas/<int:area_id>/delete/', views.campus_area_delete, name='api_campus_area_delete'),
    
    # 校区学员和教练管理API
    path('api/<int:campus_id>/students/', views.campus_students, name='api_campus_students'),
    path('api/<int:campus_id>/students/add/', views.campus_student_add, name='api_campus_student_add'),
    path('api/<int:campus_id>/coaches/', views.campus_coaches, name='api_campus_coaches'),
    path('api/<int:campus_id>/coaches/add/', views.campus_coach_add, name='api_campus_coach_add'),
]