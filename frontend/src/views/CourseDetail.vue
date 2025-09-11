<template>
  <div class="course-detail-page">
    <!-- 顶部导航栏 -->
    <div class="course-header">
      <div class="header-content">
        <div class="back-section">
          <el-button type="primary" link @click="$router.go(-1)">
            <el-icon><ArrowLeft /></el-icon>
            返回课程列表
          </el-button>
        </div>
        
        <div class="header-actions">
          <el-button type="primary" @click="handleEnroll" :loading="enrolling">
            {{ course?.enrolled ? '继续学习' : '立即报名' }}
          </el-button>
        </div>
      </div>
    </div>

    <!-- 课程详情内容 -->
    <div class="course-detail-main" v-if="!loading && course">
      <div class="course-container">
        <!-- 课程基本信息 -->
        <div class="course-hero">
          <div class="course-image-section">
            <img :src="course.image" :alt="course.title" class="course-image" />
            <div class="course-badges">
              <el-tag :type="getLevelTagType(course.level)" size="large">
                {{ getLevelText(course.level) }}
              </el-tag>
              <el-tag type="info" size="large">
                {{ getTypeText(course.type) }}
              </el-tag>
            </div>
          </div>
          
          <div class="course-info-section">
            <h1 class="course-title">{{ course.title }}</h1>
            <p class="course-subtitle">{{ course.description }}</p>
            
            <div class="course-meta-grid">
              <div class="meta-item">
                <el-icon class="meta-icon"><User /></el-icon>
                <div class="meta-content">
                  <span class="meta-label">授课教练</span>
                  <span class="meta-value">{{ course.instructor }}</span>
                </div>
              </div>
              
              <div class="meta-item">
                <el-icon class="meta-icon"><Clock /></el-icon>
                <div class="meta-content">
                  <span class="meta-label">课程时长</span>
                  <span class="meta-value">{{ course.duration }}小时</span>
                </div>
              </div>
              
              <div class="meta-item">
                <el-icon class="meta-icon"><UserFilled /></el-icon>
                <div class="meta-content">
                  <span class="meta-label">学习人数</span>
                  <span class="meta-value">{{ course.students }}人</span>
                </div>
              </div>
              
              <div class="meta-item">
                <el-icon class="meta-icon"><Star /></el-icon>
                <div class="meta-content">
                  <span class="meta-label">课程评分</span>
                  <div class="rating-section">
                    <el-rate
                      v-model="course.rating"
                      disabled
                      show-score
                      text-color="#ff9900"
                      score-template="{value}"
                    />
                    <span class="rating-count">({{ course.ratingCount }}条评价)</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="price-section">
              <div class="price-info">
                <span v-if="course.originalPrice" class="original-price">¥{{ course.originalPrice }}</span>
                <span class="current-price">¥{{ course.price }}</span>
                <span v-if="course.originalPrice" class="discount">
                  省¥{{ course.originalPrice - course.price }}
                </span>
              </div>
              
              <el-button 
                type="primary" 
                size="large"
                class="enroll-button"
                @click="handleEnroll"
                :loading="enrolling"
              >
                {{ course.enrolled ? '继续学习' : '立即报名' }}
              </el-button>
            </div>
          </div>
        </div>
        
        <!-- 课程详细内容 -->
        <div class="course-content-section">
          <el-tabs v-model="activeTab" class="course-tabs">
            <!-- 课程介绍 -->
            <el-tab-pane label="课程介绍" name="introduction">
              <div class="tab-content">
                <div class="content-card custom-card">
                  <h3>课程简介</h3>
                  <p>{{ course.fullDescription }}</p>
                  
                  <h3>学习目标</h3>
                  <ul class="learning-objectives">
                    <li v-for="objective in course.objectives" :key="objective">
                      <el-icon class="objective-icon"><Check /></el-icon>
                      {{ objective }}
                    </li>
                  </ul>
                  
                  <h3>适合人群</h3>
                  <div class="target-audience">
                    <el-tag 
                      v-for="audience in course.targetAudience" 
                      :key="audience"
                      class="audience-tag"
                    >
                      {{ audience }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <!-- 课程大纲 -->
            <el-tab-pane label="课程大纲" name="curriculum">
              <div class="tab-content">
                <div class="content-card custom-card">
                  <div class="curriculum-list">
                    <div 
                      v-for="(chapter, index) in course.curriculum" 
                      :key="chapter.id"
                      class="curriculum-item"
                    >
                      <div class="chapter-header">
                        <div class="chapter-number">{{ index + 1 }}</div>
                        <div class="chapter-info">
                          <h4 class="chapter-title">{{ chapter.title }}</h4>
                          <p class="chapter-description">{{ chapter.description }}</p>
                          <div class="chapter-meta">
                            <span class="chapter-duration">
                              <el-icon><Clock /></el-icon>
                              {{ chapter.duration }}分钟
                            </span>
                            <span class="chapter-lessons">
                              <el-icon><VideoPlay /></el-icon>
                              {{ chapter.lessons }}节课
                            </span>
                          </div>
                        </div>
                        <div class="chapter-status">
                          <el-icon v-if="chapter.completed" class="status-icon completed">
                            <CircleCheckFilled />
                          </el-icon>
                          <el-icon v-else-if="chapter.locked" class="status-icon locked">
                            <Lock />
                          </el-icon>
                          <el-icon v-else class="status-icon available">
                            <VideoPlay />
                          </el-icon>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <!-- 学员评价 -->
            <el-tab-pane label="学员评价" name="reviews">
              <div class="tab-content">
                <div class="content-card custom-card">
                  <div class="reviews-summary">
                    <div class="rating-overview">
                      <div class="overall-rating">
                        <span class="rating-number">{{ course.rating }}</span>
                        <el-rate
                          v-model="course.rating"
                          disabled
                          show-score
                          text-color="#ff9900"
                        />
                      </div>
                      <div class="rating-distribution">
                        <div 
                          v-for="(count, star) in course.ratingDistribution" 
                          :key="star"
                          class="rating-bar"
                        >
                          <span class="star-label">{{ star }}星</span>
                          <div class="bar-container">
                            <div 
                              class="bar-fill" 
                              :style="{ width: (count / course.ratingCount * 100) + '%' }"
                            ></div>
                          </div>
                          <span class="count-label">{{ count }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="reviews-list">
                    <div 
                      v-for="review in course.reviews" 
                      :key="review.id"
                      class="review-item"
                    >
                      <div class="review-header">
                        <el-avatar :size="40" :src="review.avatar">
                          <el-icon><User /></el-icon>
                        </el-avatar>
                        <div class="reviewer-info">
                          <span class="reviewer-name">{{ review.name }}</span>
                          <div class="review-meta">
                            <el-rate
                              v-model="review.rating"
                              disabled
                              size="small"
                            />
                            <span class="review-date">{{ formatDate(review.date) }}</span>
                          </div>
                        </div>
                      </div>
                      <div class="review-content">
                        <p>{{ review.content }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-else-if="loading" class="loading-state">
      <el-skeleton :rows="8" animated />
    </div>
    
    <!-- 错误状态 -->
    <div v-else class="error-state">
      <el-empty description="课程不存在或加载失败" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowLeft,
  User,
  Clock,
  UserFilled,
  Star,
  Check,
  VideoPlay,
  CircleCheckFilled,
  Lock
} from '@element-plus/icons-vue'
import axios from '@/utils/axios'
import { useUserStore } from '@/stores/user'

export default {
  name: 'CourseDetail',
  components: {
    ArrowLeft,
    User,
    Clock,
    UserFilled,
    Star,
    Check,
    VideoPlay,
    CircleCheckFilled,
    Lock
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const userStore = useUserStore()
    const course = ref(null)
    const activeTab = ref('introduction')
    const enrolling = ref(false)
    const loading = ref(true)
    
    // API调用方法
    const loadCourseDetail = async () => {
      const courseId = route.params.id
      loading.value = true
      
      try {
        const response = await axios.get(`/api/courses/${courseId}/`)
        if (response.data) {
          course.value = {
            ...response.data,
            // 处理数据格式
            objectives: response.data.objectives || [],
            targetAudience: response.data.target_audience || [],
            curriculum: response.data.curriculum || [],
            reviews: response.data.reviews || [],
            ratingDistribution: response.data.rating_distribution || {},
            fullDescription: response.data.full_description || response.data.description
          }
        }
      } catch (error) {
        console.error('加载课程详情失败:', error)
        ElMessage.error('加载课程详情失败')
        router.push('/courses')
      } finally {
        loading.value = false
      }
    }
    
    const handleEnroll = async () => {
      if (!userStore.isAuthenticated) {
        ElMessage.warning('请先登录')
        router.push('/login')
        return
      }
      
      enrolling.value = true
      try {
        if (course.value.enrolled) {
          // 继续学习 - 跳转到学习页面
          ElMessage.success('开始学习！')
          // router.push(`/courses/${course.value.id}/learn`)
        } else {
          // 报名课程
          await axios.post(`/api/courses/${course.value.id}/enroll/`)
          ElMessage.success('报名成功！')
          course.value.enrolled = true
        }
      } catch (error) {
        console.error('操作失败:', error)
        const message = error.response?.data?.error || '操作失败，请重试'
        ElMessage.error(message)
      } finally {
        enrolling.value = false
      }
    }
    
    // 方法
    const getLevelTagType = (level) => {
      const typeMap = {
        'beginner': 'success',
        'intermediate': 'warning',
        'advanced': 'danger'
      }
      return typeMap[level] || 'info'
    }
    
    const getLevelText = (level) => {
      const textMap = {
        'beginner': '初级',
        'intermediate': '中级',
        'advanced': '高级'
      }
      return textMap[level] || '未知'
    }
    
    const getTypeText = (type) => {
      const textMap = {
        'basic': '基础课程',
        'advanced': '进阶课程',
        'professional': '专业课程'
      }
      return textMap[type] || '课程'
    }
    
    const formatDate = (date) => {
      return date.toLocaleDateString('zh-CN')
    }
    

    
    onMounted(() => {
      loadCourseDetail()
    })
    
    return {
      course,
      activeTab,
      enrolling,
      loading,
      getLevelTagType,
      getLevelText,
      getTypeText,
      formatDate,
      handleEnroll,
      loadCourseDetail
    }
  }
}
</script>

<style scoped>
.course-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
}

/* 顶部导航栏 */
.course-header {
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

/* 主要内容 */
.course-detail-main {
  padding: 24px;
}

.course-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 课程英雄区域 */
.course-hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.course-image-section {
  position: relative;
}

.course-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.course-badges {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.course-info-section {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.course-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
  margin: 0 0 16px 0;
  line-height: 1.2;
}

.course-subtitle {
  font-size: 1.2rem;
  color: #666;
  line-height: 1.6;
  margin: 0 0 32px 0;
}

.course-meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.meta-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.meta-icon {
  font-size: 1.5rem;
  color: #667eea;
  margin-top: 2px;
}

.meta-content {
  flex: 1;
}

.meta-label {
  display: block;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 4px;
}

.meta-value {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.rating-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rating-count {
  color: #666;
  font-size: 0.9rem;
}

.price-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  background: #f8f9fa;
  border-radius: 12px;
}

.price-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.original-price {
  color: #999;
  font-size: 1.1rem;
  text-decoration: line-through;
}

.current-price {
  color: #f56c6c;
  font-size: 2rem;
  font-weight: bold;
}

.discount {
  background: #f56c6c;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.enroll-button {
  height: 50px;
  padding: 0 32px;
  font-size: 1.1rem;
  font-weight: 600;
}

/* 课程内容区域 */
.course-content-section {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.course-tabs {
  padding: 0;
}

.tab-content {
  padding: 32px;
}

.content-card {
  padding: 0;
  box-shadow: none;
  border: none;
}

.content-card h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.content-card p {
  color: #666;
  line-height: 1.8;
  margin: 0 0 24px 0;
}

.learning-objectives {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
}

.learning-objectives li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 0;
  color: #333;
}

.objective-icon {
  color: #67c23a;
  margin-top: 2px;
}

.target-audience {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.audience-tag {
  margin: 0;
}

/* 课程大纲 */
.curriculum-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.curriculum-item {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
}

.chapter-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #fafafa;
}

.chapter-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.chapter-info {
  flex: 1;
}

.chapter-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.chapter-description {
  color: #666;
  margin: 0 0 8px 0;
}

.chapter-meta {
  display: flex;
  gap: 16px;
  font-size: 0.9rem;
  color: #666;
}

.chapter-duration,
.chapter-lessons {
  display: flex;
  align-items: center;
  gap: 4px;
}

.chapter-status {
  display: flex;
  align-items: center;
}

.status-icon {
  font-size: 1.5rem;
}

.status-icon.completed {
  color: #67c23a;
}

.status-icon.locked {
  color: #c0c4cc;
}

.status-icon.available {
  color: #409eff;
}

/* 评价区域 */
.reviews-summary {
  margin-bottom: 32px;
}

.rating-overview {
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

.overall-rating {
  text-align: center;
}

.rating-number {
  display: block;
  font-size: 3rem;
  font-weight: bold;
  color: #ff9900;
  margin-bottom: 8px;
}

.rating-distribution {
  flex: 1;
}

.rating-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.star-label {
  width: 40px;
  font-size: 0.9rem;
  color: #666;
}

.bar-container {
  flex: 1;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: #ff9900;
  transition: width 0.3s;
}

.count-label {
  width: 30px;
  text-align: right;
  font-size: 0.9rem;
  color: #666;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.review-item {
  padding: 20px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
}

.review-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.reviewer-info {
  flex: 1;
}

.reviewer-name {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.review-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.review-date {
  color: #666;
  font-size: 0.9rem;
}

.review-content p {
  color: #333;
  line-height: 1.6;
  margin: 0;
}

/* 加载状态 */
.loading-state {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 错误状态 */
.error-state {
  padding: 80px 40px;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .course-detail-main {
    padding: 16px;
  }
  
  .header-content {
    padding: 0 16px;
  }
  
  .course-hero {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .course-title {
    font-size: 2rem;
  }
  
  .course-meta-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .price-section {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .tab-content {
    padding: 20px;
  }
  
  .rating-overview {
    flex-direction: column;
    gap: 24px;
  }
}

@media (max-width: 480px) {
  .course-image {
    height: 250px;
  }
  
  .course-title {
    font-size: 1.5rem;
  }
  
  .chapter-header {
    padding: 16px;
  }
  
  .chapter-meta {
    flex-direction: column;
    gap: 8px;
  }
}
</style>