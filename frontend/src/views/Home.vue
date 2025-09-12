<template>
  <div class="home">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-brand">
          <el-icon class="brand-icon"><Basketball /></el-icon>
          <span class="brand-text">乒乓球培训管理系统</span>
        </div>
        <div class="nav-menu">
          <template v-if="!isAuthenticated">
            <el-button type="primary" @click="$router.push('/login')">
              <el-icon><User /></el-icon>
              登录
            </el-button>
            <el-button @click="$router.push('/register')">
              <el-icon><UserFilled /></el-icon>
              注册
            </el-button>
          </template>
          <template v-else>
            <el-button type="primary" @click="$router.push('/dashboard')">
              <el-icon><Monitor /></el-icon>
              进入系统
            </el-button>
            <el-button @click="handleLogout">
              <el-icon><SwitchButton /></el-icon>
              退出
            </el-button>
          </template>
        </div>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- 英雄区域 -->
      <section class="hero-section">
        <div class="hero-container">
          <div class="hero-content fade-in-up">
            <h1 class="hero-title">
              专业乒乓球培训
              <span class="highlight">管理系统</span>
            </h1>
            <p class="hero-subtitle">
              为乒乓球培训机构提供完整的学员管理、课程安排、教练管理解决方案
            </p>
            <div class="hero-actions">
              <el-button 
                type="primary" 
                size="large" 
                class="gradient-button"
                @click="$router.push('/register')"
                v-if="!isAuthenticated"
              >
                <el-icon><Star /></el-icon>
                立即注册
              </el-button>
              <el-button 
                type="primary" 
                size="large" 
                class="gradient-button"
                @click="$router.push('/dashboard')"
                v-else
              >
                <el-icon><Monitor /></el-icon>
                进入系统
              </el-button>
              <el-button size="large" @click="scrollToFeatures">
                <el-icon><ArrowDown /></el-icon>
                了解更多
              </el-button>
            </div>
          </div>
          <div class="hero-image">
            <div class="ping-pong-animation">
              <div class="ball"></div>
              <div class="paddle paddle-1"></div>
              <div class="paddle paddle-2"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- 功能特色区域 -->
      <section class="features-section" ref="featuresSection">
        <div class="container">
          <h2 class="section-title">系统功能特色</h2>
          <div class="features-grid">
            <div class="feature-card" v-for="feature in features" :key="feature.id">
              <div class="feature-icon">
                <el-icon><component :is="feature.icon" /></el-icon>
              </div>
              <h3 class="feature-title">{{ feature.title }}</h3>
              <p class="feature-description">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 统计数据区域 -->
      <section class="stats-section">
        <div class="container">
          <div class="stats-grid">
            <div class="stat-item" v-for="stat in stats" :key="stat.id">
              <div class="stat-number">{{ stat.number }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 用户类型介绍 -->
      <section class="user-types-section">
        <div class="container">
          <h2 class="section-title">适用用户</h2>
          <div class="user-types-grid">
            <div class="user-type-card" v-for="userType in userTypes" :key="userType.id">
              <div class="user-type-icon">
                <el-icon><component :is="userType.icon" /></el-icon>
              </div>
              <h3 class="user-type-title">{{ userType.title }}</h3>
              <ul class="user-type-features">
                <li v-for="feature in userType.features" :key="feature">
                  <el-icon><Check /></el-icon>
                  {{ feature }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <el-icon class="brand-icon"><Basketball /></el-icon>
            <span class="brand-text">乒乓球培训管理系统</span>
          </div>
          <div class="footer-info">
            <p>&copy; 2024 乒乓球培训管理系统. 保留所有权利.</p>
            <p>专业的培训管理解决方案</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import axios from '@/utils/axios'
import {
  Basketball,
  User,
  UserFilled,
  Monitor,
  SwitchButton,
  Star,
  ArrowDown,
  Check,
  Management,
  Calendar,
  CreditCard,
  Trophy,
  School,
  Avatar
} from '@element-plus/icons-vue'

export default {
  name: 'Home',
  components: {
    Basketball,
    User,
    UserFilled,
    Monitor,
    SwitchButton,
    Star,
    ArrowDown,
    Check,
    Management,
    Calendar,
    CreditCard,
    Trophy,
    School,
    Avatar
  },
  setup() {
    const userStore = useUserStore()
    const stats = ref([
      { id: 1, number: '1000+', label: '注册学员' },
      { id: 2, number: '50+', label: '专业教练' },
      { id: 3, number: '10+', label: '培训校区' },
      { id: 4, number: '5000+', label: '课程时数' }
    ])
    
    const isAuthenticated = computed(() => userStore.isAuthenticated)
    
    const features = [
      {
        id: 1,
        icon: 'Management',
        title: '学员管理',
        description: '完善的学员信息管理，包括注册、资料维护、学习进度跟踪等功能'
      },
      {
        id: 2,
        icon: 'Calendar',
        title: '课程安排',
        description: '灵活的课程安排系统，支持课程预约、时间管理、教练分配等'
      },
      {
        id: 3,
        icon: 'CreditCard',
        title: '支付管理',
        description: '集成支付系统，支持在线支付、费用管理、财务统计等功能'
      },
      {
        id: 4,
        icon: 'Trophy',
        title: '比赛管理',
        description: '比赛组织管理，包括报名、分组、赛程安排、成绩统计等'
      }
    ]
    
    // 加载统计数据
    const loadStats = async () => {
      try {
        const response = await axios.get('/accounts/api/stats/')
        if (response.data) {
          stats.value = [
            { id: 1, number: response.data.students || '1000+', label: '注册学员' },
            { id: 2, number: response.data.coaches || '50+', label: '专业教练' },
            { id: 3, number: response.data.campuses || '10+', label: '培训校区' },
            { id: 4, number: response.data.course_hours || '5000+', label: '课程时数' }
          ]
        }
      } catch (error) {
        console.log('加载统计数据失败，使用默认数据')
      }
    }
    
    const userTypes = [
      {
        id: 1,
        icon: 'School',
        title: '学员',
        features: [
          '在线注册和资料管理',
          '课程预约和时间安排',
          '教练选择和双选机制',
          '学习进度跟踪',
          '比赛报名参与'
        ]
      },
      {
        id: 2,
        icon: 'Avatar',
        title: '教练',
        features: [
          '个人资料和资质管理',
          '课程安排和学员管理',
          '教学进度跟踪',
          '收入统计查看',
          '学员评价反馈'
        ]
      },
      {
        id: 3,
        icon: 'Management',
        title: '管理员',
        features: [
          '校区信息管理',
          '教练审核和管理',
          '课程统筹安排',
          '财务数据统计',
          '系统运营监控'
        ]
      }
    ]
    
    const scrollToFeatures = () => {
      const element = document.querySelector('.features-section')
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
      }
    }
    
    const handleLogout = async () => {
      try {
        await userStore.logout()
        ElMessage.success('退出成功')
      } catch (error) {
        ElMessage.error('退出失败')
      }
    }
    
    onMounted(() => {
      loadStats()
    })
    
    return {
      isAuthenticated,
      features,
      stats,
      userTypes,
      scrollToFeatures,
      handleLogout
    }
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
}

.home::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="ping-pong" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="%23ffffff" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23ping-pong)"/></svg>') repeat;
  pointer-events: none;
}

/* 导航栏样式 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  padding: 0;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.brand-icon {
  font-size: 28px;
  color: #667eea;
}

.nav-menu {
  display: flex;
  gap: 15px;
}

/* 主要内容区域 */
.main-content {
  margin-top: 70px;
}

/* 英雄区域样式 */
.hero-section {
  min-height: 90vh;
  display: flex;
  align-items: center;
  padding: 80px 0;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.hero-content {
  text-align: left;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: bold;
  color: white;
  margin-bottom: 20px;
  line-height: 1.2;
}

.highlight {
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 40px;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

/* 乒乓球动画 */
.hero-image {
  display: flex;
  justify-content: center;
  align-items: center;
}

.ping-pong-animation {
  position: relative;
  width: 300px;
  height: 300px;
}

.ball {
  position: absolute;
  width: 40px;
  height: 40px;
  background: #ff6b6b;
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: bounce 2s ease-in-out infinite;
  box-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
}

.paddle {
  position: absolute;
  width: 80px;
  height: 120px;
  background: #8b4513;
  border-radius: 40px 40px 10px 10px;
}

.paddle-1 {
  top: 20px;
  left: 20px;
  transform: rotate(-30deg);
  animation: paddle1 2s ease-in-out infinite;
}

.paddle-2 {
  bottom: 20px;
  right: 20px;
  transform: rotate(150deg);
  animation: paddle2 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translate(-50%, -50%) translateY(0); }
  25% { transform: translate(-50%, -50%) translateY(-60px) translateX(-30px); }
  75% { transform: translate(-50%, -50%) translateY(60px) translateX(30px); }
}

@keyframes paddle1 {
  0%, 100% { transform: rotate(-30deg); }
  50% { transform: rotate(-10deg); }
}

@keyframes paddle2 {
  0%, 100% { transform: rotate(150deg); }
  50% { transform: rotate(170deg); }
}

/* 功能特色区域 */
.features-section {
  padding: 100px 0;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: bold;
  color: white;
  margin-bottom: 60px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 40px 30px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 3rem;
  color: #667eea;
  margin-bottom: 20px;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

.feature-description {
  color: #666;
  line-height: 1.6;
}

/* 统计数据区域 */
.stats-section {
  padding: 80px 0;
  background: rgba(255, 255, 255, 0.05);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
  text-align: center;
}

.stat-item {
  color: white;
}

.stat-number {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 10px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 1.1rem;
  opacity: 0.9;
}

/* 用户类型区域 */
.user-types-section {
  padding: 100px 0;
  background: rgba(255, 255, 255, 0.1);
}

.user-types-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
}

.user-type-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 40px 30px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.user-type-card:hover {
  transform: translateY(-5px);
}

.user-type-icon {
  font-size: 3rem;
  color: #667eea;
  margin-bottom: 20px;
}

.user-type-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 25px;
}

.user-type-features {
  list-style: none;
  padding: 0;
  text-align: left;
}

.user-type-features li {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  color: #666;
}

.user-type-features .el-icon {
  color: #67c23a;
  font-size: 16px;
}

/* 页脚样式 */
.footer {
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 40px 0;
  text-align: center;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: bold;
}

.footer-info p {
  margin: 5px 0;
  opacity: 0.8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .nav-container {
    padding: 0 15px;
  }
  
  .nav-menu {
    gap: 10px;
  }
  
  .hero-actions {
    justify-content: center;
  }
  
  .ping-pong-animation {
    width: 200px;
    height: 200px;
  }
}
</style>