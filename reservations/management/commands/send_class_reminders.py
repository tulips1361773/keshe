from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from reservations.models import Booking
from notifications.models import Notification


class Command(BaseCommand):
    help = '发送上课前一小时提醒'

    def handle(self, *args, **options):
        # 获取一小时后的时间范围（前后5分钟的缓冲）
        now = timezone.now()
        start_time = now + timedelta(hours=1, minutes=-5)
        end_time = now + timedelta(hours=1, minutes=5)
        
        # 查找即将开始的预约（已确认状态）
        upcoming_bookings = Booking.objects.filter(
            start_time__gte=start_time,
            start_time__lte=end_time,
            status='confirmed'
        ).select_related('relation__coach', 'relation__student', 'table')
        
        reminder_count = 0
        
        for booking in upcoming_bookings:
            # 检查是否已经发送过提醒（避免重复发送）
            existing_reminder = Notification.objects.filter(
                recipient=booking.student,
                message_type='booking',
                data__contains={'booking_id': booking.id, 'type': 'class_reminder'}
            ).exists()
            
            if not existing_reminder:
                # 给学员发送提醒
                Notification.create_booking_notification(
                    recipient=booking.relation.student,
                    title="上课提醒",
                    message=f"您预约的课程将在一小时后开始。教练：{booking.relation.coach.real_name or booking.relation.coach.username}，球台：{booking.table.name}，时间：{booking.start_time.strftime('%Y-%m-%d %H:%M')}",
                    data={
                        'booking_id': booking.id,
                        'type': 'class_reminder',
                        'table_name': booking.table.name,
                        'coach_name': booking.relation.coach.real_name or booking.relation.coach.username,
                        'start_time': booking.start_time.isoformat()
                    }
                )
                
                # 给教练发送提醒
                coach_reminder = Notification.objects.filter(
                    recipient=booking.relation.coach,
                    message_type='booking',
                    data__contains={'booking_id': booking.id, 'type': 'class_reminder'}
                ).exists()
                
                if not coach_reminder:
                    Notification.create_booking_notification(
                        recipient=booking.relation.coach,
                        title="上课提醒",
                        message=f"您的课程将在一小时后开始。学员：{booking.relation.student.real_name or booking.relation.student.username}，球台：{booking.table.name}，时间：{booking.start_time.strftime('%Y-%m-%d %H:%M')}",
                        data={
                            'booking_id': booking.id,
                            'type': 'class_reminder',
                            'table_name': booking.table.name,
                            'student_name': booking.relation.student.real_name or booking.relation.student.username,
                            'start_time': booking.start_time.isoformat()
                        }
                    )
                
                reminder_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'已发送提醒：预约ID {booking.id}，学员 {booking.relation.student.username}，教练 {booking.relation.coach.username}'
                    )
                )
        
        if reminder_count == 0:
            self.stdout.write(self.style.WARNING('没有需要发送提醒的预约'))
        else:
            self.stdout.write(
                self.style.SUCCESS(f'成功发送 {reminder_count} 个预约的上课提醒')
            )