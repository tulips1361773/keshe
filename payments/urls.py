from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # 支付管理API
    path('api/create/', views.payment_create, name='api_payment_create'),
    path('api/list/', views.payment_list, name='api_payment_list'),
    path('api/<str:payment_id>/', views.payment_detail, name='api_payment_detail'),
    path('api/<str:payment_id>/confirm/', views.payment_confirm, name='api_payment_confirm'),
    
    # 退款管理API
    path('api/refund/create/', views.refund_create, name='api_refund_create'),
    path('api/refund/list/', views.refund_list, name='api_refund_list'),
    path('api/refund/<str:refund_id>/', views.refund_detail, name='api_refund_detail'),
    path('api/refund/<str:refund_id>/approve/', views.refund_approve, name='api_refund_approve'),
    
    # 用户账户API
    path('api/account/', views.user_account, name='api_user_account'),
    path('api/account/recharge/', views.account_recharge, name='api_account_recharge'),
    path('api/account/transactions/', views.account_transactions, name='api_account_transactions'),
    
    # 发票管理API
    path('api/invoice/create/', views.invoice_create, name='api_invoice_create'),
    path('api/invoice/list/', views.invoice_list, name='api_invoice_list'),
    path('api/invoice/<str:invoice_number>/', views.invoice_detail, name='api_invoice_detail'),
    
    # 支付方式API
    path('api/methods/', views.payment_methods, name='api_payment_methods'),
]