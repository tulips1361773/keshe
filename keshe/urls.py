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

urlpatterns = [
    # Django admin站点
    path('admin/', admin.site.urls),
    
    # API路由
    path('api/accounts/', include('accounts.urls')),
    path('api/campus/', include('campus.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/payments/', include(('payments.urls', 'payments_api'), namespace='payments_api')),
    path('api/reservations/', include('reservations.urls')),
    path('api/notifications/', include('notifications.urls')),
    
    # 管理员页面路由
    path('payments/', include('payments.urls')),
    
    path('', include('competitions.urls'))
    
    # 根路径重定向到管理后台
    # path('', RedirectView.as_view(url='/admin/', permanent=False)),
]

# 开发环境下的静态文件和媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
