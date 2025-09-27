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
              <el-option label="男" value="male" />
              <el-option label="女" value="female" />
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
                <el-avatar :size="80" :src="getAvatarUrl(coach.user_info?.avatar)">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <div class="coach-status" :class="getStatusClass(coach.status)">
                  {{ getStatusText(coach.status) }}
                </div>
              </div>
              
              <div class="coach-basic-info">
                <h3 class="coach-name">{{ coach.real_name }}</h3>
                <div class="coach-level">
                  <el-tag :type="getLevelTagType(coach.coach_level)" size="small">
                    {{ getLevelText(coach.coach_level) }}
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
                <span class="detail-value">{{ coach.gender ? (coach.gender === 'male' ? '男' : '女') : '?' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">年龄：</span>
                <span class="detail-value">{{ coach.age !== null ? `${coach.age}岁` : '?' }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">联系方式：</span>
                <span class="detail-value">{{ coach.phone }}</span>
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
                :type="getCoachButtonType(coach)"
                @click="selectCoach(coach)"
                :loading="selectingCoach === coach.id"
                :disabled="isCoachDisabled(coach)"
                class="coach-select-btn"
              >
                <el-icon><Check /></el-icon>
                <span>{{ getCoachButtonText(coach) }}</span>
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
            <el-avatar :size="40" :src="getAvatarUrl(coach.avatar)">
              <el-icon><User /></el-icon>
            </el-avatar>
            <div class="coach-info">
              <span class="coach-name">{{ coach.real_name }}</span>
              <span class="coach-level">{{ getLevelText(coach.coach_level) }}</span>
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
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Search, View, Check } from '@element-plus/icons-vue'
import axios from '@/utils/axios'
import { useUserStore } from '@/stores/user'

export default {
  name: 'CoachSelection',
  components: {
    User,
    Search,
    View,
    Check
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
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
        console.log('教练列表API响应:', response.data)
        
        if (response.data.success) {
          coaches.value = response.data.results || []
          total.value = response.data.count || coaches.value.length
          console.log('获取到的教练列表:', coaches.value)
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
    
    // 存储所有师生关系状态，用于按钮状态判断
    const allRelationStatuses = ref(new Map())
    
    const fetchSelectedCoaches = async () => {
      try {
        console.log('开始获取师生关系数据...')
        const response = await axios.get('/api/reservations/relations/')
        console.log('师生关系API响应:', response.data)
        
        const relations = response.data.results || response.data || []
        console.log('解析出的师生关系数据:', relations)
        
        // 清空并重新构建关系状态映射
        allRelationStatuses.value.clear()
        
        if (relations.length > 0) {
          // 构建所有师生关系的状态映射，用于按钮状态判断
          relations.forEach(relation => {
            if (relation.coach?.id) {
              allRelationStatuses.value.set(relation.coach.id, {
                status: relation.status,
                applied_at: relation.applied_at
              })
            }
          })
          console.log('所有师生关系状态映射:', allRelationStatuses.value)
          
          // 只获取审核通过的师生关系用于"我的教练员"列表
          const approvedRelations = relations.filter(relation => relation.status === 'approved')
          console.log('审核通过的师生关系:', approvedRelations)
          
          if (approvedRelations.length > 0) {
            // 需要通过教练的用户ID找到对应的Coach模型ID
            console.log('获取教练列表以进行ID映射...')
            const coachesResponse = await axios.get('/api/accounts/coaches/')
            const allCoaches = coachesResponse.data.results || []
            console.log('所有教练数据:', allCoaches)
            
            selectedCoaches.value = approvedRelations.map(relation => {
              console.log('处理师生关系:', relation)
              
              // 通过用户ID找到对应的Coach记录
              const coachRecord = allCoaches.find(coach => coach.user === relation.coach?.id)
              const coachId = coachRecord ? coachRecord.id : relation.coach?.id
              
              console.log('用户ID:', relation.coach?.id, '对应的Coach ID:', coachId)
              console.log('找到的Coach记录:', coachRecord)
              
              const mappedCoach = {
                id: coachId, // 使用Coach模型的ID
                real_name: relation.coach?.real_name || coachRecord?.real_name || '未知教练',
                coach_level: coachRecord?.coach_level || 'junior', // 从Coach记录获取等级
                avatar: relation.coach?.avatar || coachRecord?.user_info?.avatar || '/default-avatar.svg',
                status: relation.status,
                applied_at: relation.applied_at
              }
              
              console.log('映射后的教练数据:', mappedCoach)
              return mappedCoach
            })
            console.log('处理后的selectedCoaches:', selectedCoaches.value)
          } else {
            console.log('当前用户没有审核通过的师生关系记录')
            selectedCoaches.value = []
          }
        } else {
          console.log('当前用户没有师生关系记录')
          selectedCoaches.value = []
        }
      } catch (error) {
        console.error('获取已选择教练员失败:', error)
        selectedCoaches.value = []
        allRelationStatuses.value.clear()
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
        // 检查用户认证状态
        if (!userStore.isAuthenticated) {
          ElMessage.error('请先登录后再选择教练')
          return
        }
        
        // 检查用户信息是否已加载
        if (!userStore.userInfo || !userStore.userInfo.id) {
          ElMessage.error('用户信息加载中，请稍后重试')
          // 尝试重新获取用户信息
          await userStore.fetchProfile()
          if (!userStore.userInfo || !userStore.userInfo.id) {
            ElMessage.error('无法获取用户信息，请重新登录')
            return
          }
        }
        
        // 检查已选择的教练数量（包括已通过和待审核的）
        const approvedCount = selectedCoaches.value.length
        const pendingCount = Object.values(allRelationStatuses.value).filter(status => status === 'pending').length
        const totalCount = approvedCount + pendingCount
        
        if (totalCount >= 2) {
          ElMessage.error('最多只能选择两个教练员，请更换教练员')
          return
        }
        
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
        
        const requestData = {
          coach_id: coach.user,  // 使用用户ID而不是Coach模型ID
          student_id: userStore.userInfo.id,  // 确保有值后再使用
          notes: `学员选择教练：${coach.real_name}`
        }
        
        console.log('发送的请求数据:', requestData)
        console.log('教练对象:', coach)
        console.log('用户信息:', userStore.userInfo)
        
        const response = await axios.post('/api/reservations/relations/', requestData)
        
        if (response.status === 201 || response.status === 200) {
          ElMessage.success('申请已提交，请等待教练审核！')
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
              // 处理数组格式的错误信息
              if (Array.isArray(data) && data.length > 0) {
                errorMessage = data[0]
              } else if (data.non_field_errors && data.non_field_errors.length > 0) {
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
          r.coach_id === coach.user && r.status === 'approved'  // 使用用户ID查找关系
        )
        
        if (relation) {
          // 删除师生关系
          const response = await axios.delete(`/api/reservations/relations/${relation.id}/`)
          ElMessage.success('取消选择成功！')
          selectedCoaches.value = selectedCoaches.value.filter(c => c.id !== coach.user)  // 使用用户ID过滤
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
      // 跳转到教练详情页面
      router.push({ name: 'CoachDetail', params: { id: coach.id } })
    }
    
    const isCoachSelected = (coach) => {
      // 检查是否在"我的教练员"列表中（只包含审核通过的）
      return selectedCoaches.value.some(selectedCoach => selectedCoach.id === coach.id)
    }
    
    const getCoachButtonText = (coach) => {
      // 通过教练的用户ID查找师生关系状态
      const relationStatus = allRelationStatuses.value.get(coach.user)
      
      if (!relationStatus) {
        return '选择教练'
      }
      
      console.log('getCoachButtonText - coach:', coach, 'relationStatus:', relationStatus)
      
      switch (relationStatus.status) {
        case 'approved':
          return '已选择'
        case 'pending':
          return '正在审核'
        case 'rejected':
          return '已拒绝'
        default:
          return '选择教练'
      }
    }
    
    const getCoachButtonType = (coach) => {
      // 通过教练的用户ID查找师生关系状态
      const relationStatus = allRelationStatuses.value.get(coach.user)
      
      if (!relationStatus) {
        return 'primary'
      }
      
      console.log('getCoachButtonType - coach:', coach, 'relationStatus:', relationStatus)
      
      switch (relationStatus.status) {
        case 'approved':
          return 'success'
        case 'pending':
          return 'warning'
        case 'rejected':
          return 'danger'
        default:
          return 'primary'
      }
    }
    
    const isCoachDisabled = (coach) => {
      // 通过教练的用户ID查找师生关系状态
      const relationStatus = allRelationStatuses.value.get(coach.user)
      
      if (!relationStatus) {
        return false
      }
      
      // 已选择、正在审核、已拒绝的都不能再点击
      return ['approved', 'pending', 'rejected'].includes(relationStatus.status)
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

    const getAvatarUrl = (avatar) => {
      if (!avatar) {
        return '/default-avatar.svg'
      }

      
      // 如果已经是完整URL，直接返回
      if (avatar.startsWith('http')) {
        return avatar
      }
      
      // 如果是静态文件路径，使用后端服务器
      if (avatar.startsWith('/static/')) {
        return `http://127.0.0.1:8000${avatar}`
      }
      
      // 如果是相对路径，添加服务器地址
      return `http://127.0.0.1:8000${avatar}`
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
      getCoachButtonText,
      getCoachButtonType,
      isCoachDisabled,
      getStatusClass,
      getStatusText,
      getLevelTagType,
      getLevelText,
      getAvatarUrl
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