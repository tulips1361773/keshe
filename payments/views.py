from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from django.core.paginator import Paginator
from .models import Payment, PaymentMethod, UserAccount, AccountTransaction, Refund, Invoice
from .serializers import PaymentSerializer, PaymentMethodSerializer, UserAccountSerializer, AccountTransactionSerializer, RefundSerializer, InvoiceSerializer
from courses.models import CourseEnrollment
from accounts.models import User

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_create(request):
    """创建支付API"""
    try:
        data = request.data
        enrollment_id = data.get('enrollment_id')
        payment_type = data.get('payment_type', 'course_fee')
        amount = Decimal(str(data.get('amount', 0)))
        payment_method_id = data.get('payment_method_id')
        
        # 验证报名记录
        enrollment = None
        if enrollment_id:
            enrollment = get_object_or_404(CourseEnrollment, id=enrollment_id, student=request.user)
        
        # 验证支付方式
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id, is_active=True)
        
        # 创建支付记录
        payment = Payment.objects.create(
            user=request.user,
            enrollment=enrollment,
            payment_type=payment_type,
            amount=amount,
            payment_method=payment_method,
            description=data.get('description', '')
        )
        
        serializer = PaymentSerializer(payment)
        return Response({
            'code': 200,
            'message': '支付订单创建成功',
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'创建支付失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_list(request):
    """支付列表API"""
    try:
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')
        
        # 筛选条件
        payment_type = request.GET.get('payment_type')
        payment_status = request.GET.get('status')
        
        if payment_type:
            payments = payments.filter(payment_type=payment_type)
        if payment_status:
            payments = payments.filter(status=payment_status)
        
        # 分页
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        paginator = Paginator(payments, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = PaymentSerializer(page_obj.object_list, many=True)
        
        return Response({
            'code': 200,
            'message': '获取支付列表成功',
            'data': {
                'results': serializer.data,
                'count': paginator.count,
                'page': page,
                'page_size': page_size,
                'total_pages': paginator.num_pages
            }
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取支付列表失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_detail(request, payment_id):
    """支付详情API"""
    try:
        payment = get_object_or_404(Payment, payment_id=payment_id, user=request.user)
        serializer = PaymentSerializer(payment)
        
        return Response({
            'code': 200,
            'message': '获取支付详情成功',
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取支付详情失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_confirm(request, payment_id):
    """确认支付API"""
    try:
        with transaction.atomic():
            payment = get_object_or_404(Payment, payment_id=payment_id, user=request.user)
            
            if payment.status != 'pending':
                return Response({
                    'code': 400,
                    'message': '支付状态不允许确认'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 更新支付状态
            payment.status = 'completed'
            payment.paid_at = timezone.now()
            payment.transaction_id = request.data.get('transaction_id', '')
            payment.save()
            
            # 如果是课程费用，更新报名状态
            if payment.enrollment and payment.payment_type == 'course_fee':
                payment.enrollment.payment_status = 'paid'
                payment.enrollment.save()
            
            serializer = PaymentSerializer(payment)
            return Response({
                'code': 200,
                'message': '支付确认成功',
                'data': serializer.data
            })
            
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'支付确认失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refund_create(request):
    """创建退款API"""
    try:
        data = request.data
        payment_id = data.get('payment_id')
        refund_amount = Decimal(str(data.get('refund_amount', 0)))
        reason = data.get('reason', '')
        
        # 验证支付记录
        payment = get_object_or_404(Payment, payment_id=payment_id, user=request.user)
        
        if payment.status != 'completed':
            return Response({
                'code': 400,
                'message': '只能对已完成的支付申请退款'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if refund_amount > payment.amount:
            return Response({
                'code': 400,
                'message': '退款金额不能超过支付金额'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建退款记录
        refund = Refund.objects.create(
            payment=payment,
            refund_amount=refund_amount,
            reason=reason
        )
        
        serializer = RefundSerializer(refund)
        return Response({
            'code': 200,
            'message': '退款申请提交成功',
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'创建退款失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def refund_list(request):
    """退款列表API"""
    try:
        refunds = Refund.objects.filter(payment__user=request.user).order_by('-created_at')
        
        # 筛选条件
        refund_status = request.GET.get('status')
        if refund_status:
            refunds = refunds.filter(status=refund_status)
        
        # 分页
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        paginator = Paginator(refunds, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = RefundSerializer(page_obj.object_list, many=True)
        
        return Response({
            'code': 200,
            'message': '获取退款列表成功',
            'data': {
                'results': serializer.data,
                'count': paginator.count,
                'page': page,
                'page_size': page_size,
                'total_pages': paginator.num_pages
            }
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取退款列表失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def refund_detail(request, refund_id):
    """退款详情API"""
    try:
        refund = get_object_or_404(Refund, refund_id=refund_id, payment__user=request.user)
        serializer = RefundSerializer(refund)
        
        return Response({
            'code': 200,
            'message': '获取退款详情成功',
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取退款详情失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refund_approve(request, refund_id):
    """审批退款API"""
    try:
        # 只有管理员可以审批退款
        if not request.user.is_staff:
            return Response({
                'code': 403,
                'message': '权限不足，只有管理员可以审批退款'
            }, status=status.HTTP_403_FORBIDDEN)
        
        with transaction.atomic():
            refund = get_object_or_404(Refund, refund_id=refund_id)
            
            if refund.status != 'pending':
                return Response({
                    'code': 400,
                    'message': '退款状态不允许审批'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            approve = request.data.get('approve', False)
            
            if approve:
                refund.status = 'approved'
                refund.processed_at = timezone.now()
                # 这里应该调用实际的退款接口
            else:
                refund.status = 'rejected'
                refund.processed_at = timezone.now()
            
            refund.save()
            
            serializer = RefundSerializer(refund)
            return Response({
                'code': 200,
                'message': '退款审批成功',
                'data': serializer.data
            })
            
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'退款审批失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_account(request):
    """用户账户API"""
    try:
        account, created = UserAccount.objects.get_or_create(user=request.user)
        serializer = UserAccountSerializer(account)
        
        return Response(serializer.data)
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error in user_account: {error_detail}")
        return Response({
            'error': f'获取用户账户失败: {str(e)}',
            'detail': error_detail
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def account_recharge(request):
    """账户充值API"""
    try:
        from .serializers import RechargeSerializer
        
        serializer = RechargeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'code': 400,
                'message': '参数验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        amount = validated_data['amount']
        payment_method_id = validated_data['payment_method_id']
        description = validated_data.get('description', '账户充值')
        
        # 获取支付方式
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id, is_active=True)
        
        # 创建充值支付记录
        payment = Payment.objects.create(
            user=request.user,
            payment_type='recharge',
            amount=amount,
            payment_method=payment_method,
            description=description
        )
        
        payment_serializer = PaymentSerializer(payment)
        return Response({
            'code': 200,
            'message': '充值订单创建成功',
            'data': payment_serializer.data
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'账户充值失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account_transactions(request):
    """账户交易记录API"""
    try:
        account, created = UserAccount.objects.get_or_create(user=request.user)
        transactions = AccountTransaction.objects.filter(account=account).order_by('-created_at')
        
        # 筛选条件
        transaction_type = request.GET.get('transaction_type')
        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)
        
        # 分页
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        paginator = Paginator(transactions, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = AccountTransactionSerializer(page_obj.object_list, many=True)
        
        return Response({
            'code': 200,
            'message': '获取交易记录成功',
            'data': {
                'results': serializer.data,
                'count': paginator.count,
                'page': page,
                'page_size': page_size,
                'total_pages': paginator.num_pages
            }
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取交易记录失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invoice_create(request):
    """创建发票API"""
    try:
        data = request.data
        payment_id = data.get('payment_id')
        invoice_type = data.get('invoice_type', 'personal')
        title = data.get('title', '')
        tax_number = data.get('tax_number', '')
        
        # 验证支付记录
        payment = get_object_or_404(Payment, payment_id=payment_id, user=request.user)
        
        if payment.status != 'completed':
            return Response({
                'code': 400,
                'message': '只能为已完成的支付开具发票'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查是否已开具发票
        if Invoice.objects.filter(payment=payment).exists():
            return Response({
                'code': 400,
                'message': '该支付记录已开具发票'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建发票记录
        invoice = Invoice.objects.create(
            payment=payment,
            invoice_type=invoice_type,
            title=title,
            tax_number=tax_number,
            amount=payment.amount
        )
        
        serializer = InvoiceSerializer(invoice)
        return Response({
            'code': 200,
            'message': '发票申请提交成功',
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'创建发票失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def invoice_list(request):
    """发票列表API"""
    try:
        invoices = Invoice.objects.filter(payment__user=request.user).order_by('-created_at')
        
        # 筛选条件
        invoice_status = request.GET.get('status')
        if invoice_status:
            invoices = invoices.filter(status=invoice_status)
        
        # 分页
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        paginator = Paginator(invoices, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = InvoiceSerializer(page_obj.object_list, many=True)
        
        return Response({
            'code': 200,
            'message': '获取发票列表成功',
            'data': {
                'results': serializer.data,
                'count': paginator.count,
                'page': page,
                'page_size': page_size,
                'total_pages': paginator.num_pages
            }
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取发票列表失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def invoice_detail(request, invoice_number):
    """发票详情API"""
    try:
        invoice = get_object_or_404(Invoice, invoice_number=invoice_number, payment__user=request.user)
        serializer = InvoiceSerializer(invoice)
        
        return Response({
            'code': 200,
            'message': '获取发票详情成功',
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取发票详情失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_methods(request):
    """支付方式API"""
    try:
        methods = PaymentMethod.objects.filter(is_active=True).order_by('id')
        serializer = PaymentMethodSerializer(methods, many=True)
        
        return Response({
            'code': 200,
            'message': '获取支付方式成功',
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取支付方式失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_offline_payment(request):
    """校区管理员线下支付录入API"""
    try:
        # 验证管理员权限
        if request.user.user_type not in ['super_admin', 'campus_admin']:
            return Response({
                'code': 403,
                'message': '权限不足，只有校区管理员可以录入线下支付'
            }, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        student_id = data.get('student_id')
        amount = Decimal(str(data.get('amount', 0)))
        payment_type = data.get('payment_type', 'course_fee')
        description = data.get('description', '')
        enrollment_id = data.get('enrollment_id')
        
        # 验证学员
        student = get_object_or_404(User, id=student_id, user_type='student')
        
        # 验证报名记录（如果提供）
        enrollment = None
        if enrollment_id:
            enrollment = get_object_or_404(CourseEnrollment, id=enrollment_id, student=student)
        
        # 获取现金支付方式
        cash_method = PaymentMethod.objects.filter(method_type='cash', is_active=True).first()
        if not cash_method:
            return Response({
                'code': 400,
                'message': '现金支付方式未配置或已禁用'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            # 创建支付记录
            payment = Payment.objects.create(
                user=student,
                enrollment=enrollment,
                payment_type=payment_type,
                amount=amount,
                payment_method=cash_method,
                status='completed',  # 线下支付直接标记为已完成
                description=f'管理员线下录入: {description}',
                paid_at=timezone.now()
            )
            
            # 更新学员账户余额
            account, created = UserAccount.objects.get_or_create(
                user=student,
                defaults={'balance': Decimal('0.00')}
            )
            
            # 记录账户交易
            AccountTransaction.objects.create(
                account=account,
                transaction_type='recharge',
                amount=amount,
                balance_before=account.balance,
                balance_after=account.balance + amount,
                payment=payment,
                description=f'管理员线下充值录入: {description}'
            )
            
            # 更新账户余额
            account.balance += amount
            account.total_paid += amount
            account.save()
        
        serializer = PaymentSerializer(payment)
        return Response({
            'code': 200,
            'message': '线下支付录入成功',
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'线下支付录入失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_recharge_approve(request, payment_id):
    """管理员审核充值订单API"""
    try:
        # 验证管理员权限
        if request.user.user_type not in ['super_admin', 'campus_admin']:
            return Response({
                'code': 403,
                'message': '权限不足，只有管理员可以审核充值订单'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 获取充值订单
        payment = get_object_or_404(Payment, payment_id=payment_id, payment_type='recharge')
        
        if payment.status != 'pending':
            return Response({
                'code': 400,
                'message': '充值订单状态不允许审核'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        approve = request.data.get('approve', False)
        
        with transaction.atomic():
            if approve:
                # 审核通过
                payment.status = 'completed'
                payment.paid_at = timezone.now()
                payment.save()
                
                # 更新用户账户余额
                account, created = UserAccount.objects.get_or_create(
                    user=payment.user,
                    defaults={'balance': Decimal('0.00')}
                )
                
                # 记录账户交易
                AccountTransaction.objects.create(
                    account=account,
                    transaction_type='recharge',
                    amount=payment.amount,
                    balance_before=account.balance,
                    balance_after=account.balance + payment.amount,
                    payment=payment,
                    description=f'管理员审核通过充值: {payment.description}'
                )
                
                # 更新账户余额
                account.balance += payment.amount
                account.total_paid += payment.amount
                account.save()
                
                message = '充值订单审核通过，用户余额已更新'
            else:
                # 审核拒绝
                payment.status = 'failed'
                payment.paid_at = timezone.now()
                payment.save()
                
                message = '充值订单已拒绝'
        
        serializer = PaymentSerializer(payment)
        return Response({
            'code': 200,
            'message': message,
            'data': serializer.data
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'充值审核失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_pending_recharges(request):
    """获取待审核充值订单列表API"""
    try:
        # 验证管理员权限
        if request.user.user_type not in ['super_admin', 'campus_admin']:
            return Response({
                'code': 403,
                'message': '权限不足，只有管理员可以查看待审核充值订单'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 获取待审核的充值订单
        payments = Payment.objects.filter(
            payment_type='recharge',
            status='pending'
        ).select_related('user', 'payment_method').order_by('-created_at')
        
        # 分页
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        paginator = Paginator(payments, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = PaymentSerializer(page_obj.object_list, many=True)
        
        return Response({
            'code': 200,
            'message': '获取待审核充值订单成功',
            'data': {
                'results': serializer.data,
                'count': paginator.count,
                'page': page,
                'page_size': page_size,
                'total_pages': paginator.num_pages
            }
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取待审核充值订单失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_students_list(request):
    """获取学员列表供管理员选择"""
    try:
        # 验证管理员权限
        if request.user.user_type not in ['super_admin', 'campus_admin']:
            return Response({
                'code': 403,
                'message': '权限不足，只有校区管理员可以查看学员列表'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # 获取学员列表
        students = User.objects.filter(user_type='student', is_active=True)
        
        # 搜索功能
        search = request.GET.get('search', '').strip()
        if search:
            from django.db.models import Q
            students = students.filter(
                Q(username__icontains=search) | 
                Q(real_name__icontains=search) |
                Q(phone__icontains=search)
            )
        
        students = students.order_by('real_name')
        
        # 分页
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        paginator = Paginator(students, page_size)
        students_page = paginator.get_page(page)
        
        # 构造返回数据
        students_data = []
        for student in students_page:
            students_data.append({
                'id': student.id,
                'username': student.username,
                'real_name': student.real_name,
                'phone': student.phone,
                'email': student.email
            })
        
        return Response({
            'code': 200,
            'message': '获取学员列表成功',
            'data': {
                'students': students_data,
                'total': paginator.count,
                'page': page,
                'page_size': page_size,
                'total_pages': paginator.num_pages
            }
        })
        
    except Exception as e:
        return Response({
            'code': 400,
            'message': f'获取学员列表失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


def payments_index(request):
    """支付模块首页视图"""
    return render(request, 'payments/index.html', {
        'title': '支付管理系统',
        'description': '欢迎使用支付管理系统'
    })


@staff_member_required
def pending_payments_list(request):
    """待审核支付列表页面"""
    # 获取待审核的充值订单
    payments = Payment.objects.filter(
        payment_type='recharge',
        status='pending'
    ).select_related('user', 'payment_method').order_by('-created_at')
    
    # 搜索功能
    search = request.GET.get('search', '').strip()
    if search:
        from django.db.models import Q
        payments = payments.filter(
            Q(user__username__icontains=search) |
            Q(user__real_name__icontains=search) |
            Q(user__phone__icontains=search) |
            Q(payment_id__icontains=search)
        )
    
    # 分页
    page = request.GET.get('page', 1)
    paginator = Paginator(payments, 20)
    payments_page = paginator.get_page(page)
    
    context = {
        'title': '待审核支付',
        'payments': payments_page,
        'search': search,
        'total_count': paginator.count
    }
    
    return render(request, 'payments/pending_payments.html', context)


@staff_member_required
@csrf_exempt
def approve_payment(request, payment_id):
    """审核支付订单"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '请求方法错误'})
    
    try:
        payment = get_object_or_404(Payment, payment_id=payment_id, payment_type='recharge')
        
        if payment.status != 'pending':
            return JsonResponse({'success': False, 'message': '支付订单状态不允许审核'})
        
        action = request.POST.get('action')
        
        with transaction.atomic():
            if action == 'approve':
                # 审核通过
                payment.status = 'completed'
                payment.paid_at = timezone.now()
                payment.save()
                
                # 更新用户账户余额
                account, created = UserAccount.objects.get_or_create(
                    user=payment.user,
                    defaults={'balance': Decimal('0.00')}
                )
                
                # 记录账户交易
                AccountTransaction.objects.create(
                    account=account,
                    transaction_type='recharge',
                    amount=payment.amount,
                    balance_before=account.balance,
                    balance_after=account.balance + payment.amount,
                    payment=payment,
                    description=f'管理员审核通过充值: {payment.description}'
                )
                
                # 更新账户余额
                account.balance += payment.amount
                account.total_paid += payment.amount
                account.save()
                
                messages.success(request, f'充值订单 {payment.payment_id} 审核通过，用户余额已更新')
                return JsonResponse({'success': True, 'message': '审核通过，用户余额已更新'})
                
            elif action == 'reject':
                # 审核拒绝
                payment.status = 'failed'
                payment.paid_at = timezone.now()
                payment.save()
                
                messages.success(request, f'充值订单 {payment.payment_id} 已拒绝')
                return JsonResponse({'success': True, 'message': '订单已拒绝'})
            
            else:
                return JsonResponse({'success': False, 'message': '无效的操作'})
                
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'操作失败: {str(e)}'})


@staff_member_required
def payment_detail_view(request, payment_id):
    """支付订单详情页面"""
    payment = get_object_or_404(Payment, payment_id=payment_id)
    
    context = {
        'title': '支付订单详情',
        'payment': payment
    }
    
    return render(request, 'payments/payment_detail.html', context)