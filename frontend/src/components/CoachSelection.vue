<template>
  <div class="coach-selection-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon><User /></el-icon>
        选择教练员
      </h2>
      <p class="page-subtitle">找到最适合您的乒乓球教练</p>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="search-filter-section">
      <el-card class="filter-card">
        <div class="search-row">
          <!-- 搜索框 -->
          <div class="search-input">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索教练姓名..."
              clearable
              @input="handleSearch"
              @clear="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
          
          <!-- 搜索按钮 -->
          <el-button type="primary" @click="handleSearch" :loading="loading">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
        </div>
        
        <!-- 筛选条件 -->
        <div class="filter-row">
          <div class="filter-item">
            <label class="filter-label">教练等级：</label>
            <el-select v-model="filters.level" placeholder="选择等级" clearable @change="handleFilterChange">
              <el-option label="初级教练" value="junior" />
              <el-option label="中级教练" value="intermediate" />
              <el-option label="高级教练" value="senior" />
              <el-option label="专业教练" value="professional" />
            </el-select>
          </div>
          
          <div class="filter-item">
            <label class="filter-label">性别：</label>
            <el-select v-model="filters.gender" placeholder="选择性别" clearable @change="handleFilterChange">
              <el-option label="男" value="M" />
              <el-option label="女" value="F" />
            </el-select>
          </div>
          
          <div class="filter-item">
            <label class="filter-label">年龄范围：</label>
            <el-select v-model="filters.age_range" placeholder="选择年龄" clearable @change="handleFilterChange">
              <el-option label="20-30岁" value="20-30" />
              <el-option label="30-40岁" value="30-40" />
              <el-option label="40-50岁" value="40-50" />
              <el-option label="50岁以上" value="50+" />
            </el-select>
          </div>
          
          <div class="filter-item">
            <label class="filter-label">排序：</label>
            <el-select v-model="filters.ordering" placeholder="排序方式" @change="handleFilterChange">
              <el-option label="评分最高" value="-rating" />
              <el-option label="经验最多" value="-experience_years" />
              <el-option label="学员最多" value="-student_count" />
              <el-option label="最新加入" value="-created_at" />
            </el-select>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 教练员列表 -->
    <div class="coaches-section">
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>
      
      <div v-else-if="coaches.length === 0" class="empty-state">
        <el-empty description="暂无符合条件的教练员">
          <el-button type="primary" @click="resetFilters">重置筛选条件</el-button>
        </el-empty>
      </div>
      
      <div v-else class="coaches-grid">
        <div 
          v-for="coach in coaches" 
          :key="coach.id" 
          class="coach-card"
        >
          <el-card class="coach-card-content" shadow="hover">
            <!-- 教练头像和基本信息 -->
            <div class="coach-header">
              <div class="coach-avatar">
                <el-avatar :size="80" :src="coach.avatar">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <div class="coach-status" :class="getStatusClass(coach.status)">
                  {{ getStatusText(coach.status) }}
                </div>
              </div>
              
              <div class="coach-basic-info">
                <h3 class="coach-name">{{ coach.real_name }}</h3>
                <div class="coach-level">
                  <el-tag :type="getLevelTagType(coach.level)" size="small">
                    {{ getLevelText(coach.level) }}
                  </el-tag>
                </div>
                <div class="coach-rating">
                  <el-rate
                    v-model="coach.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}分"
                  />
                </div>
              </div>
            </div>
            
            <!-- 教练详细信息 -->
            <div class="coach-details">
              <div class="detail-row">
                <span class="detail-label">性别：</span>
                <span class="detail-value">{{ coach.gender === 'M' ? '男' : '女' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">年龄：</span>
                <span class="detail-value">{{ coach.age }}岁</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">教学经验：</span>
                <span class="detail-value">{{ coach.experience_years }}年</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">联系方式：</span>
                <span class="detail-value">{{ coach.phone }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">学员数量：</span>
                <span class="detail-value">{{ coach.student_count }}人</span>
              </div>
            </div>
            
            <!-- 教练专长和成就 -->
            <div class="coach-achievements" v-if="coach.specialties || coach.achievements">
              <div v-if="coach.specialties" class="specialties">
                <span class="section-label">专长：</span>
                <el-tag v-for="specialty in coach.specialties.split(',')"
                       :key="specialty"
                       size="small"
                       class="specialty-tag">
                  {{ specialty.trim() }}
                </el-tag>
              </div>
              <div v-if="coach.achievements" class="achievements">
                <span class="section-label">成就：</span>
                <p class="achievement-text">{{ coach.achievements }}</p>
              </div>
            </div>
            
            <!-- 操作按钮 -->
            <div class="coach-actions">
              <el-button type="info" plain @click="viewCoachDetail(coach)">
                <el-icon><View /></el-icon>
                查看详情
              </el-button>
              <el-button 
                type="primary" 
                @click="selectCoach(coach)"
                :loading="selectingCoach === coach.id"
                :disabled="coach.status !== 'approved' || isCoachSelected(coach.id)"
              >
                <el-icon><Check /></el-icon>
                {{ isCoachSelected(coach.id) ? '已选择' : '选择教练' }}
              </el-button>
            </div>
          </el-card>
        </div>
      </div>
      
      <!-- 分页 -->
      <div class="pagination-container" v-if="total > pageSize">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[12, 24, 48]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 我的教练员 -->
    <div class="my-coaches-section" v-if="selectedCoaches.length > 0">
      <el-card>
        <template #header>
          <div class="section-header">
            <h3>我的教练员</h3>
            <el-tag type="success">{{ selectedCoaches.length }}位</el-tag>
          </div>
        </template>
        
        <div class="selected-coaches-list">
          <div 
            v-for="coach in selectedCoaches" 
            :key="coach.id" 
            class="selected-coach-item"
          >
            <el-avatar :size="40" :src="coach.avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <div class="coach-info">
              <span class="coach-name">{{ coach.real_name }}</span>
              <span class="coach-level">{{ getLevelText(coach.level) }}</span>
            </div>
            <div class="coach-actions">
              <el-button type="primary" link @click="viewCoachDetail(coach)">
                查看详情
              </el-button>
              <el-button type="danger" link @click="unselectCoach(coach.id)">
                取消选择
              </el-button>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Search, View, Check } from '@element-plus/icons-vue'
import axios from '@/utils/axios'

export default {
  name: 'CoachSelection',
  components: {
    User,
    Search,
    View,
    Check
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const selectingCoach = ref(null)
    const searchKeyword = ref('')
    const coaches = ref([])
    const selectedCoaches = ref([])
    const currentPage = ref(1)
    const pageSize = ref(12)
    const total = ref(0)
    
    // 筛选条件
    const filters = reactive({
      level: '',
      gender: '',
      age_range: '',
      ordering: '-rating'
    })
    
    // 方法
    const fetchCoaches = async () => {
      loading.value = true
      try {
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          search: searchKeyword.value,
          ...filters
        }
        
        // 移除空值参数
        Object.keys(params).forEach(key => {
          if (params[key] === '' || params[key] === null || params[key] === undefined) {
            delete params[key]
          }
        })
        
        const response = await axios.get('/api/accounts/coaches/', { params })
        
        if (response.data.success) {
          coaches.value = response.data.results || []
          total.value = response.data.count || coaches.value.length
        } else {
          throw new Error(response.data.message || '获取教练员列表失败')
        }
      } catch (error) {
        console.error('获取教练员列表失败:', error)
        ElMessage.error('获取教练员列表失败，请稍后重试')
        // 使用模拟数据
        coaches.value = []
      } finally {
        loading.value = false
      }
    }
    
    const fetchSelectedCoaches = async () => {
      try {
        const response = await axios.get('/api/reservations/relations/')
        if (response.data && response.data.length > 0) {
          // 过滤出已通过的师生关系，并提取教练信息
          const approvedRelations = response.data.filter(relation => relation.status === 'approved')
          selectedCoaches.value = approvedRelations.map(relation => ({
            id: relation.coach_id,
            real_name: relation.coach?.real_name || '未知教练',
            level: relation.coach?.coach_level || 'junior',
            avatar: relation.coach?.avatar || '/default-avatar.svg'
          }))
        } else {
          selectedCoaches.value = []
        }
      } catch (error) {
        console.error('获取已选择教练员失败:', error)
        selectedCoaches.value = []
      }
    }
    
    const handleSearch = () => {
      currentPage.value = 1
      fetchCoaches()
    }
    
    const handleFilterChange = () => {
      currentPage.value = 1
      fetchCoaches()
    }
    
    const handleSizeChange = (size) => {
      pageSize.value = size
      fetchCoaches()
    }
    
    const handleCurrentChange = (page) => {
      currentPage.value = page
      fetchCoaches()
    }
    
    const resetFilters = () => {
      searchKeyword.value = ''
      Object.keys(filters).forEach(key => {
        if (key !== 'ordering') {
          filters[key] = ''
        }
      })
      currentPage.value = 1
      fetchCoaches()
    }
    
    const selectCoach = async (coach) => {
      try {
        await ElMessageBox.confirm(
          `确定要选择 ${coach.real_name} 作为您的教练吗？`,
          '确认选择教练',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'info'
          }
        )
        
        selectingCoach.value = coach.id
        
        const response = await axios.post('/api/reservations/relations/', {
          coach_id: coach.user_id || coach.id,
          notes: `学员选择教练：${coach.real_name}`
        })
        
        if (response.status === 201 || response.status === 200) {
          ElMessage.success('选择教练成功！')
          selectedCoaches.value.push(coach)
          // 刷新教练列表和已选择教练列表
          fetchCoaches()
          fetchSelectedCoaches()
        } else {
          throw new Error('选择教练失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('选择教练失败:', error)
          console.log('错误详情:', error.response?.data)
          
          // 处理不同类型的错误
          let errorMessage = '选择教练失败，请稍后重试'
          
          if (error.response) {
            const status = error.response.status
            const data = error.response.data
            
            console.log(`HTTP状态码: ${status}, 响应数据:`, data)
            
            if (status === 400) {
              if (data.non_field_errors && data.non_field_errors.length > 0) {
                const errorDetail = data.non_field_errors[0]
                if (typeof errorDetail === 'string') {
                  errorMessage = errorDetail
                } else if (errorDetail.message) {
                  errorMessage = errorDetail.message
                }
              } else if (data.detail) {
                errorMessage = data.detail
              } else if (data.error) {
                errorMessage = data.error
              } else {
                // 检查是否是重复关系错误
                const errorStr = JSON.stringify(data)
                if (errorStr.includes('UNIQUE constraint failed') || errorStr.includes('already exists')) {
                  errorMessage = '您已经选择过这位教练了，请勿重复选择'
                }
              }
            } else if (status === 401) {
              errorMessage = '请先登录后再选择教练'
            } else if (status === 403) {
              errorMessage = '您没有权限执行此操作'
            }
          } else if (error.message) {
            errorMessage = error.message
          }
          
          console.log('最终错误消息:', errorMessage)
          ElMessage.error(errorMessage)
        }
      } finally {
        selectingCoach.value = null
      }
    }
    
    const unselectCoach = async (coachId) => {
      try {
        const coach = selectedCoaches.value.find(c => c.id === coachId)
        await ElMessageBox.confirm(
          `确定要取消选择 ${coach?.real_name} 吗？`,
          '确认取消选择',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        // 先获取师生关系列表，找到对应的关系记录
        const relationsResponse = await axios.get('/api/reservations/relations/')
        const relation = relationsResponse.data.find(r => 
          r.coach_id === coachId && r.status === 'approved'
        )
        
        if (relation) {
          // 删除师生关系
          const response = await axios.delete(`/api/reservations/relations/${relation.id}/`)
          ElMessage.success('取消选择成功！')
          selectedCoaches.value = selectedCoaches.value.filter(c => c.id !== coachId)
          // 刷新教练列表
          fetchCoaches()
        } else {
          throw new Error('未找到对应的师生关系记录')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('取消选择失败:', error)
          ElMessage.error(error.message || '取消选择失败，请稍后重试')
        }
      }
    }
    
    const viewCoachDetail = (coach) => {
      // 可以跳转到教练详情页面或打开详情对话框
      ElMessage.info('教练详情功能开发中...')
    }
    
    const isCoachSelected = (coachId) => {
      return selectedCoaches.value.some(coach => coach.id === coachId)
    }
    
    // 辅助方法
    const getStatusClass = (status) => {
      const statusMap = {
        'approved': 'status-approved',
        'pending': 'status-pending',
        'rejected': 'status-rejected'
      }
      return statusMap[status] || 'status-unknown'
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        'approved': '已认证',
        'pending': '审核中',
        'rejected': '未通过'
      }
      return statusMap[status] || '未知'
    }
    
    const getLevelTagType = (level) => {
      const levelMap = {
        'junior': 'info',
        'intermediate': 'warning',
        'senior': 'success',
        'professional': 'danger'
      }
      return levelMap[level] || 'info'
    }
    
    const getLevelText = (level) => {
      const levelMap = {
        'junior': '初级教练',
        'intermediate': '中级教练',
        'senior': '高级教练',
        'professional': '专业教练'
      }
      return levelMap[level] || '未知等级'
    }
    
    // 生命周期
    onMounted(() => {
      fetchCoaches()
      fetchSelectedCoaches()
    })
    
    return {
      loading,
      selectingCoach,
      searchKeyword,
      coaches,
      selectedCoaches,
      currentPage,
      pageSize,
      total,
      filters,
      fetchCoaches,
      handleSearch,
      handleFilterChange,
      handleSizeChange,
      handleCurrentChange,
      resetFilters,
      selectCoach,
      unselectCoach,
      viewCoachDetail,
      isCoachSelected,
      getStatusClass,
      getStatusText,
      getLevelTagType,
      getLevelText
    }
  }
}
</script>

<style scoped>
.coach-selection-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-title {
  font-size: 28px;
  color: #303133;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.page-subtitle {
  font-size: 16px;
  color: #606266;
  margin: 0;
}

.search-filter-section {
  margin-bottom: 30px;
}

.filter-card {
  border-radius: 12px;
}

.search-row {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  align-items: center;
}

.search-input {
  flex: 1;
  max-width: 400px;
}

.filter-row {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  align-items: center;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #606266;
  white-space: nowrap;
}

.coaches-section {
  margin-bottom: 30px;
}

.loading-container {
  padding: 20px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.coaches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.coach-card {
  height: 100%;
}

.coach-card-content {
  height: 100%;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.coach-card-content:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.coach-header {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  align-items: flex-start;
}

.coach-avatar {
  position: relative;
}

.coach-status {
  position: absolute;
  bottom: -5px;
  right: -5px;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 10px;
  color: white;
  font-weight: bold;
}

.status-approved {
  background-color: #67c23a;
}

.status-pending {
  background-color: #e6a23c;
}

.status-rejected {
  background-color: #f56c6c;
}

.coach-basic-info {
  flex: 1;
}

.coach-name {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  margin: 0 0 8px 0;
}

.coach-level {
  margin-bottom: 8px;
}

.coach-rating {
  margin-bottom: 5px;
}

.coach-details {
  margin-bottom: 15px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.detail-label {
  color: #909399;
  font-weight: 500;
}

.detail-value {
  color: #303133;
  font-weight: 600;
}

.coach-achievements {
  margin-bottom: 20px;
}

.specialties {
  margin-bottom: 10px;
}

.section-label {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
  margin-right: 8px;
}

.specialty-tag {
  margin-right: 5px;
  margin-bottom: 5px;
}

.achievement-text {
  font-size: 13px;
  color: #606266;
  line-height: 1.5;
  margin: 5px 0 0 0;
}

.coach-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.my-coaches-section {
  margin-top: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.selected-coaches-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.selected-coach-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.selected-coach-item:hover {
  background-color: #e9ecef;
}

.selected-coach-item .coach-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.selected-coach-item .coach-name {
  font-weight: bold;
  color: #303133;
}

.selected-coach-item .coach-level {
  font-size: 12px;
  color: #909399;
}

.selected-coach-item .coach-actions {
  display: flex;
  gap: 10px;
}

@media (max-width: 768px) {
  .coaches-grid {
    grid-template-columns: 1fr;
  }
  
  .search-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>