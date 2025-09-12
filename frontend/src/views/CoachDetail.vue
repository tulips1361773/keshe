<template>
  <div class="coach-detail-page">
    <!-- 顶部导航栏 -->
    <div class="coach-header">
      <div class="header-content">
        <div class="back-section">
          <el-button type="primary" link @click="$router.go(-1)">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
        </div>
        
        <h1 class="page-title">教练员详情</h1>
        
        <div class="header-actions">
          <el-button type="primary" @click="contactCoach" v-if="coach">
            <el-icon><ChatDotRound /></el-icon>
            联系教练
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="coach-main" v-loading="loading">
      <div class="coach-container" v-if="coach">
        <!-- 教练基本信息卡片 -->
        <div class="coach-info-card custom-card">
          <div class="coach-avatar-section">
            <div class="avatar-container">
              <img :src="coach.avatar || '/default-avatar.png'" :alt="coach.real_name" class="coach-avatar" />
              <div class="status-badge">
                <el-tag :type="getStatusTagType(coach.status)" size="large">
                  {{ getStatusText(coach.status) }}
                </el-tag>
              </div>
            </div>
          </div>
          
          <div class="coach-basic-info">
            <h2 class="coach-name">{{ coach.real_name }}</h2>
            <p class="coach-level">{{ getLevelText(coach.coach_level) }}</p>
            
            <div class="coach-rating">
              <el-rate
                v-model="coach.rating"
                disabled
                show-score
                text-color="#ff9900"
                score-template="{value}"
              />
              <span class="rating-count">({{ coach.rating_count || 0 }}条评价)</span>
            </div>
            
            <div class="coach-stats">
              <div class="stat-item">
                <el-icon><UserFilled /></el-icon>
                <span>{{ coach.student_count || 0 }}名学员</span>
              </div>
              <div class="stat-item">
                <el-icon><Trophy /></el-icon>
                <span>{{ coach.experience_years || 0 }}年经验</span>
              </div>
              <div class="stat-item">
                <el-icon><Calendar /></el-icon>
                <span>{{ formatDate(coach.created_at) }}加入</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 联系信息卡片 -->
        <div class="contact-info-card custom-card">
          <h3 class="card-title">
            <el-icon><Phone /></el-icon>
            联系信息
          </h3>
          <div class="contact-content">
            <div class="contact-item">
              <label>手机号码：</label>
              <span>{{ coach.phone }}</span>
            </div>
            <div class="contact-item" v-if="coach.user_info && coach.user_info.email">
              <label>邮箱地址：</label>
              <span>{{ coach.user_info.email }}</span>
            </div>
            <div class="contact-item" v-if="coach.user_info && coach.user_info.username">
              <label>用户名：</label>
              <span>{{ coach.user_info.username }}</span>
            </div>
          </div>
        </div>
        
        <!-- 成就描述卡片 -->
        <div class="achievements-card custom-card">
          <h3 class="card-title">
            <el-icon><Medal /></el-icon>
            成就与经历
          </h3>
          <div class="achievements-content">
            <p v-if="coach.achievements">{{ coach.achievements }}</p>
            <p v-else class="no-achievements">该教练员暂未填写成就描述</p>
          </div>
        </div>
        
        <!-- 专业技能卡片 -->
        <div class="skills-card custom-card" v-if="coach.skills && coach.skills.length > 0">
          <h3 class="card-title">
            <el-icon><Star /></el-icon>
            专业技能
          </h3>
          <div class="skills-content">
            <el-tag
              v-for="skill in coach.skills"
              :key="skill"
              type="info"
              class="skill-tag"
            >
              {{ skill }}
            </el-tag>
          </div>
        </div>
        
        <!-- 课程信息卡片 -->
        <div class="courses-card custom-card" v-if="coach.courses && coach.courses.length > 0">
          <h3 class="card-title">
            <el-icon><Reading /></el-icon>
            授课课程
          </h3>
          <div class="courses-content">
            <div 
              v-for="course in coach.courses"
              :key="course.id"
              class="course-item"
              @click="viewCourse(course.id)"
            >
              <div class="course-info">
                <h4 class="course-title">{{ course.title }}</h4>
                <p class="course-description">{{ course.description }}</p>
                <div class="course-meta">
                  <span class="course-price">¥{{ course.price }}</span>
                  <span class="course-students">{{ course.student_count }}人学习</span>
                </div>
              </div>
              <el-button type="primary" size="small">
                查看详情
              </el-button>
            </div>
          </div>
        </div>
        
        <!-- 学员评价卡片 -->
        <div class="reviews-card custom-card" v-if="coach.reviews && coach.reviews.length > 0">
          <h3 class="card-title">
            <el-icon><ChatDotSquare /></el-icon>
            学员评价
          </h3>
          <div class="reviews-content">
            <div 
              v-for="review in coach.reviews"
              :key="review.id"
              class="review-item"
            >
              <div class="review-header">
                <div class="reviewer-info">
                  <img :src="review.student_avatar || '/default-avatar.png'" :alt="review.student_name" class="reviewer-avatar" />
                  <div class="reviewer-details">
                    <span class="reviewer-name">{{ review.student_name }}</span>
                    <el-rate v-model="review.rating" disabled size="small" />
                  </div>
                </div>
                <span class="review-date">{{ formatDate(review.created_at) }}</span>
              </div>
              <p class="review-content">{{ review.content }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-else-if="!loading" class="empty-state">
        <el-icon class="empty-icon"><UserFilled /></el-icon>
        <h3>教练员不存在</h3>
        <p>未找到该教练员信息</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowLeft,
  ChatDotRound,
  Phone,
  UserFilled,
  Trophy,
  Calendar,
  Medal,
  Star,
  Reading,
  ChatDotSquare
} from '@element-plus/icons-vue'
import api from '../utils/api'

export default {
  name: 'CoachDetail',
  components: {
    ArrowLeft,
    ChatDotRound,
    Phone,
    UserFilled,
    Trophy,
    Calendar,
    Medal,
    Star,
    Reading,
    ChatDotSquare
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const coach = ref(null)
    const loading = ref(false)
    
    // 获取教练员详情
    const fetchCoachDetail = async () => {
      try {
        loading.value = true
        const coachId = route.params.id
        const response = await api.get(`/accounts/coaches/${coachId}/`)
        
        if (response.data) {
          // 处理API返回的数据
          const data = response.data
          coach.value = {
            id: data.id,
            real_name: data.user?.real_name || data.user?.username || '未知教练',
            avatar: data.user?.avatar || '/default-avatar.png',
            coach_level: data.coach_level || 'junior',
            status: data.status || 'pending',
            phone: data.user?.phone || '未提供',
            user_info: {
              email: data.user?.email || '未提供',
              username: data.user?.username || '未提供'
            },
            created_at: data.created_at,
            rating: data.rating || 0,
            rating_count: data.rating_count || 0,
            student_count: data.student_count || 0,
            experience_years: data.experience_years || 0,
            achievements: data.achievements || '暂无成就描述',
            skills: data.skills || [],
            courses: data.courses || [],
            reviews: data.reviews || []
          }
        } else {
          throw new Error('获取教练员详情失败')
        }
      } catch (error) {
        console.error('获取教练员详情失败:', error)
        ElMessage.error(error.response?.data?.message || '获取教练员详情失败')
        
        // 如果API调用失败，使用模拟数据
        useMockData()
      } finally {
        loading.value = false
      }
    }
    
    // 使用模拟数据
    const useMockData = () => {
      const coachId = route.params.id
      
      coach.value = {
        id: coachId,
        real_name: '张教练',
        avatar: '/default-avatar.png',
        coach_level: 'senior',
        status: 'approved',
        phone: '138****8888',
        user_info: {
          email: 'zhang@example.com',
          username: 'zhang_coach'
        },
        created_at: '2023-01-15T00:00:00Z',
        rating: 4.8,
        rating_count: 156,
        student_count: 45,
        experience_years: 8,
        achievements: '国家二级运动员，多次获得省级比赛冠军，拥有丰富的教学经验。',
        skills: ['乒乓球基础教学', '技术指导', '比赛训练', '青少年培训'],
        courses: [
          {
            id: 1,
            title: '乒乓球基础入门课程',
            description: '适合初学者的乒乓球基础课程',
            price: 200,
            student_count: 12
          },
          {
            id: 2,
            title: '乒乓球进阶技巧课程',
            description: '提升乒乓球技巧的进阶课程',
            price: 300,
            student_count: 8
          }
        ],
        reviews: [
          {
            id: 1,
            student_name: '张同学',
            student_avatar: '/default-avatar.png',
            rating: 5,
            content: '教练非常专业，教学方法很好，进步很快！',
            created_at: '2024-01-15T00:00:00Z'
          },
          {
            id: 2,
            student_name: '李同学',
            student_avatar: '/default-avatar.png',
            rating: 4,
            content: '教练很耐心，技术指导很到位。',
            created_at: '2024-01-10T00:00:00Z'
          }
        ]
      }
    }
    
    // 联系教练
    const contactCoach = () => {
      ElMessage.info('联系教练功能开发中...')
    }
    
    // 查看课程详情
    const viewCourse = (courseId) => {
      router.push(`/courses/${courseId}`)
    }
    
    // 获取状态标签类型
    const getStatusTagType = (status) => {
      switch (status) {
        case 'approved': return 'success'
        case 'pending': return 'warning'
        case 'rejected': return 'danger'
        default: return 'info'
      }
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'approved': return '已通过审核'
        case 'pending': return '待审核'
        case 'rejected': return '审核未通过'
        default: return '未知状态'
      }
    }
    
    // 获取等级文本
    const getLevelText = (level) => {
      switch (level) {
        case 'junior': return '初级教练'
        case 'intermediate': return '中级教练'
        case 'senior': return '高级教练'
        case 'expert': return '专家教练'
        default: return '未设置等级'
      }
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未知时间'
      return new Date(dateString).toLocaleDateString('zh-CN')
    }
    
    onMounted(() => {
      fetchCoachDetail()
    })
    
    return {
      coach,
      loading,
      contactCoach,
      viewCourse,
      getStatusTagType,
      getStatusText,
      getLevelText,
      formatDate
    }
  }
}
</script>

<style scoped>
.coach-detail-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
}

.coach-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.back-section {
  flex: 1;
}

.page-title {
  flex: 2;
  text-align: center;
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.header-actions {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.coach-main {
  padding: 2rem 0;
}

.coach-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.custom-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  transition: all 0.3s ease;
}

.custom-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.coach-info-card {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.coach-avatar-section {
  flex-shrink: 0;
}

.avatar-container {
  position: relative;
  text-align: center;
}

.coach-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #fff;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.status-badge {
  position: absolute;
  top: -10px;
  right: -10px;
}

.coach-basic-info {
  flex: 1;
}

.coach-name {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.coach-level {
  font-size: 1.1rem;
  color: #7f8c8d;
  margin: 0 0 1rem 0;
}

.coach-rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.rating-count {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.coach-stats {
  display: flex;
  gap: 2rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #ecf0f1;
}

.contact-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.contact-item {
  display: flex;
  align-items: center;
}

.contact-item label {
  font-weight: 500;
  color: #2c3e50;
  width: 100px;
  flex-shrink: 0;
}

.contact-item span {
  color: #7f8c8d;
}

.achievements-content p {
  line-height: 1.6;
  color: #2c3e50;
  margin: 0;
}

.no-achievements {
  color: #95a5a6;
  font-style: italic;
}

.skills-content {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  margin: 0;
}

.courses-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.course-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.course-item:hover {
  background: #f8f9fa;
  border-color: #3498db;
}

.course-info {
  flex: 1;
}

.course-title {
  font-size: 1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.course-description {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.course-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #95a5a6;
}

.course-price {
  font-weight: 600;
  color: #e74c3c;
}

.reviews-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.review-item {
  padding: 1rem;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  background: #f8f9fa;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.reviewer-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.reviewer-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.reviewer-name {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
}

.review-date {
  color: #95a5a6;
  font-size: 0.8rem;
}

.review-content {
  color: #2c3e50;
  line-height: 1.5;
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #7f8c8d;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  color: #bdc3c7;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
}

.empty-state p {
  margin: 0;
  font-size: 0.9rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    padding: 0 1rem;
  }
  
  .back-section,
  .page-title,
  .header-actions {
    flex: none;
  }
  
  .coach-container {
    padding: 0 1rem;
  }
  
  .coach-info-card {
    flex-direction: column;
    text-align: center;
  }
  
  .coach-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .contact-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
  
  .contact-item label {
    width: auto;
  }
  
  .course-item {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .course-meta {
    justify-content: space-between;
  }
}
</style>