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
    <div class="course-detail-main" v-if="course">
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
    <div v-else class="loading-state">
      <el-skeleton :rows="8" animated />
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
    const course = ref(null)
    const activeTab = ref('introduction')
    const enrolling = ref(false)
    
    // 模拟课程详情数据
    const mockCourseData = {
      1: {
        id: 1,
        title: '乒乓球基础入门',
        description: '从零开始学习乒乓球，掌握基本握拍、发球和接球技巧',
        fullDescription: '本课程专为乒乓球初学者设计，通过系统的理论讲解和实践训练，帮助学员从零基础开始，逐步掌握乒乓球的基本技能。课程内容包括握拍方法、基本站位、发球技术、接球技巧等核心内容，让您在轻松愉快的氛围中快速入门乒乓球运动。',
        image: 'https://via.placeholder.com/600x400?text=乒乓球基础入门',
        instructor: '张教练',
        duration: 20,
        level: 'beginner',
        type: 'basic',
        rating: 4.8,
        ratingCount: 156,
        students: 1200,
        price: 299,
        originalPrice: 399,
        enrolled: false,
        objectives: [
          '掌握正确的握拍方法和基本站位',
          '学会基础发球技术，包括正手发球和反手发球',
          '熟练掌握正手和反手的基本击球动作',
          '了解乒乓球比赛的基本规则和礼仪',
          '培养良好的运动习惯和安全意识'
        ],
        targetAudience: ['乒乓球零基础学员', '想要系统学习的初学者', '希望纠正错误动作的学员'],
        curriculum: [
          {
            id: 1,
            title: '乒乓球基础知识',
            description: '了解乒乓球运动的历史、规则和基本装备',
            duration: 45,
            lessons: 3,
            completed: true,
            locked: false
          },
          {
            id: 2,
            title: '握拍方法与基本站位',
            description: '学习正确的握拍方法和标准的基本站位',
            duration: 60,
            lessons: 4,
            completed: false,
            locked: false
          },
          {
            id: 3,
            title: '正手基本技术',
            description: '掌握正手攻球、正手推挡等基本技术',
            duration: 90,
            lessons: 6,
            completed: false,
            locked: true
          }
        ],
        ratingDistribution: {
          5: 98,
          4: 45,
          3: 10,
          2: 2,
          1: 1
        },
        reviews: [
          {
            id: 1,
            name: '学员小王',
            avatar: '',
            rating: 5,
            date: new Date('2024-01-15'),
            content: '张教练讲解得非常详细，从最基础的握拍开始教，很适合我这种零基础的学员。课程安排合理，循序渐进，现在已经能打几个回合了！'
          },
          {
            id: 2,
            name: '乒乓球爱好者',
            avatar: '',
            rating: 4,
            date: new Date('2024-01-10'),
            content: '课程内容很全面，教练的示范动作很标准。不过希望能增加一些实战练习的内容。'
          }
        ]
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
    
    const handleEnroll = async () => {
      enrolling.value = true
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        if (course.value.enrolled) {
          ElMessage.success('开始学习！')
          // 跳转到学习页面
        } else {
          ElMessage.success('报名成功！')
          course.value.enrolled = true
        }
      } catch (error) {
        ElMessage.error('操作失败，请重试')
      } finally {
        enrolling.value = false
      }
    }
    
    const loadCourseDetail = async () => {
      const courseId = parseInt(route.params.id)
      
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 500))
        
        const courseData = mockCourseData[courseId]
        if (courseData) {
          course.value = courseData
        } else {
          ElMessage.error('课程不存在')
          router.push('/courses')
        }
      } catch (error) {
        ElMessage.error('加载课程详情失败')
        router.push('/courses')
      }
    }
    
    onMounted(() => {
      loadCourseDetail()
    })
    
    return {
      course,
      activeTab,
      enrolling,
      getLevelTagType,
      getLevelText,
      getTypeText,
      formatDate,
      handleEnroll
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