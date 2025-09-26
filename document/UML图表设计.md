# 乒乓球培训管理系统UML图表设计

**版本：** 1.0  
**日期：** 2025年1月  
**编写人员：** 项目开发团队  

## 一、用例图设计

### 1.1 系统总体用例图

```plantuml
@startuml 系统总体用例图
!theme plain
skinparam backgroundColor white
skinparam actorStyle awesome

title 乒乓球培训管理系统总体用例图

' 定义参与者
actor "学员" as Student
actor "教练员" as Coach  
actor "校区管理员" as CampusAdmin
actor "超级管理员" as SuperAdmin

' 定义系统边界
rectangle "乒乓球培训管理系统" {
  
  ' 学员用例
  usecase "用户注册" as UC1
  usecase "用户登录" as UC2
  usecase "查询教练员" as UC3
  usecase "选择教练员" as UC4
  usecase "预约课程" as UC5
  usecase "账户充值" as UC6
  usecase "查看课表" as UC7
  usecase "取消预约" as UC8
  usecase "更换教练员" as UC9
  usecase "训练评价" as UC10
  usecase "月赛报名" as UC11
  usecase "查看比赛信息" as UC12
  usecase "查看消息通知" as UC13
  usecase "支付管理" as UC14
  usecase "申请退费" as UC15
  usecase "查看账户余额" as UC16
  usecase "查看交易记录" as UC17
  
  ' 教练员用例
  usecase "教练员注册" as UC19
  usecase "审核学员申请" as UC20
  usecase "确认课程预约" as UC21
  usecase "拒绝课程预约" as UC22
  usecase "维护个人信息" as UC23
  usecase "学员训练评价" as UC24
  usecase "查看课程安排" as UC25
  usecase "管理课程表" as UC26
  
  ' 校区管理员用例
  usecase "管理学员信息" as UC28
  usecase "管理教练信息" as UC29
  usecase "审核教练注册" as UC30
  usecase "管理课程预约" as UC31
  usecase "查询系统日志" as UC32
  usecase "线下充值录入" as UC33
  usecase "审核充值申请" as UC34
  usecase "管理比赛" as UC35
  usecase "创建比赛分组" as UC36
  usecase "生成比赛赛程" as UC37
  usecase "记录比赛结果" as UC38
  usecase "发送系统通知" as UC39
  
  ' 超级管理员用例
  usecase "管理校区信息" as UC40
  usecase "指定校区负责人" as UC41
  usecase "系统全局管理" as UC42
  usecase "审核退费申请" as UC43
  usecase "批量发送通知" as UC44
}

' 学员关联
Student --> UC1
Student --> UC2
Student --> UC3
Student --> UC4
Student --> UC5
Student --> UC6
Student --> UC7
Student --> UC8
Student --> UC9
Student --> UC10
Student --> UC11
Student --> UC12
Student --> UC13
Student --> UC14
Student --> UC15
Student --> UC16
Student --> UC17


' 教练员关联
Coach --> UC2
Coach --> UC19
Coach --> UC20
Coach --> UC21
Coach --> UC22
Coach --> UC23
Coach --> UC24
Coach --> UC25
Coach --> UC26
Coach --> UC27
Coach --> UC13

' 校区管理员关联
CampusAdmin --> UC2
CampusAdmin --> UC28
CampusAdmin --> UC29
CampusAdmin --> UC30
CampusAdmin --> UC31
CampusAdmin --> UC32
CampusAdmin --> UC33
CampusAdmin --> UC34
CampusAdmin --> UC35
CampusAdmin --> UC36
CampusAdmin --> UC37
CampusAdmin --> UC38
CampusAdmin --> UC39
CampusAdmin --> UC13

' 超级管理员关联
SuperAdmin --> UC2
SuperAdmin --> UC40
SuperAdmin --> UC41
SuperAdmin --> UC42
SuperAdmin --> UC43
SuperAdmin --> UC44
SuperAdmin --> UC13

' 包含关系
UC4 ..> UC3 : <<include>>
UC5 ..> UC4 : <<include>>
UC8 ..> UC5 : <<include>>
UC11 ..> UC6 : <<include>>
UC14 ..> UC6 : <<include>>
UC15 ..> UC14 : <<include>>
UC17 ..> UC16 : <<include>>
UC36 ..> UC35 : <<include>>
UC37 ..> UC36 : <<include>>

' 扩展关系
UC21 <.. UC31 : <<extend>>
UC22 <.. UC31 : <<extend>>
UC34 <.. UC33 : <<extend>>
UC43 <.. UC15 : <<extend>>

@enduml
```

### 1.2 学员子系统用例图

```plantuml
@startuml 学员子系统用例图
!theme plain
skinparam backgroundColor white

title 学员子系统用例图

actor "学员" as Student

rectangle "学员管理子系统" {
  usecase "注册账户" as Register
  usecase "登录系统" as Login
  usecase "维护个人信息" as UpdateProfile
  usecase "修改密码" as ChangePassword
  usecase "上传头像" as UploadAvatar
}

rectangle "教练选择子系统" {
  usecase "按姓名查询教练" as SearchByName
  usecase "浏览所有教练" as BrowseAll
  usecase "查看教练详情" as ViewCoachDetail
  usecase "申请选择教练" as ApplyCoach
  usecase "查看申请状态" as CheckStatus
}

rectangle "课程管理子系统" {
  usecase "查看教练课表" as ViewSchedule
  usecase "预约课程" as BookCourse
  usecase "选择球台" as SelectTable
  usecase "确认预约" as ConfirmBooking
  usecase "取消预约" as CancelBooking
  usecase "查看我的课表" as MySchedule
}

rectangle "财务管理子系统" {
  usecase "在线充值" as OnlineRecharge
  usecase "线下充值" as OfflineRecharge
  usecase "查看账户余额" as CheckBalance
  usecase "查看消费记录" as ViewConsumption
  usecase "申请退费" as RequestRefund
}

rectangle "赛事管理子系统" {
  usecase "查看月赛信息" as ViewMatchInfo
  usecase "报名月赛" as RegisterMatch
  usecase "查看赛程安排" as ViewScheduleMatch
  usecase "查看比赛结果" as ViewResult
}

' 学员关联
Student --> Register
Student --> Login
Student --> UpdateProfile
Student --> SearchByName
Student --> BrowseAll
Student --> BookCourse
Student --> OnlineRecharge
Student --> RegisterMatch

' 包含关系
UpdateProfile ..> ChangePassword : <<include>>
UpdateProfile ..> UploadAvatar : <<include>>
SearchByName ..> ViewCoachDetail : <<include>>
BrowseAll ..> ViewCoachDetail : <<include>>
ViewCoachDetail ..> ApplyCoach : <<include>>
ApplyCoach ..> CheckStatus : <<include>>
BookCourse ..> ViewSchedule : <<include>>
BookCourse ..> SelectTable : <<include>>
BookCourse ..> ConfirmBooking : <<include>>
RegisterMatch ..> ViewMatchInfo : <<include>>

' 扩展关系
OnlineRecharge <.. OfflineRecharge : <<extend>>
CheckBalance <.. ViewConsumption : <<extend>>
CancelBooking <.. RequestRefund : <<extend>>

@enduml
```

### 1.3 教练员子系统用例图

```plantuml
@startuml 教练员子系统用例图
!theme plain
skinparam backgroundColor white

title 教练员子系统用例图

actor "教练员" as Coach
actor "校区管理员" as Admin

rectangle "教练员管理子系统" {
  usecase "教练员注册" as CoachRegister
  usecase "提交资质材料" as SubmitCredentials
  usecase "等待审核" as WaitApproval
  usecase "维护个人信息" as UpdateCoachProfile
  usecase "上传获奖信息" as UploadAchievements
}

rectangle "学员管理子系统" {
  usecase "查看学员申请" as ViewApplications
  usecase "审核学员申请" as ReviewApplication
  usecase "接受申请" as AcceptApplication
  usecase "拒绝申请" as RejectApplication
  usecase "查看我的学员" as ViewMyStudents
  usecase "学员信息管理" as ManageStudentInfo
}

rectangle "课程管理子系统" {
  usecase "查看课程预约" as ViewBookings
  usecase "确认预约" as ConfirmBooking
  usecase "拒绝预约" as RejectBooking
  usecase "设置可用时间" as SetAvailableTime
  usecase "查看我的课表" as ViewMySchedule
  usecase "课程取消处理" as HandleCancellation
}

rectangle "评价管理子系统" {
  usecase "课后评价学员" as EvaluateStudent
  usecase "提供训练建议" as GiveAdvice
  usecase "查看评价历史" as ViewEvaluationHistory
}

' 教练员关联
Coach --> CoachRegister
Coach --> UpdateCoachProfile
Coach --> ViewApplications
Coach --> ViewBookings
Coach --> EvaluateStudent

' 管理员关联
Admin --> WaitApproval

' 包含关系
CoachRegister ..> SubmitCredentials : <<include>>
CoachRegister ..> WaitApproval : <<include>>
UpdateCoachProfile ..> UploadAchievements : <<include>>
ReviewApplication ..> AcceptApplication : <<include>>
ReviewApplication ..> RejectApplication : <<include>>
ViewApplications ..> ReviewApplication : <<include>>
ViewBookings ..> ConfirmBooking : <<include>>
ViewBookings ..> RejectBooking : <<include>>
EvaluateStudent ..> GiveAdvice : <<include>>

' 扩展关系
ViewMyStudents <.. ManageStudentInfo : <<extend>>
SetAvailableTime <.. ViewMySchedule : <<extend>>
HandleCancellation <.. ViewBookings : <<extend>>

@enduml
```

## 二、活动图设计

### 2.1 学员选择教练流程活动图

```plantuml
@startuml 学员选择教练流程
!theme plain
skinparam backgroundColor white

title 学员选择教练流程活动图

start

:学员登录系统;

:选择查询方式;

if (按姓名查询?) then (是)
  :输入查询条件;
  :系统搜索匹配教练;
  if (找到匹配教练?) then (是)
    if (多个教练?) then (是)
      :显示教练列表;
      :学员选择查看详情;
    else (否)
      :直接显示教练详情;
    endif
  else (否)
    :显示"未找到相关教练";
    stop
  endif
else (否)
  :浏览所有教练;
  :显示本校区教练列表;
  :学员选择查看详情;
endif

:显示教练详细信息;
note right: 包括照片、获奖信息等

:学员点击"选择教练";

:检查学员当前教练数量;

if (已有2个教练?) then (是)
  :提示"最多只能选择2个教练";
  stop
else (否)
  :提交选择申请;
  :系统发送消息给教练;
  :显示"申请已提交，等待教练审核";
endif

fork
  :教练收到申请通知;
  :教练审核申请;
  
  if (教练同意?) then (是)
    :建立双选关系;
    :系统通知学员"申请通过";
    :记录成功双选记录;
  else (否)
    :拒绝申请;
    :系统通知学员"申请被拒绝";
    :记录失败双选记录;
  endif
fork again
  :学员可查看申请状态;
end fork

stop

@enduml
```

### 2.2 课程预约流程活动图

```plantuml
@startuml 课程预约流程
!theme plain
skinparam backgroundColor white

title 课程预约流程活动图

start

:学员登录系统;

:选择已建立双选关系的教练;

if (存在双选关系?) then (否)
  :提示"请先选择教练";
  stop
else (是)
  :显示教练课表;
  note right: 显示未来一周的课表
endif

:学员选择空白时间段;

:系统显示可用球台;

if (学员选择球台?) then (手动选择)
  :学员选择具体球台;
else (自动分配)
  :系统自动分配球台;
endif

:计算课时费;

:检查学员账户余额;

if (余额充足?) then (否)
  :提示"余额不足，请先充值";
  :跳转到充值页面;
  stop
else (是)
  :提交预约申请;
endif

:系统发送消息给教练;

fork
  :教练收到预约通知;
  :教练审核预约;
  
  if (教练确认?) then (是)
    :扣除学员账户课时费;
    :预约状态变更为"已确认";
    :系统通知学员"预约成功";
    :添加到双方课表;
  else (否)
    :拒绝预约;
    :系统通知学员"预约被拒绝";
    :预约状态变更为"已拒绝";
  endif
fork again
  :学员可查看预约状态;
end fork

if (预约成功?) then (是)
  :课程开始前1小时;
  :系统发送上课提醒;
  
  :课程结束后;
  :系统发起评价请求;
  
  fork
    :学员填写训练收获;
  fork again
    :教练评价学员表现;
  end fork
endif

stop

@enduml
```

### 2.3 月赛报名流程活动图

```plantuml
@startuml 月赛报名流程
!theme plain
skinparam backgroundColor white

title 月赛报名流程活动图

start

:学员登录系统;

:查看月赛信息;

:点击"报名参赛";

:检查报名截止时间;

if (已截止?) then (是)
  :提示"报名已截止";
  stop
else (否)
  :显示报名费用(30元);
endif

:检查学员账户余额;

if (余额充足?) then (否)
  :提示"余额不足，请先充值";
  :跳转到充值页面;
  stop
else (是)
  :确认报名;
  :扣除报名费;
  :报名成功;
endif

:系统记录报名信息;

:等待报名截止;

:系统统计参赛人数;

if (每组人数 <= 6?) then (是)
  :采用组内全循环;
  :随机分配球台;
else (否)
  :分为更小的小组;
  :小组内全循环;
  :取小组前两名;
  :交叉淘汰赛;
endif

:生成赛程安排;

:系统通知参赛学员;

:学员查看比赛安排;
note right: 包括比赛时间、对手、球台等

:比赛当天;

:按赛程进行比赛;

:录入比赛结果;

:更新赛程状态;

:公布最终结果;

stop

@enduml
```

### 2.5 支付充值流程活动图

```plantuml
@startuml 支付充值流程
!theme plain
skinparam backgroundColor white

title 支付充值流程活动图

start

:学员登录系统;

:进入账户充值页面;

:选择充值方式;

if (在线充值?) then (是)
  :选择支付方式;
  note right: 支付宝、微信、银行卡等
  
  :输入充值金额;
  
  :提交充值申请;
  
  :跳转到第三方支付平台;
  
  if (支付成功?) then (是)
    :系统接收支付回调;
    :更新账户余额;
    :记录交易记录;
    :发送充值成功通知;
  else (否)
    :支付失败;
    :显示失败原因;
    stop
  endif
else (否)
  :选择线下充值;
  :填写充值信息;
  note right: 金额、支付方式、备注等
  
  :提交线下充值申请;
  :系统创建待审核订单;
  :通知管理员审核;
  
  fork
    :管理员收到审核通知;
    :管理员查看充值申请;
    
    if (审核通过?) then (是)
      :更新订单状态为已完成;
      :更新学员账户余额;
      :记录交易记录;
      :通知学员充值成功;
    else (否)
      :拒绝充值申请;
      :更新订单状态为已拒绝;
      :通知学员申请被拒绝;
    endif
  fork again
    :学员可查看申请状态;
  end fork
endif

:充值完成;

stop

@enduml
```

### 2.6 退费申请流程活动图

```plantuml
@startuml 退费申请流程
!theme plain
skinparam backgroundColor white

title 退费申请流程活动图

start

:学员登录系统;

:进入退费申请页面;

:选择要退费的支付记录;

:检查支付状态;

if (支付已完成?) then (否)
  :提示"只能对已完成的支付申请退费";
  stop
else (是)
  :填写退费信息;
  note right: 退费金额、退费原因等
endif

:验证退费金额;

if (退费金额 <= 支付金额?) then (否)
  :提示"退费金额不能超过支付金额";
  stop
else (是)
  :提交退费申请;
endif

:系统创建退费记录;

:通知管理员审核;

fork
  :管理员收到审核通知;
  :管理员查看退费申请;
  
  if (审核通过?) then (是)
    :更新退费状态为已批准;
    :处理退费操作;
    
    if (原路退回?) then (是)
      :退款到原支付账户;
    else (否)
      :退款到学员账户余额;
      :更新账户余额;
      :记录交易记录;
    endif
    
    :通知学员退费成功;
  else (否)
    :拒绝退费申请;
    :更新退费状态为已拒绝;
    :通知学员申请被拒绝;
  endif
fork again
  :学员可查看申请状态;
end fork

:退费处理完成;

stop

@enduml
```

### 2.7 比赛管理流程活动图

```plantuml
@startuml 比赛管理流程
!theme plain
skinparam backgroundColor white

title 比赛管理流程活动图

start

:管理员登录系统;

:创建新比赛;

:设置比赛信息;
note right: 名称、时间、报名费、截止时间等

:发布比赛公告;

:学员查看比赛信息;

:学员报名参赛;

:系统扣除报名费;

:等待报名截止;

:管理员统计参赛人数;

:创建比赛分组;

if (参赛人数 <= 6?) then (是)
  :采用单组循环赛;
else (否)
  :分为多个小组;
  :小组内循环赛;
  :取前两名进入淘汰赛;
endif

:生成比赛赛程;

:分配比赛时间和球台;

:发送赛程通知给参赛者;

:比赛开始;

repeat
  :进行单场比赛;
  :记录比赛结果;
  :更新积分排名;
repeat while (还有未完成比赛?) is (是)
-> 否;

:计算最终排名;

:公布比赛结果;

:发送结果通知;

stop

@enduml
```

### 2.8 消息通知流程活动图

```plantuml
@startuml 消息通知流程
!theme plain
skinparam backgroundColor white

title 消息通知流程活动图

start

:系统事件触发;
note right: 预约确认、支付成功、比赛安排等

:确定通知类型;

if (系统自动通知?) then (是)
  :根据事件类型生成通知内容;
  :确定接收用户;
  :创建通知记录;
else (否)
  :管理员手动创建通知;
  :选择通知类型;
  
  if (单个用户通知?) then (是)
    :选择接收用户;
    :编写通知内容;
    :创建通知记录;
  else (否)
    :批量通知;
    :选择用户群体;
    note right: 按用户类型、校区等筛选
    :编写通知内容;
    :批量创建通知记录;
  endif
endif

:发送通知;

fork
  :用户登录系统;
  :查看未读通知数量;
  :查看通知列表;
  :点击查看通知详情;
  :标记通知为已读;
fork again
  :用户可以删除通知;
fork again
  :用户可以清空所有通知;
end fork

:通知处理完成;

stop

@enduml
```

## 三、时序图设计

### 3.1 用户登录时序图

```plantuml
@startuml 用户登录时序图
!theme plain
skinparam backgroundColor white

title 用户登录时序图

participant "用户" as User
participant "登录控制器" as LoginController
participant "用户服务" as UserService
participant "数据库" as Database
participant "会话管理" as SessionManager

User -> LoginController: 输入用户名和密码
activate LoginController

LoginController -> UserService: 验证用户凭据
activate UserService

UserService -> Database: 查询用户信息
activate Database
Database --> UserService: 返回用户数据
deactivate Database

alt 用户存在且密码正确
  UserService -> UserService: 验证密码
  UserService --> LoginController: 验证成功
  
  LoginController -> SessionManager: 创建用户会话
  activate SessionManager
  SessionManager --> LoginController: 返回会话ID
  deactivate SessionManager
  
  LoginController --> User: 登录成功，跳转到主页
else 用户不存在或密码错误
  UserService --> LoginController: 验证失败
  LoginController --> User: 显示错误信息
endif

deactivate UserService
deactivate LoginController

@enduml
```

### 3.3 支付充值时序图

```plantuml
@startuml 支付充值时序图
!theme plain
skinparam backgroundColor white

title 支付充值时序图

participant "学员" as Student
participant "支付控制器" as PaymentController
participant "支付服务" as PaymentService
participant "账户服务" as AccountService
participant "第三方支付" as ThirdPartyPayment
participant "消息服务" as MessageService
participant "数据库" as Database

Student -> PaymentController: 提交充值申请
activate PaymentController

PaymentController -> PaymentService: 处理充值请求
activate PaymentService

PaymentService -> Database: 创建支付记录
activate Database
Database --> PaymentService: 返回支付ID
deactivate Database

alt 在线支付
  PaymentService -> ThirdPartyPayment: 调用支付接口
  activate ThirdPartyPayment
  ThirdPartyPayment --> PaymentService: 返回支付链接
  deactivate ThirdPartyPayment
  
  PaymentService --> PaymentController: 返回支付链接
  PaymentController --> Student: 跳转到支付页面
  
  Student -> ThirdPartyPayment: 完成支付
  activate ThirdPartyPayment
  ThirdPartyPayment -> PaymentService: 支付回调通知
  activate PaymentService
  
  PaymentService -> Database: 更新支付状态
  activate Database
  Database --> PaymentService: 更新成功
  deactivate Database
  
  PaymentService -> AccountService: 更新账户余额
  activate AccountService
  AccountService -> Database: 更新余额和交易记录
  activate Database
  Database --> AccountService: 更新成功
  deactivate Database
  AccountService --> PaymentService: 余额更新成功
  deactivate AccountService
  
  PaymentService -> MessageService: 发送充值成功通知
  activate MessageService
  MessageService --> PaymentService: 通知发送成功
  deactivate MessageService
  
  PaymentService --> ThirdPartyPayment: 确认回调处理
  deactivate PaymentService
  ThirdPartyPayment --> Student: 显示支付成功
  deactivate ThirdPartyPayment

else 线下支付
  PaymentService -> Database: 创建待审核记录
  activate Database
  Database --> PaymentService: 记录创建成功
  deactivate Database
  
  PaymentService -> MessageService: 通知管理员审核
  activate MessageService
  MessageService --> PaymentService: 通知发送成功
  deactivate MessageService
  
  PaymentService --> PaymentController: 申请提交成功
  PaymentController --> Student: 显示"等待审核"
endif

deactivate PaymentService
deactivate PaymentController

@enduml
```

### 3.4 比赛报名时序图

```plantuml
@startuml 比赛报名时序图
!theme plain
skinparam backgroundColor white

title 比赛报名时序图

participant "学员" as Student
participant "比赛控制器" as CompetitionController
participant "比赛服务" as CompetitionService
participant "账户服务" as AccountService
participant "消息服务" as MessageService
participant "数据库" as Database

Student -> CompetitionController: 提交报名申请
activate CompetitionController

CompetitionController -> CompetitionService: 处理报名请求
activate CompetitionService

CompetitionService -> Database: 检查比赛状态和报名截止时间
activate Database
Database --> CompetitionService: 返回比赛信息
deactivate Database

alt 报名未截止
  CompetitionService -> Database: 检查是否已报名
  activate Database
  Database --> CompetitionService: 返回报名状态
  deactivate Database
  
  alt 未报名
    CompetitionService -> Database: 检查参赛人数限制
    activate Database
    Database --> CompetitionService: 返回当前报名人数
    deactivate Database
    
    alt 未达到人数限制
      CompetitionService -> AccountService: 检查账户余额
      activate AccountService
      AccountService -> Database: 查询账户余额
      activate Database
      Database --> AccountService: 返回余额信息
      deactivate Database
      AccountService --> CompetitionService: 余额检查结果
      deactivate AccountService
      
      alt 余额充足
        CompetitionService -> Database: 创建报名记录
        activate Database
        Database --> CompetitionService: 报名记录创建成功
        deactivate Database
        
        CompetitionService -> AccountService: 扣除报名费
        activate AccountService
        AccountService -> Database: 更新余额和交易记录
        activate Database
        Database --> AccountService: 扣费成功
        deactivate Database
        AccountService --> CompetitionService: 扣费完成
        deactivate AccountService
        
        CompetitionService -> MessageService: 发送报名成功通知
        activate MessageService
        MessageService --> CompetitionService: 通知发送成功
        deactivate MessageService
        
        CompetitionService --> CompetitionController: 报名成功
        CompetitionController --> Student: 显示"报名成功"
      else 余额不足
        CompetitionService --> CompetitionController: 余额不足
        CompetitionController --> Student: 提示充值
      endif
    else 人数已满
      CompetitionService --> CompetitionController: 报名已满
      CompetitionController --> Student: 显示"报名已满"
    endif
  else 已报名
    CompetitionService --> CompetitionController: 重复报名
    CompetitionController --> Student: 显示"已报名"
  endif
else 报名已截止
  CompetitionService --> CompetitionController: 报名截止
  CompetitionController --> Student: 显示"报名已截止"
endif

deactivate CompetitionService
deactivate CompetitionController

@enduml
```

## 四、类图设计

### 4.1 用户管理类图

```plantuml
@startuml 用户管理类图
!theme plain
skinparam backgroundColor white

title 用户管理类图

abstract class User {
  - id: Long
  - username: String
  - password: String
  - realName: String
  - gender: Gender
  - age: Integer
  - phone: String
  - email: String
  - avatar: String
  - campusId: Long
  - createTime: DateTime
  - lastLoginTime: DateTime
  - status: UserStatus
  
  + login(username: String, password: String): Boolean
  + logout(): void
  + updateProfile(profile: UserProfile): Boolean
  + changePassword(oldPassword: String, newPassword: String): Boolean
  + uploadAvatar(avatarFile: File): String
}

class Student extends User {
  - balance: BigDecimal
  - coachCount: Integer
  
  + recharge(amount: BigDecimal, paymentMethod: PaymentMethod): Boolean
  + getBalance(): BigDecimal
  + getCoaches(): List<Coach>
  + applyForCoach(coachId: Long): Boolean
  + bookCourse(coachId: Long, dateTime: DateTime, duration: Integer): Boolean
  + cancelBooking(bookingId: Long): Boolean
  + evaluateTraining(bookingId: Long, evaluation: String): Boolean
  + registerCompetition(competitionId: Long): Boolean
  + viewTransactionHistory(): List<Transaction>
}

class Coach extends User {
  - level: CoachLevel
  - achievements: String
  - hourlyRate: BigDecimal
  - maxStudents: Integer
  - approvalStatus: ApprovalStatus
  
  + getStudents(): List<Student>
  + approveStudentApplication(applicationId: Long, approved: Boolean): Boolean
  + confirmBooking(bookingId: Long, confirmed: Boolean): Boolean
  + setAvailableTime(schedule: Schedule): Boolean
  + evaluateStudent(bookingId: Long, evaluation: String): Boolean
  + viewEarnings(): BigDecimal
}

class CampusAdmin extends User {
  - campusId: Long
  - permissions: List<Permission>
  
  + manageStudents(): List<Student>
  + manageCoaches(): List<Coach>
  + approveCoachRegistration(coachId: Long, approved: Boolean): Boolean
  + viewSystemLogs(): List<SystemLog>
  + processOfflineRecharge(studentId: Long, amount: BigDecimal): Boolean
  + manageCompetitions(): List<Competition>
  + approveRefundRequest(refundId: Long, approved: Boolean): Boolean
}

class SuperAdmin extends User {
  + manageCampuses(): List<Campus>
  + createCampus(campus: Campus): Boolean
  + assignCampusAdmin(campusId: Long, adminId: Long): Boolean
  + viewAllSystemData(): SystemData
  + managePaymentMethods(): List<PaymentMethod>
  + viewSystemStatistics(): Map<String, Object>
}

class UserAccount {
  - id: Long
  - userId: Long
  - balance: BigDecimal
  - totalRecharge: BigDecimal
  - totalConsumption: BigDecimal
  - createTime: DateTime
  - updateTime: DateTime
  
  + recharge(amount: BigDecimal): Boolean
  + deduct(amount: BigDecimal): Boolean
  + getTransactionHistory(): List<Transaction>
  + freezeAccount(): Boolean
  + unfreezeAccount(): Boolean
}

class Transaction {
  - id: Long
  - accountId: Long
  - transactionType: TransactionType
  - amount: BigDecimal
  - balanceAfter: BigDecimal
  - description: String
  - relatedId: Long
  - createTime: DateTime
  
  + getTransactionDetails(): Map<String, Object>
}

enum Gender {
  MALE
  FEMALE
  OTHER
}

enum UserStatus {
  ACTIVE
  FROZEN
  DELETED
}

enum CoachLevel {
  SENIOR
  INTERMEDIATE
  JUNIOR
}

enum ApprovalStatus {
  PENDING
  APPROVED
  REJECTED
}

enum TransactionType {
  RECHARGE
  CONSUMPTION
  REFUND
  TRANSFER
}

class Campus {
  - id: Long
  - name: String
  - address: String
  - contactPerson: String
  - phone: String
  - email: String
  - adminId: Long
  - createTime: DateTime
  - status: CampusStatus
  
  + getStudents(): List<Student>
  + getCoaches(): List<Coach>
  + getAdmin(): CampusAdmin
  + getStatistics(): Map<String, Object>
}

enum CampusStatus {
  ACTIVE
  INACTIVE
}

' 关联关系
User ||--o{ Campus : belongs to
Student ||--o{ Coach : selects
Coach ||--o{ Student : teaches
User ||--|| UserAccount : has
UserAccount ||--o{ Transaction : contains

@enduml
```

### 4.2 课程管理类图

```plantuml
@startuml 课程管理类图
!theme plain
skinparam backgroundColor white

title 课程管理类图

class Booking {
  - id: Long
  - studentId: Long
  - coachId: Long
  - bookingDate: Date
  - startTime: Time
  - endTime: Time
  - tableNumber: Integer
  - courseFee: BigDecimal
  - status: BookingStatus
  - createTime: DateTime
  - confirmTime: DateTime
  - cancelTime: DateTime
  - cancelReason: String
  
  + create(): Boolean
  + confirm(): Boolean
  + cancel(reason: String): Boolean
  + calculateFee(): BigDecimal
  + isWithin24Hours(): Boolean
  + reschedule(newDateTime: DateTime): Boolean
}

enum BookingStatus {
  PENDING
  CONFIRMED
  CANCELLED
  COMPLETED
  NO_SHOW
}

class Schedule {
  - id: Long
  - coachId: Long
  - dayOfWeek: Integer
  - startTime: Time
  - endTime: Time
  - isAvailable: Boolean
  - maxStudents: Integer
  - currentBookings: Integer
  
  + setAvailable(available: Boolean): void
  + getAvailableSlots(date: Date): List<TimeSlot>
  + addBooking(): Boolean
  + removeBooking(): Boolean
  + checkAvailability(): Boolean
}

class TimeSlot {
  - id: Long
  - startTime: Time
  - endTime: Time
  - isOccupied: Boolean
  - tableNumber: Integer
  - duration: Integer
  
  + isConflictWith(other: TimeSlot): Boolean
  + getDuration(): Integer
  + isValid(): Boolean
}

class Table {
  - id: Long
  - number: Integer
  - campusId: Long
  - status: TableStatus
  - location: String
  - maintenanceDate: Date
  
  + isAvailable(dateTime: DateTime): Boolean
  + reserve(booking: Booking): Boolean
  + release(): Boolean
  + setMaintenance(): Boolean
}

enum TableStatus {
  AVAILABLE
  OCCUPIED
  MAINTENANCE
  OUT_OF_SERVICE
}

class CoachStudentRelation {
  - id: Long
  - studentId: Long
  - coachId: Long
  - applyTime: DateTime
  - approveTime: DateTime
  - status: RelationStatus
  - notes: String
  
  + apply(): Boolean
  + approve(): Boolean
  + reject(reason: String): Boolean
  + terminate(): Boolean
  + getRelationDetails(): Map<String, Object>
}

enum RelationStatus {
  PENDING
  ESTABLISHED
  REJECTED
  TERMINATED
}

class TrainingEvaluation {
  - id: Long
  - bookingId: Long
  - studentEvaluation: String
  - coachEvaluation: String
  - studentRating: Integer
  - coachRating: Integer
  - createTime: DateTime
  - updateTime: DateTime
  
  + submitStudentEvaluation(evaluation: String): Boolean
  + submitCoachEvaluation(evaluation: String): Boolean
  + getEvaluationSummary(): Map<String, Object>
}

class Attendance {
  - id: Long
  - bookingId: Long
  - studentId: Long
  - coachId: Long
  - checkInTime: DateTime
  - checkOutTime: DateTime
  - status: AttendanceStatus
  - notes: String
  
  + checkIn(): Boolean
  + checkOut(): Boolean
  + markAbsent(): Boolean
}

enum AttendanceStatus {
  PRESENT
  ABSENT
  LATE
  EARLY_LEAVE
}

' 关联关系
Booking ||--|| CoachStudentRelation : based on
Booking ||--o| Table : uses
Booking ||--o| TrainingEvaluation : generates
Booking ||--|| Attendance : has
Schedule ||--o{ TimeSlot : contains
Coach ||--o{ Schedule : has
Campus ||--o{ Table : contains

@enduml
```

## 五、状态图设计

### 5.1 课程预约状态图

```plantuml
@startuml 课程预约状态图
!theme plain
skinparam backgroundColor white

title 课程预约状态图

[*] --> 待确认 : 学员提交预约

待确认 --> 已确认 : 教练确认预约
待确认 --> 已拒绝 : 教练拒绝预约
待确认 --> 已取消 : 学员取消预约

已确认 --> 已取消 : 双方协商取消\n(24小时前)
已确认 --> 进行中 : 课程开始时间到达
已确认 --> 已过期 : 超过开始时间未进行

进行中 --> 已完成 : 课程正常结束
进行中 --> 异常结束 : 课程异常中断

已完成 --> 已评价 : 双方完成评价

已拒绝 --> [*]
已取消 --> [*]
已过期 --> [*]
已评价 --> [*]

note right of 待确认 : 等待教练审核
note right of 已确认 : 已扣费，可正常上课
note right of 已取消 : 已退费
note right of 已完成 : 课程正常结束
note right of 已评价 : 流程完全结束

@enduml
```

### 5.2 教练审核状态图

```plantuml
@startuml 教练审核状态图
!theme plain
skinparam backgroundColor white

title 教练审核状态图

[*] --> 待提交 : 教练开始注册

待提交 --> 待审核 : 提交注册资料

待审核 --> 审核通过 : 管理员通过审核
待审核 --> 审核拒绝 : 管理员拒绝审核
待审核 --> 补充资料 : 管理员要求补充

补充资料 --> 待审核 : 重新提交资料

审核通过 --> 正常状态 : 激活账户
审核拒绝 --> [*] : 注册失败

正常状态 --> 冻结状态 : 管理员冻结
冻结状态 --> 正常状态 : 管理员解冻
正常状态 --> 注销状态 : 账户注销

注销状态 --> [*]

note right of 待审核 : 管理员审核资质
note right of 审核通过 : 可正常使用系统
note right of 冻结状态 : 暂停使用权限

@enduml
```



**说明：**
1. 以上UML图表使用PlantUML语法编写，可以通过PlantUML工具生成对应的图形
2. 图表涵盖了系统的主要功能模块和业务流程
3. 可根据实际开发需要进一步细化和调整图表内容
4. 建议在开发过程中持续更新和维护这些图表，确保与实际实现保持一致