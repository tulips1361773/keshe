from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission, Group
from .models import User


@receiver(post_save, sender=User)
def setup_campus_admin_permissions(sender, instance, created, **kwargs):
    """
    用户创建后的信号处理器
    为校区管理员自动分配必要的权限
    """
    if created and instance.user_type == 'campus_admin':
        # 获取或创建校区管理员权限组
        campus_admin_group, group_created = Group.objects.get_or_create(
            name='校区管理员'
        )
        
        # 如果是新创建的组，分配权限
        if group_created:
            # 定义校区管理员需要的权限
            campus_admin_permissions = [
                # 校区管理权限
                'campus.view_campus',
                'campus.change_campus',
                'campus.view_campusarea',
                'campus.add_campusarea',
                'campus.change_campusarea',
                'campus.delete_campusarea',
                'campus.view_campusstudent',
                'campus.add_campusstudent',
                'campus.change_campusstudent',
                'campus.delete_campusstudent',
                'campus.view_campuscoach',
                'campus.add_campuscoach',
                'campus.change_campuscoach',
                'campus.delete_campuscoach',
                
                # 用户管理权限
                'accounts.view_user',
                'accounts.change_user',
                'accounts.view_coach',
                'accounts.change_coach',
                'accounts.view_userprofile',
                'accounts.change_userprofile',
                
                # 预约管理权限
                'reservations.view_booking',
                'reservations.add_booking',
                'reservations.change_booking',
                'reservations.delete_booking',
                'reservations.view_table',
                'reservations.add_table',
                'reservations.change_table',
                'reservations.delete_table',
                'reservations.view_coachstudentrelation',
                'reservations.add_coachstudentrelation',
                'reservations.change_coachstudentrelation',
                'reservations.delete_coachstudentrelation',
                'reservations.view_coachchangerequest',
                'reservations.change_coachchangerequest',
                
                # 支付管理权限
                'payments.view_payment',
                'payments.change_payment',
                'payments.view_useraccount',
                'payments.change_useraccount',
                'payments.view_accounttransaction',
                
                # 比赛管理权限
                'competitions.view_competition',
                'competitions.add_competition',
                'competitions.change_competition',
                'competitions.delete_competition',
                'competitions.view_competitionregistration',
                'competitions.change_competitionregistration',
                
                # 通知管理权限
                'notifications.view_notification',
                'notifications.add_notification',
                'notifications.change_notification',
                'notifications.delete_notification',
                
                # 日志查看权限
                'logs.view_systemlog',
                'logs.view_loginlog',
            ]
            
            # 分配权限给组
            for perm_codename in campus_admin_permissions:
                try:
                    app_label, codename = perm_codename.split('.')
                    permission = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename
                    )
                    campus_admin_group.permissions.add(permission)
                except Permission.DoesNotExist:
                    # 如果权限不存在，跳过
                    continue
        
        # 将用户加入校区管理员组
        instance.groups.add(campus_admin_group)
        
        print(f"✅ 为校区管理员 {instance.username} 自动分配了权限组")