from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # 支付模块首页
    path('', views.payments_index, name='payments_index'),
    
    # 支付管理API
    path('api/create/', views.payment_create, name='api_payment_create'),
    path('api/list/', views.payment_list, name='api_payment_list'),
    
    # 用户账户API (必须在通用模式之前)
    path('api/account/', views.user_account, name='api_user_account'),
    path('api/account/recharge/', views.account_recharge, name='api_account_recharge'),
    path('api/account/transactions/', views.account_transactions, name='api_account_transactions'),
    
    # 退款管理API
    path('api/refund/create/', views.refund_create, name='api_refund_create'),
    path('api/refund/list/', views.refund_list, name='api_refund_list'),
    path('api/refund/<str:refund_id>/', views.refund_detail, name='api_refund_detail'),
    path('api/refund/<str:refund_id>/approve/', views.refund_approve, name='api_refund_approve'),
    
    # 发票管理API
    path('api/invoice/create/', views.invoice_create, name='api_invoice_create'),
    path('api/invoice/list/', views.invoice_list, name='api_invoice_list'),
    path('api/invoice/<str:invoice_number>/', views.invoice_detail, name='api_invoice_detail'),
    
    # 支付方式API
    path('api/methods/', views.payment_methods, name='api_payment_methods'),
    
    # 管理员API
    path('api/admin/offline-payment/', views.admin_offline_payment, name='api_admin_offline_payment'),
    path('api/admin/students/', views.admin_students_list, name='api_admin_students_list'),
    path('api/admin/pending-recharges/', views.admin_pending_recharges, name='api_admin_pending_recharges'),
    path('api/admin/recharge/<str:payment_id>/approve/', views.admin_recharge_approve, name='api_admin_recharge_approve'),
    
    # 支付详情API (通用模式，必须放在最后)
    path('api/<str:payment_id>/', views.payment_detail, name='api_payment_detail'),
    path('api/<str:payment_id>/confirm/', views.payment_confirm, name='api_payment_confirm'),
]