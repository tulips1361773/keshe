<template>
  <div class="coaches-page">
    <!-- 顶部导航栏 -->
    <div class="coaches-header">
      <div class="header-content">
        <div class="back-section">
          <el-button type="primary" link @click="$router.go(-1)">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
        </div>
        
        <h1 class="page-title">教练员中心</h1>
        
        <div class="header-actions">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索教练员..."
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
    <div class="coaches-main">
      <div class="coaches-container">
        <!-- 筛选器 -->
        <div class="filters-section custom-card">
          <div class="filters-content">
            <div class="filter-group">
              <label class="filter-label">教练等级：</label>
              <el-radio-group v-model="filters.level" @change="handleFilterChange">
                <el-radio-button label="all">全部</el-radio-button>
                <el-radio-button label="junior">初级教练</el-radio-button>
                <el-radio-button label="intermediate">中级教练</el-radio-button>
                <el-radio-button label="senior">高级教练</el-radio-button>
                <el-radio-button label="expert">专家教练</el-radio-button>
              </el-radio-group>
            </div>
            
            <div class="filter-group">
              <label class="filter-label">审核状态：</label>
              <el-radio-group v-model="filters.status" @change="handleFilterChange">
                <el-radio-button label="all">全部</el-radio-button>
                <el-radio-button label="approved">已通过</el-radio-button>
                <el-radio-button label="pending">待审核</el-radio-button>
                <el-radio-button label="rejected">已拒绝</el-radio-button>
              </el-radio-group>
            </div>
            
            <div class="filter-group">
              <label class="filter-label">性别：</label>
              <el-radio-group v-model="filters.gender" @change="handleFilterChange">
                <el-radio-button label="all">全部</el-radio-button>
                <el-radio-button label="male">男</el-radio-button>
                <el-radio-button label="female">女</el-radio-button>
              </el-radio-group>
            </div>
            
            <div class="filter-group">
              <label class="filter-label">年龄：</label>
              <el-input-number 
                v-model="filters.ageMin" 
                :min="18" 
                :max="80" 
                placeholder="最小年龄"
                style="width: 100px"
                @change="handleFilterChange"
              />
              <span style="margin: 0 8px;">-</span>
              <el-input-number 
                v-model="filters.ageMax" 
                :min="18" 
                :max="80" 
                placeholder="最大年龄"
                style="width: 100px"
                @change="handleFilterChange"
              />
            </div>
            
            <div class="filter-group">
              <label class="filter-label">排序方式：</label>
              <el-select v-model="filters.sort" @change="handleFilterChange" style="width: 120px">
                <el-option label="最新" value="newest" />
                <el-option label="评分" value="rating" />
                <el-option label="经验" value="experience" />
                <el-option label="姓名" value="name" />
              </el-select>
            </div>
          </div>
        </div>

        <!-- 教练员列表 -->
        <div class="coaches-grid">
          <div 
            v-for="coach in filteredCoaches" 
            :key="coach.id" 
            class="coach-card custom-card"
            @click="viewCoach(coach.id)"
          >
            <div class="coach-avatar">
              <img :src="coach.avatar || '/default-avatar.svg'" :alt="coach.real_name" />
              <div class="coach-status">
                <el-tag :type="getStatusTagType(coach.status)" size="small">
                  {{ getStatusText(coach.status) }}
                </el-tag>
              </div>
            </div>
            
            <div class="coach-content">
              <h3 class="coach-name">{{ coach.real_name }}</h3>
              <p class="coach-level">{{ getLevelText(coach.coach_level) }}</p>
              
              <div class="coach-meta">
                <div class="coach-phone">
                  <el-icon><Phone /></el-icon>
                  <span>{{ coach.phone }}</span>
                </div>
                
                <div class="coach-experience">
                  <el-icon><Trophy /></el-icon>
                  <span>{{ coach.experience_years || 0 }}年经验</span>
                </div>
              </div>
              
              <div class="coach-achievements">
                <p class="achievements-text">{{ coach.achievements || '暂无成就描述' }}</p>
              </div>
              
              <div class="coach-stats">
                <div class="coach-rating">
                  <el-rate
                    v-model="coach.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}"
                  />
                  <span class="rating-count">({{ coach.rating_count || 0 }})</span>
                </div>
                
                <div class="coach-students">
                  <el-icon><UserFilled /></el-icon>
                  <span>{{ coach.student_count || 0 }}名学员</span>
                </div>
              </div>
              
              <div class="coach-footer">
                <div class="coach-join-date">
                  <span class="join-text">加入时间：{{ formatDate(coach.created_at) }}</span>
                </div>
                
                <el-button 
                  type="primary" 
                  size="small"
                  @click.stop="contactCoach(coach.id)"
                >
                  联系教练
                </el-button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-if="filteredCoaches.length === 0" class="empty-state">
          <el-icon class="empty-icon"><UserFilled /></el-icon>
          <h3>暂无教练员</h3>
          <p>没有找到符合条件的教练员，请尝试调整筛选条件</p>
        </div>
        
        <!-- 分页 -->
        <div v-if="filteredCoaches.length > 0" class="pagination-section">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[12, 24, 48]"
            :total="totalCoaches"
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
  Phone,
  Trophy,
  UserFilled
} from '@element-plus/icons-vue'
import api from '../utils/api'

export default {
  name: 'Coaches',
  components: {
    ArrowLeft,
    Search,
    Phone,
    Trophy,
    UserFilled
  },
  setup() {
    const router = useRouter()
    const searchKeyword = ref('')
    const currentPage = ref(1)
    const pageSize = ref(12)
    const totalCoaches = ref(0)
    const loading = ref(false)
    
    const filters = reactive({
      level: 'all',
      status: 'all',
      sort: 'newest',
      gender: 'all',
      ageMin: null,
      ageMax: null
    })
    
    const coaches = ref([])
    
    // 获取教练员列表
    const fetchCoaches = async () => {
      try {
        loading.value = true
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          search: searchKeyword.value,
          level: filters.level,
          status: filters.status === 'all' ? '' : filters.status,
          ordering: getOrderingParam(filters.sort),
          gender: filters.gender === 'all' ? '' : filters.gender,
          age_min: filters.ageMin,
          age_max: filters.ageMax
        }
        
        // 移除空参数
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === 'all') {
            delete params[key]
          }
        })
        
        const response = await api.get('/api/coaches/', { params })
        
        if (response.data.success !== false) {
          coaches.value = response.data.results || response.data
          totalCoaches.value = response.data.count || response.data.length
        } else {
          throw new Error(response.data.message || '获取教练员列表失败')
        }
        
      } catch (error) {
        console.error('获取教练员列表失败:', error)
        ElMessage.error(error.response?.data?.message || '获取教练员列表失败')
        
        // 如果API调用失败，使用模拟数据
        useMockData()
      } finally {
        loading.value = false
      }
    }
    
    // 使用模拟数据的函数
    const useMockData = () => {
      // 这里可以添加模拟数据逻辑
      coaches.value = []
      totalCoaches.value = 0
    }
    
    // 获取排序参数
    const getOrderingParam = (sort) => {
      switch (sort) {
        case 'newest': return '-created_at'
        case 'rating': return '-rating'
        case 'experience': return '-experience_years'
        case 'name': return 'real_name'
        default: return '-created_at'
      }
    }
    
    // 过滤后的教练员列表
    const filteredCoaches = computed(() => {
      return coaches.value
    })
    
    // 搜索处理
    const handleSearch = () => {
      currentPage.value = 1
      fetchCoaches()
    }
    
    // 筛选变化处理
    const handleFilterChange = () => {
      currentPage.value = 1
      fetchCoaches()
    }
    
    // 分页处理
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
      fetchCoaches()
    }
    
    const handleCurrentChange = (page) => {
      currentPage.value = page
      fetchCoaches()
    }
    
    // 查看教练详情
    const viewCoach = (coachId) => {
      router.push(`/coaches/${coachId}`)
    }
    
    // 联系教练
    const contactCoach = (coachId) => {
      ElMessage.info('联系教练功能开发中...')
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
        case 'approved': return '已通过'
        case 'pending': return '待审核'
        case 'rejected': return '已拒绝'
        default: return '未知'
      }
    }
    
    // 获取等级文本
    const getLevelText = (level) => {
      switch (level) {
        case 'junior': return '初级教练'
        case 'intermediate': return '中级教练'
        case 'senior': return '高级教练'
        case 'expert': return '专家教练'
        default: return '未设置'
      }
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未知'
      return new Date(dateString).toLocaleDateString('zh-CN')
    }
    
    onMounted(() => {
      fetchCoaches()
    })
    
    return {
      searchKeyword,
      currentPage,
      pageSize,
      totalCoaches,
      loading,
      filters,
      coaches,
      filteredCoaches,
      handleSearch,
      handleFilterChange,
      handleSizeChange,
      handleCurrentChange,
      viewCoach,
      contactCoach,
      getStatusTagType,
      getStatusText,
      getLevelText,
      formatDate
    }
  }
}
</script>

<style scoped>
.coaches-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
}

.coaches-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
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

.coaches-main {
  padding: 2rem 0;
}

.coaches-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.custom-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.custom-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.filters-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
}

.filters-content {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  align-items: center;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-label {
  font-weight: 500;
  color: #2c3e50;
  white-space: nowrap;
}

.coaches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.coach-card {
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.coach-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.2);
}

.coach-avatar {
  position: relative;
  text-align: center;
  margin-bottom: 1rem;
}

.coach-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.coach-status {
  position: absolute;
  top: -5px;
  right: calc(50% - 60px);
}

.coach-content {
  text-align: center;
}

.coach-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.coach-level {
  color: #7f8c8d;
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
}

.coach-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  color: #7f8c8d;
}

.coach-phone,
.coach-experience {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.coach-achievements {
  margin-bottom: 1rem;
  text-align: left;
}

.achievements-text {
  font-size: 0.85rem;
  color: #7f8c8d;
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.coach-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 0.85rem;
}

.coach-rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.rating-count {
  color: #7f8c8d;
  font-size: 0.8rem;
}

.coach-students {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #7f8c8d;
}

.coach-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #ecf0f1;
}

.join-text {
  font-size: 0.8rem;
  color: #95a5a6;
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

.pagination-section {
  display: flex;
  justify-content: center;
  padding: 2rem 0;
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
  
  .coaches-container {
    padding: 0 1rem;
  }
  
  .coaches-grid {
    grid-template-columns: 1fr;
  }
  
  .filters-content {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .filter-group {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
}
</style>