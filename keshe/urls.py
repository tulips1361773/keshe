"""
URL configuration for keshe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import JsonResponse

def api_root(request):
    """API根路径，返回API信息"""
    return JsonResponse({
        'message': '乒乓球训练管理系统 API',
        'version': '1.0',
        'frontend_url': 'http://localhost:3001',
        'admin_url': '/admin/',
        'available_apis': {
            'accounts': '/api/accounts/',
            'campus': '/api/campus/',
            'courses': '/api/courses/',
            'payments': '/api/payments/',
            'reservations': '/api/reservations/',
            'notifications': '/api/notifications/',
            'competitions': '/api/competitions/',
            'logs': '/api/logs/'
        }
    })

urlpatterns = [
    # 根路径 - API信息页面
    path('', api_root, name='api_root'),
    
    # Django admin站点
    path('admin/', admin.site.urls),
    
    # API路由
    path('api/accounts/', include('accounts.urls')),
    path('api/campus/', include('campus.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/payments/', include(('payments.urls', 'payments_api'), namespace='payments_api')),
    path('api/reservations/', include('reservations.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/logs/', include('logs.urls')),
    
    # 管理员页面路由
    path('payments/', include('payments.urls')),
    
    # 比赛相关路由
    path('', include('competitions.urls')),
]

# 开发环境下的静态文件和媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
