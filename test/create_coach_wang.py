import os
import django
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keshe.settings')
django.setup()

from accounts.models import User, Coach
from reservations.models import Booking, CoachStudentRelation, Table
from campus.models import Campus

# 创建王教练用户
try:
    coach_wang = User.objects.get(username='王教练')
    created = False
    print(f'王教练用户已存在 (ID: {coach_wang.id})')
except User.DoesNotExist:
    # 找一个不重复的手机号
    phone_base = '13900139'
    for i in range(100, 200):
        phone = f'{phone_base}{i:03d}'
        if not User.objects.filter(phone=phone).exists():
            break
    
    coach_wang = User.objects.create(
        username='王教练',
        email='wangcoach@example.com',
        first_name='王',
        last_name='教练',
        real_name='王教练',
        phone=phone,
        user_type='coach',
        is_active=True,
    )
    coach_wang.set_password('password123')
    coach_wang.save()
    created = True
    print(f'成功创建王教练用户 (ID: {coach_wang.id}, 手机号: {phone})')



# 创建教练资料
coach_profile, profile_created = Coach.objects.get_or_create(
    user=coach_wang,
    defaults={
        'coach_level': 'senior',
        'hourly_rate': 120.00,
        'status': 'approved',
        'achievements': '资深乒乓球教练，具有10年教学经验',
        'max_students': 30,
    }
)

if profile_created:
    print(f'成功创建王教练资料')
else:
    print(f'王教练资料已存在')

# 获取校区和球台
campus = Campus.objects.first()
if not campus:
    campus = Campus.objects.create(name='主校区', address='测试地址')
    print(f'创建校区: {campus.name}')

tables = Table.objects.filter(campus=campus)[:3]
if not tables:
    # 创建一些球台
    for i in range(1, 4):
        Table.objects.create(
            campus=campus,
            number=f'T{i}',
            name=f'球台{i}',
            status='available'
        )
    tables = Table.objects.filter(campus=campus)[:3]
    print(f'创建了 {len(tables)} 个球台')

# 创建一些学生用户作为预约者
students = []
for i in range(1, 4):
    username = f'wang_student{i}'
    try:
        student = User.objects.get(username=username)
        print(f'学生用户 {username} 已存在')
    except User.DoesNotExist:
        # 找一个不重复的手机号
        phone_base = '13800138'
        for j in range(100 + i * 10, 200):
            phone = f'{phone_base}{j:03d}'[:-1]  # 取11位
            if not User.objects.filter(phone=phone).exists():
                break
        
        student = User.objects.create(
            username=username,
            email=f'wangstudent{i}@example.com',
            first_name=f'王学生{i}',
            real_name=f'王学生{i}',
            phone=phone,
            user_type='student',
            is_active=True,
        )
        student.set_password('password123')
        student.save()
        print(f'创建学生用户: {username} (手机号: {phone})')
    
    students.append(student)

print(f'准备了 {len(students)} 个学生用户')

# 为每个学生创建与王教练的师生关系
relations = []
for student in students:
    relation, created = CoachStudentRelation.objects.get_or_create(
        coach=coach_wang,
        student=student,
        defaults={
            'status': 'approved',
            'applied_by': 'student',
        }
    )
    relations.append(relation)
    if created:
        print(f'创建师生关系: {coach_wang.first_name} - {student.first_name}')

# 为王教练创建课表预约数据
base_date = datetime.now().date()
bookings_created = 0

# 创建本周的预约数据
for day_offset in range(7):  # 本周7天
    current_date = base_date + timedelta(days=day_offset)
    
    # 每天创建2-3个预约
    for hour in [9, 14, 16]:  # 上午9点、下午2点、下午4点
        if bookings_created >= len(students) * 3:  # 限制预约数量
            break
            
        start_time = datetime.combine(current_date, datetime.min.time().replace(hour=hour))
        end_time = start_time + timedelta(hours=1)
        
        # 选择师生关系和球台
        relation = relations[bookings_created % len(relations)]
        table = tables[bookings_created % len(tables)]
        
        booking, created = Booking.objects.get_or_create(
            relation=relation,
            table=table,
            start_time=start_time,
            end_time=end_time,
            defaults={
                'status': 'confirmed',
                'duration_hours': 1.0,
                'total_fee': 100.00,
                'notes': f'王教练的课程 - {current_date.strftime("%Y-%m-%d")} {hour}:00',
            }
        )
        
        if created:
            bookings_created += 1
            print(f'创建预约: {relation.student.first_name} - {start_time.strftime("%Y-%m-%d %H:%M")} - 球台{table.number}')

print(f'\n总共为王教练创建了 {bookings_created} 个预约')
print(f'王教练ID: {coach_wang.id}')
print('数据创建完成！')