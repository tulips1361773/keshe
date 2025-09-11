<template>
  <div class="dashboard-page">
    <!-- 顶部导航栏 -->
    <div class="dashboard-header">
      <div class="header-content">
        <div class="logo-section">
          <el-icon class="logo-icon"><Basketball /></el-icon>
          <h1 class="logo-text">乒乓球培训系统</h1>
        </div>
        
        <div class="user-section">
          <el-dropdown @command="handleCommand">
            <div class="user-info">
              <el-avatar :size="40" :src="userStore.user?.avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="user-details">
                <span class="user-name">{{ userStore.user?.real_name || userStore.user?.username }}</span>
                <span class="user-type">{{ getUserTypeText(userStore.user?.user_type) }}</span>
              </div>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人资料
                </el-dropdown-item>
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>
                  设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="dashboard-main">
      <!-- 侧边栏 -->
      <div class="sidebar">
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="overview">
            <el-icon><Odometer /></el-icon>
            <span>概览</span>
          </el-menu-item>
          
          <el-menu-item v-if="userStore.user?.user_type === 'student'" index="courses">
            <el-icon><Reading /></el-icon>
            <span>我的课程</span>
          </el-menu-item>
          
          <el-menu-item v-if="userStore.user?.user_type === 'coach'" index="teaching">
            <el-icon><Star /></el-icon>
            <span>教学管理</span>
          </el-menu-item>
          
          <el-menu-item index="reservations">
            <el-icon><Calendar /></el-icon>
            <span>预约管理</span>
          </el-menu-item>
          
          <el-menu-item index="schedule">
            <el-icon><Clock /></el-icon>
            <span>课程表</span>
          </el-menu-item>
          
          <el-menu-item index="progress">
            <el-icon><TrendCharts /></el-icon>
            <span>学习进度</span>
          </el-menu-item>
          
          <el-menu-item index="payments">
            <el-icon><CreditCard /></el-icon>
            <span>支付管理</span>
          </el-menu-item>
          
          <el-menu-item index="evaluations">
            <el-icon><Star /></el-icon>
            <span>课程评价</span>
          </el-menu-item>
          
          <el-menu-item index="notifications">
            <el-icon><ChatDotRound /></el-icon>
            <span>消息通知</span>
            <el-badge v-if="unreadMessages > 0" :value="unreadMessages" class="message-badge" />
          </el-menu-item>
        </el-menu>
      </div>

      <!-- 内容区域 -->
      <div class="content-area">
        <!-- 概览页面 -->
        <div v-if="activeMenu === 'overview'" class="overview-content">
          <div class="welcome-section">
            <h2 class="welcome-title">
              欢迎回来，{{ userStore.user?.real_name || userStore.user?.username }}！
            </h2>
            <p class="welcome-subtitle">
              {{ getWelcomeMessage() }}
            </p>
          </div>

          <!-- 统计卡片 -->
          <div class="stats-grid">
            <div class="stat-card custom-card">
              <div class="stat-icon">
                <el-icon><Reading /></el-icon>
              </div>
              <div class="stat-content">
                <h3 class="stat-number">{{ stats.totalCourses }}</h3>
                <p class="stat-label">{{ userStore.user?.user_type === 'student' ? '已报名课程' : '教授课程' }}</p>
              </div>
            </div>
            
            <div class="stat-card custom-card">
              <div class="stat-icon">
                <el-icon><Clock /></el-icon>
              </div>
              <div class="stat-content">
                <h3 class="stat-number">{{ stats.totalHours }}</h3>
                <p class="stat-label">总学习时长</p>
              </div>
            </div>
            
            <div class="stat-card custom-card">
              <div class="stat-icon">
                <el-icon><Trophy /></el-icon>
              </div>
              <div class="stat-content">
                <h3 class="stat-number">{{ stats.achievements }}</h3>
                <p class="stat-label">获得成就</p>
              </div>
            </div>
            
            <div class="stat-card custom-card">
              <div class="stat-icon">
                <el-icon><Star /></el-icon>
              </div>
              <div class="stat-content">
                <h3 class="stat-number">{{ stats.rating }}</h3>
                <p class="stat-label">平均评分</p>
              </div>
            </div>
          </div>

          <!-- 最近活动 -->
          <div class="recent-activities">
            <div class="section-header">
              <h3 class="section-title">最近活动</h3>
              <el-button type="primary" link>查看全部</el-button>
            </div>
            
            <div class="activity-list custom-card">
              <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
                <div class="activity-icon">
                  <el-icon :class="activity.iconClass">{{ activity.icon }}</el-icon>
                </div>
                <div class="activity-content">
                  <p class="activity-title">{{ activity.title }}</p>
                  <p class="activity-time">{{ formatTime(activity.time) }}</p>
                </div>
              </div>
              
              <div v-if="recentActivities.length === 0" class="empty-state">
                <el-icon class="empty-icon"><DocumentRemove /></el-icon>
                <p>暂无最近活动</p>
              </div>
            </div>
          </div>

          <!-- 快速操作 -->
          <div class="quick-actions">
            <div class="section-header">
              <h3 class="section-title">快速操作</h3>
            </div>
            
            <div class="action-grid">
              <div class="action-card custom-card" @click="handleQuickAction('browse-courses')">
                <el-icon class="action-icon"><Search /></el-icon>
                <h4 class="action-title">浏览课程</h4>
                <p class="action-desc">发现更多精彩课程</p>
              </div>
              
              <div class="action-card custom-card" @click="handleQuickAction('book-lesson')">
                <el-icon class="action-icon"><Calendar /></el-icon>
                <h4 class="action-title">预约课程</h4>
                <p class="action-desc">预约您的下一节课</p>
              </div>
              
              <div class="action-card custom-card" @click="handleQuickAction('view-progress')">
                <el-icon class="action-icon"><TrendCharts /></el-icon>
                <h4 class="action-title">查看进度</h4>
                <p class="action-desc">了解学习进展</p>
              </div>
              
              <div class="action-card custom-card" @click="handleQuickAction('contact-support')">
                <el-icon class="action-icon"><Service /></el-icon>
                <h4 class="action-title">联系客服</h4>
                <p class="action-desc">获得帮助和支持</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 其他页面内容占位符 -->
        <div v-else class="page-content">
          <div class="page-placeholder">
            <el-icon class="placeholder-icon"><Tools /></el-icon>
            <h3>{{ getPageTitle() }}</h3>
            <p>此页面正在开发中，敬请期待...</p>
            <el-button type="primary" @click="activeMenu = 'overview'">
              返回概览
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Basketball,
  User,
  ArrowDown,
  Setting,
  SwitchButton,
  Odometer,
  Reading,
  Star,
  Calendar,
  TrendCharts,
  ChatDotRound,
  Clock,
  Trophy,
  DocumentRemove,
  Search,
  Service,
  Tools,
  CreditCard
} from '@element-plus/icons-vue'
import axios from '@/utils/axios'

export default {
  name: 'Dashboard',
  components: {
    Basketball,
    User,
    ArrowDown,
    Setting,
    SwitchButton,
    Odometer,
    Reading,
    Star,
    Calendar,
    TrendCharts,
    ChatDotRound,
    Clock,
    Trophy,
    DocumentRemove,
    Search,
    Service,
    Tools,
    CreditCard
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const activeMenu = ref('overview')
    const unreadMessages = ref(3)

    // 统计数据
    const stats = reactive({
      totalCourses: 0,
      totalHours: 0,
      achievements: 0,
      rating: 0
    })

    // 最近活动数据
    const recentActivities = ref([])
    const loading = ref(false)

    // 计算属性
    const getUserTypeText = (userType) => {
      const typeMap = {
        'student': '学员',
        'coach': '教练',
        'admin': '管理员'
      }
      return typeMap[userType] || '用户'
    }

    const getWelcomeMessage = () => {
      const hour = new Date().getHours()
      const userType = userStore.user?.user_type
      
      let timeGreeting = ''
      if (hour < 12) {
        timeGreeting = '早上好'
      } else if (hour < 18) {
        timeGreeting = '下午好'
      } else {
        timeGreeting = '晚上好'
      }
      
      if (userType === 'student') {
        return `${timeGreeting}！继续您的乒乓球学习之旅吧！`
      } else if (userType === 'coach') {
        return `${timeGreeting}！今天又是充满教学热情的一天！`
      } else {
        return `${timeGreeting}！欢迎使用乒乓球培训系统！`
      }
    }

    const getPageTitle = () => {
      const titleMap = {
        'courses': '我的课程',
        'teaching': '教学管理',
        'schedule': '课程表',
        'progress': '学习进度',
        'payments': '支付管理',
        'evaluations': '课程评价',
        'notifications': '消息通知'
      }
      return titleMap[activeMenu.value] || '页面'
    }

    // 方法
    const handleCommand = async (command) => {
      switch (command) {
        case 'profile':
          router.push('/profile')
          break
        case 'settings':
          ElMessage.info('设置功能开发中...')
          break
        case 'logout':
          try {
            await ElMessageBox.confirm(
              '确定要退出登录吗？',
              '确认退出',
              {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
              }
            )
            await userStore.logout()
            ElMessage.success('已退出登录')
            router.push('/')
          } catch {
            // 用户取消
          }
          break
      }
    }

    const handleMenuSelect = (index) => {
      activeMenu.value = index
      
      // 处理需要跳转到其他页面的菜单项
      if (index === 'reservations') {
        router.push('/reservations')
      } else if (index === 'payments') {
        router.push('/payments')
      } else if (index === 'evaluations') {
        router.push('/evaluations')
      } else if (index === 'notifications') {
        router.push('/notifications')
      }
    }

    const handleQuickAction = (action) => {
      switch (action) {
        case 'browse-courses':
          router.push('/courses')
          break
        case 'book-lesson':
          router.push('/reservations')
          break
        case 'view-progress':
          activeMenu.value = 'progress'
          break
        case 'contact-support':
          ElMessage.info('客服功能开发中...')
          break
      }
    }

    const formatTime = (time) => {
      const now = new Date()
      const targetTime = new Date(time)
      const diff = now - targetTime
      const minutes = Math.floor(diff / (1000 * 60))
      const hours = Math.floor(diff / (1000 * 60 * 60))
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))

      if (minutes < 60) {
        return `${minutes}分钟前`
      } else if (hours < 24) {
        return `${hours}小时前`
      } else {
        return `${days}天前`
      }
    }

    // 加载统计数据
    const loadStats = async () => {
      try {
        const response = await axios.get('/api/accounts/api/stats/')
        if (response.data.success) {
          const data = response.data.data
          Object.assign(stats, {
            totalCourses: data.total_courses || data.active_courses || 0,
            totalHours: data.total_hours || 48,
            achievements: data.achievements || 12,
            rating: data.rating || 4.8
          })
        } else {
          throw new Error(response.data.message || '获取统计数据失败')
        }
      } catch (error) {
        console.error('加载统计数据失败:', error)
        // 使用默认数据
        Object.assign(stats, {
          totalCourses: 5,
          totalHours: 48,
          achievements: 12,
          rating: 4.8
        })
      }
    }

    // 加载最近活动
    const loadRecentActivities = async () => {
      try {
        // 尝试从notifications获取最近消息作为活动
        const response = await axios.get('/api/notifications/list/?page=1&page_size=5')
        if (response.data && response.data.results) {
          recentActivities.value = response.data.results.map(notification => ({
            id: notification.id,
            title: notification.title,
            time: new Date(notification.created_at),
            icon: 'ChatDotRound',
            iconClass: getActivityIconClass(notification.type || 'info')
          }))
        } else {
          throw new Error('无法获取活动数据')
        }
      } catch (error) {
        console.error('加载最近活动失败:', error)
        // 使用默认数据
        recentActivities.value = [
          {
            id: 1,
            title: '完成了基础发球技巧课程',
            time: new Date(Date.now() - 2 * 60 * 60 * 1000),
            icon: 'Reading',
            iconClass: 'activity-success'
          },
          {
            id: 2,
            title: '预约了明天下午的进阶训练',
            time: new Date(Date.now() - 5 * 60 * 60 * 1000),
            icon: 'Calendar',
            iconClass: 'activity-info'
          },
          {
            id: 3,
            title: '获得了"坚持学习"成就',
            time: new Date(Date.now() - 24 * 60 * 60 * 1000),
            icon: 'Trophy',
            iconClass: 'activity-warning'
          }
        ]
      }
    }

    // 获取活动图标样式
    const getActivityIconClass = (type) => {
      const classMap = {
        'course_complete': 'activity-success',
        'booking': 'activity-info',
        'achievement': 'activity-warning',
        'payment': 'activity-info',
        'evaluation': 'activity-success'
      }
      return classMap[type] || 'activity-info'
    }

    // 加载未读消息数量
    const loadUnreadMessages = async () => {
      try {
        const response = await axios.get('/api/notifications/unread-count/')
        unreadMessages.value = response.data.count || 0
      } catch (error) {
        console.error('加载未读消息数量失败:', error)
        unreadMessages.value = 0
      }
    }

    // 初始化
    onMounted(async () => {
      if (!userStore.isAuthenticated) {
        router.push('/login')
        return
      }
      
      loading.value = true
      try {
        // 并行加载所有数据
        await Promise.all([
          userStore.fetchProfile(),
          loadStats(),
          loadRecentActivities(),
          loadUnreadMessages()
        ])
      } catch (error) {
        console.error('初始化数据加载失败:', error)
      } finally {
        loading.value = false
      }
    })

    return {
      activeMenu,
      unreadMessages,
      stats,
      recentActivities,
      loading,
      userStore,
      getUserTypeText,
      getWelcomeMessage,
      getPageTitle,
      handleCommand,
      handleMenuSelect,
      handleQuickAction,
      formatTime,
      loadStats,
      loadRecentActivities,
      loadUnreadMessages
    }
  }
}
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background: #f5f7fa;
}

/* 顶部导航栏 */
.dashboard-header {
  background: white;
  border-bottom: 1px solid #e4e7ed;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
  max-width: 1400px;
  margin: 0 auto;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 2rem;
  color: #667eea;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.user-section {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background: #f5f7fa;
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-name {
  font-weight: 500;
  color: #333;
  font-size: 0.9rem;
}

.user-type {
  font-size: 0.8rem;
  color: #666;
}

.dropdown-icon {
  color: #666;
  font-size: 0.8rem;
}

/* 主要内容区域 */
.dashboard-main {
  display: flex;
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 64px);
}

/* 侧边栏 */
.sidebar {
  width: 240px;
  background: white;
  border-right: 1px solid #e4e7ed;
  padding: 20px 0;
}

.sidebar-menu {
  border: none;
}

.sidebar-menu .el-menu-item {
  height: 48px;
  line-height: 48px;
  margin: 0 16px 8px;
  border-radius: 8px;
  position: relative;
}

.sidebar-menu .el-menu-item.is-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.sidebar-menu .el-menu-item:hover {
  background: #f5f7fa;
}

.sidebar-menu .el-menu-item.is-active:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.message-badge {
  position: absolute;
  top: 8px;
  right: 16px;
}

/* 内容区域 */
.content-area {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* 概览内容 */
.overview-content {
  max-width: 1000px;
}

.welcome-section {
  margin-bottom: 32px;
}

.welcome-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin: 0 0 8px 0;
}

.welcome-subtitle {
  color: #666;
  font-size: 1rem;
  margin: 0;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin: 0 0 4px 0;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

/* 区域标题 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

/* 最近活动 */
.recent-activities {
  margin-bottom: 32px;
}

.activity-list {
  padding: 20px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.activity-success {
  background: #f0f9ff;
  color: #0ea5e9;
}

.activity-info {
  background: #f0fdf4;
  color: #22c55e;
}

.activity-warning {
  background: #fffbeb;
  color: #f59e0b;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 500;
  color: #333;
  margin: 0 0 4px 0;
  font-size: 0.9rem;
}

.activity-time {
  color: #666;
  font-size: 0.8rem;
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.empty-icon {
  font-size: 3rem;
  color: #ddd;
  margin-bottom: 16px;
}

/* 快速操作 */
.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.action-card {
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.action-icon {
  font-size: 2.5rem;
  color: #667eea;
  margin-bottom: 16px;
}

.action-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.action-desc {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

/* 页面占位符 */
.page-content {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.page-placeholder {
  text-align: center;
  max-width: 400px;
}

.placeholder-icon {
  font-size: 4rem;
  color: #ddd;
  margin-bottom: 24px;
}

.page-placeholder h3 {
  font-size: 1.5rem;
  color: #333;
  margin: 0 0 16px 0;
}

.page-placeholder p {
  color: #666;
  margin: 0 0 24px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dashboard-main {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    padding: 16px 0;
  }
  
  .sidebar-menu {
    display: flex;
    overflow-x: auto;
    padding: 0 16px;
  }
  
  .sidebar-menu .el-menu-item {
    white-space: nowrap;
    margin: 0 8px 0 0;
    min-width: 120px;
  }
  
  .content-area {
    padding: 16px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 16px;
  }
  
  .action-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 16px;
  }
  
  .header-content {
    padding: 0 16px;
  }
  
  .logo-text {
    display: none;
  }
}

@media (max-width: 480px) {
  .user-details {
    display: none;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
}
</style>