from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建路由器
router = DefaultRouter()
router.register(r'competitions', views.CompetitionViewSet)
router.register(r'matches', views.CompetitionMatchViewSet)

app_name = 'competitions'

urlpatterns = [
    # API路由
    path('api/', include(router.urls)),
    
    # 自定义API端点
    path('api/competitions/<int:pk>/register/', 
         views.CompetitionViewSet.as_view({'post': 'register'}), 
         name='competition-register'),
    
    path('api/competitions/<int:pk>/cancel-registration/', 
         views.CompetitionViewSet.as_view({'post': 'cancel_registration'}), 
         name='competition-cancel-registration'),
    
    path('api/competitions/<int:pk>/registrations/', 
         views.CompetitionViewSet.as_view({'get': 'registrations'}), 
         name='competition-registrations'),
    
    path('api/competitions/<int:pk>/create-groups/', 
         views.CompetitionViewSet.as_view({'post': 'create_groups'}), 
         name='competition-create-groups'),
    
    path('api/competitions/<int:pk>/groups/', 
         views.CompetitionViewSet.as_view({'get': 'groups'}), 
         name='competition-groups'),
    
    path('api/competitions/<int:pk>/generate-matches/', 
         views.CompetitionViewSet.as_view({'post': 'generate_matches'}), 
         name='competition-generate-matches'),
    
    path('api/competitions/<int:pk>/matches/', 
         views.CompetitionViewSet.as_view({'get': 'matches'}), 
         name='competition-matches'),
    
    path('api/competitions/<int:pk>/results/', 
         views.CompetitionViewSet.as_view({'get': 'results'}), 
         name='competition-results'),
    
    path('api/matches/<int:pk>/record-result/', 
         views.CompetitionMatchViewSet.as_view({'post': 'record_result'}), 
         name='match-record-result'),
]