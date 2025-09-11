<template>
  <div class="courses-page">
    <!-- 顶部导航栏 -->
    <div class="courses-header">
      <div class="header-content">
        <div class="back-section">
          <el-button type="primary" link @click="$router.go(-1)">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
        </div>
        
        <h1 class="page-title">课程中心</h1>
        
        <div class="header-actions">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索课程..."
            style="width: 200px"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="courses-main">
      <div class="courses-container">
        <!-- 筛选器 -->
        <div class="filters-section custom-card">
          <div class="filters-content">
            <div class="filter-group">
              <label class="filter-label">课程类型：</label>
              <el-radio-group v-model="filters.type" @change="handleFilterChange">
                <el-radio-button label="all">全部</el-radio-button>
                <el-radio-button label="basic">基础课程</el-radio-button>
                <el-radio-button label="advanced">进阶课程</el-radio-button>
                <el-radio-button label="professional">专业课程</el-radio-button>
              </el-radio-group>
            </div>
            
            <div class="filter-group">
              <label class="filter-label">难度等级：</label>
              <el-radio-group v-model="filters.level" @change="handleFilterChange">
                <el-radio-button label="all">全部</el-radio-button>
                <el-radio-button label="beginner">初级</el-radio-button>
                <el-radio-button label="intermediate">中级</el-radio-button>
                <el-radio-button label="advanced">高级</el-radio-button>
              </el-radio-group>
            </div>
            
            <div class="filter-group">
              <label class="filter-label">排序方式：</label>
              <el-select v-model="filters.sort" @change="handleFilterChange" style="width: 120px">
                <el-option label="最新" value="newest" />
                <el-option label="最热" value="popular" />
                <el-option label="评分" value="rating" />
                <el-option label="价格" value="price" />
              </el-select>
            </div>
          </div>
        </div>

        <!-- 课程列表 -->
        <div class="courses-grid">
          <div 
            v-for="course in filteredCourses" 
            :key="course.id" 
            class="course-card custom-card"
            @click="viewCourse(course.id)"
          >
            <div class="course-image">
              <img :src="course.image" :alt="course.title" />
              <div class="course-badge">
                <el-tag :type="getLevelTagType(course.level)" size="small">
                  {{ getLevelText(course.level) }}
                </el-tag>
              </div>
            </div>
            
            <div class="course-content">
              <h3 class="course-title">{{ course.title }}</h3>
              <p class="course-description">{{ course.description }}</p>
              
              <div class="course-meta">
                <div class="course-instructor">
                  <el-icon><User /></el-icon>
                  <span>{{ course.instructor }}</span>
                </div>
                
                <div class="course-duration">
                  <el-icon><Clock /></el-icon>
                  <span>{{ course.duration }}小时</span>
                </div>
              </div>
              
              <div class="course-stats">
                <div class="course-rating">
                  <el-rate
                    v-model="course.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}"
                  />
                  <span class="rating-count">({{ course.ratingCount }})</span>
                </div>
                
                <div class="course-students">
                  <el-icon><UserFilled /></el-icon>
                  <span>{{ course.students }}人学习</span>
                </div>
              </div>
              
              <div class="course-footer">
                <div class="course-price">
                  <span v-if="course.originalPrice" class="original-price">¥{{ course.originalPrice }}</span>
                  <span class="current-price">¥{{ course.price }}</span>
                </div>
                
                <el-button 
                  type="primary" 
                  size="small"
                  @click.stop="enrollCourse(course.id)"
                >
                  {{ course.enrolled ? '继续学习' : '立即报名' }}
                </el-button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-if="filteredCourses.length === 0" class="empty-state">
          <el-icon class="empty-icon"><DocumentRemove /></el-icon>
          <h3>暂无课程</h3>
          <p>没有找到符合条件的课程，请尝试调整筛选条件</p>
        </div>
        
        <!-- 分页 -->
        <div v-if="filteredCourses.length > 0" class="pagination-section">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[12, 24, 48]"
            :total="totalCourses"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowLeft,
  Search,
  User,
  Clock,
  UserFilled,
  DocumentRemove
} from '@element-plus/icons-vue'

export default {
  name: 'Courses',
  components: {
    ArrowLeft,
    Search,
    User,
    Clock,
    UserFilled,
    DocumentRemove
  },
  setup() {
    const router = useRouter()
    const searchKeyword = ref('')
    const currentPage = ref(1)
    const pageSize = ref(12)
    const totalCourses = ref(0)
    
    const filters = reactive({
      type: 'all',
      level: 'all',
      sort: 'newest'
    })
    
    // 模拟课程数据
    const courses = ref([
      {
        id: 1,
        title: '乒乓球基础入门',
        description: '从零开始学习乒乓球，掌握基本握拍、发球和接球技巧',
        image: 'https://via.placeholder.com/300x200?text=基础入门',
        instructor: '张教练',
        duration: 20,
        level: 'beginner',
        type: 'basic',
        rating: 4.8,
        ratingCount: 156,
        students: 1200,
        price: 299,
        originalPrice: 399,
        enrolled: false
      },
      {
        id: 2,
        title: '正手攻球技术',
        description: '深入学习正手攻球技术，提高击球力量和准确性',
        image: 'https://via.placeholder.com/300x200?text=正手攻球',
        instructor: '李教练',
        duration: 15,
        level: 'intermediate',
        type: 'advanced',
        rating: 4.9,
        ratingCount: 89,
        students: 800,
        price: 399,
        originalPrice: 499,
        enrolled: true
      },
      {
        id: 3,
        title: '反手技术精进',
        description: '掌握反手推挡、拉球等技术，完善技术体系',
        image: 'https://via.placeholder.com/300x200?text=反手技术',
        instructor: '王教练',
        duration: 18,
        level: 'intermediate',
        type: 'advanced',
        rating: 4.7,
        ratingCount: 124,
        students: 950,
        price: 359,
        originalPrice: null,
        enrolled: false
      },
      {
        id: 4,
        title: '发球技术大全',
        description: '学习各种发球技术，包括下旋、上旋、侧旋等',
        image: 'https://via.placeholder.com/300x200?text=发球技术',
        instructor: '赵教练',
        duration: 12,
        level: 'beginner',
        type: 'basic',
        rating: 4.6,
        ratingCount: 203,
        students: 1500,
        price: 199,
        originalPrice: 299,
        enrolled: false
      },
      {
        id: 5,
        title: '专业比赛战术',
        description: '学习专业比赛中的战术运用和心理调节',
        image: 'https://via.placeholder.com/300x200?text=比赛战术',
        instructor: '陈教练',
        duration: 25,
        level: 'advanced',
        type: 'professional',
        rating: 4.9,
        ratingCount: 67,
        students: 450,
        price: 599,
        originalPrice: 799,
        enrolled: false
      },
      {
        id: 6,
        title: '步法训练专项',
        description: '系统训练乒乓球步法，提高移动速度和灵活性',
        image: 'https://via.placeholder.com/300x200?text=步法训练',
        instructor: '刘教练',
        duration: 16,
        level: 'intermediate',
        type: 'advanced',
        rating: 4.8,
        ratingCount: 98,
        students: 720,
        price: 329,
        originalPrice: null,
        enrolled: false
      }
    ])
    
    // 计算属性
    const filteredCourses = computed(() => {
      let result = courses.value
      
      // 搜索过滤
      if (searchKeyword.value) {
        result = result.filter(course => 
          course.title.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
          course.description.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
          course.instructor.toLowerCase().includes(searchKeyword.value.toLowerCase())
        )
      }
      
      // 类型过滤
      if (filters.type !== 'all') {
        result = result.filter(course => course.type === filters.type)
      }
      
      // 难度过滤
      if (filters.level !== 'all') {
        result = result.filter(course => course.level === filters.level)
      }
      
      // 排序
      switch (filters.sort) {
        case 'popular':
          result.sort((a, b) => b.students - a.students)
          break
        case 'rating':
          result.sort((a, b) => b.rating - a.rating)
          break
        case 'price':
          result.sort((a, b) => a.price - b.price)
          break
        case 'newest':
        default:
          result.sort((a, b) => b.id - a.id)
          break
      }
      
      totalCourses.value = result.length
      return result
    })
    
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
    
    const handleSearch = () => {
      currentPage.value = 1
    }
    
    const handleFilterChange = () => {
      currentPage.value = 1
    }
    
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
    }
    
    const handleCurrentChange = (page) => {
      currentPage.value = page
    }
    
    const viewCourse = (courseId) => {
      ElMessage.info(`查看课程 ${courseId} 详情功能开发中...`)
    }
    
    const enrollCourse = (courseId) => {
      const course = courses.value.find(c => c.id === courseId)
      if (course) {
        if (course.enrolled) {
          ElMessage.info(`继续学习《${course.title}》功能开发中...`)
        } else {
          ElMessage.info(`报名《${course.title}》功能开发中...`)
        }
      }
    }
    
    return {
      searchKeyword,
      currentPage,
      pageSize,
      totalCourses,
      filters,
      filteredCourses,
      getLevelTagType,
      getLevelText,
      handleSearch,
      handleFilterChange,
      handleSizeChange,
      handleCurrentChange,
      viewCourse,
      enrollCourse
    }
  }
}
</script>

<style scoped>
.courses-page {
  min-height: 100vh;
  background: #f5f7fa;
}

/* 顶部导航栏 */
.courses-header {
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

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

/* 主要内容 */
.courses-main {
  padding: 24px;
}

.courses-container {
  max-width: 1400px;
  margin: 0 auto;
}

/* 筛选器 */
.filters-section {
  margin-bottom: 24px;
  padding: 20px;
}

.filters-content {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  align-items: center;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-label {
  font-weight: 500;
  color: #333;
  white-space: nowrap;
}

/* 课程网格 */
.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.course-card {
  cursor: pointer;
  transition: all 0.3s;
  overflow: hidden;
}

.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
}

.course-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.course-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.course-card:hover .course-image img {
  transform: scale(1.05);
}

.course-badge {
  position: absolute;
  top: 12px;
  right: 12px;
}

.course-content {
  padding: 20px;
}

.course-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.course-description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0 0 16px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.course-instructor,
.course-duration {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #666;
  font-size: 0.85rem;
}

.course-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.course-rating {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rating-count {
  color: #666;
  font-size: 0.8rem;
}

.course-students {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #666;
  font-size: 0.85rem;
}

.course-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-price {
  display: flex;
  align-items: center;
  gap: 8px;
}

.original-price {
  color: #999;
  font-size: 0.9rem;
  text-decoration: line-through;
}

.current-price {
  color: #f56c6c;
  font-size: 1.2rem;
  font-weight: 600;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #666;
}

.empty-icon {
  font-size: 4rem;
  color: #ddd;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 1.3rem;
  margin: 0 0 8px 0;
}

.empty-state p {
  margin: 0;
}

/* 分页 */
.pagination-section {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .courses-main {
    padding: 16px;
  }
  
  .header-content {
    padding: 0 16px;
  }
  
  .header-actions {
    display: none;
  }
  
  .filters-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .filter-group {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .courses-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .page-title {
    font-size: 1.3rem;
  }
}

@media (max-width: 480px) {
  .filters-section {
    padding: 16px;
  }
  
  .course-content {
    padding: 16px;
  }
  
  .course-footer {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>