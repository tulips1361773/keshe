import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach
from reservations.models import Booking, CoachStudentRelation
from campus.models import Campus

# 验证王教练用户
print('=== 验证王教练用户信息 ===')
try:
    coach_wang = User.objects.get(username='王教练')
    print(f'✓ 王教练用户存在 (ID: {coach_wang.id})')
    print(f'  - 姓名: {coach_wang.real_name}')
    print(f'  - 邮箱: {coach_wang.email}')
    print(f'  - 手机: {coach_wang.phone}')
    print(f'  - 用户类型: {coach_wang.user_type}')
    print(f'  - 是否激活: {coach_wang.is_active}')
except User.DoesNotExist:
    print('✗ 王教练用户不存在')
    exit(1)

# 验证教练资料
print('\n=== 验证王教练资料 ===')
try:
    coach_profile = Coach.objects.get(user=coach_wang)
    print(f'✓ 王教练资料存在')
    print(f'  - 教练级别: {coach_profile.get_coach_level_display()}')
    print(f'  - 时薪: {coach_profile.hourly_rate} 元/小时')
    print(f'  - 审核状态: {coach_profile.get_status_display()}')
    print(f'  - 最大学员数: {coach_profile.max_students}')
    print(f'  - 成就描述: {coach_profile.achievements}')
except Coach.DoesNotExist:
    print('✗ 王教练资料不存在')

# 验证师生关系
print('\n=== 验证师生关系 ===')
relations = CoachStudentRelation.objects.filter(coach=coach_wang)
print(f'✓ 找到 {relations.count()} 个师生关系')
for relation in relations:
    print(f'  - {relation.student.real_name} ({relation.get_status_display()})')

# 验证预约数据
print('\n=== 验证预约数据 ===')
bookings = Booking.objects.filter(relation__coach=coach_wang).order_by('start_time')
print(f'✓ 找到 {bookings.count()} 个预约')

for booking in bookings:
    print(f'  - {booking.start_time.strftime("%Y-%m-%d %H:%M")} - {booking.end_time.strftime("%H:%M")}')
    print(f'    学生: {booking.relation.student.real_name}')
    print(f'    球台: {booking.table.name} ({booking.table.number})')
    print(f'    状态: {booking.get_status_display()}')
    print(f'    费用: {booking.total_fee} 元')
    print(f'    时长: {booking.duration_hours} 小时')
    if booking.notes:
        print(f'    备注: {booking.notes}')
    print()

# 验证校区和球台
print('=== 验证校区和球台 ===')
campus = Campus.objects.first()
if campus:
    print(f'✓ 校区: {campus.name}')
    tables = campus.tables.all()
    print(f'✓ 球台数量: {tables.count()}')
    for table in tables:
        print(f'  - {table.name} ({table.number}) - {table.get_status_display()}')
else:
    print('✗ 没有找到校区')

print('\n=== 数据验证完成 ===')