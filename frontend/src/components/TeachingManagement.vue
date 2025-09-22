<template>
  <div class="teaching-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon><UserFilled /></el-icon>
        教学管理
      </h2>
      <p class="page-description">管理您的学员申请和师生关系</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card pending">
        <div class="stat-icon">
          <el-icon><Clock /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ stats.pending }}</div>
          <div class="stat-label">待审核申请</div>
        </div>
      </div>
      <div class="stat-card approved">
        <div class="stat-icon">
          <el-icon><Check /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ stats.approved }}</div>
          <div class="stat-label">已通过申请</div>
        </div>
      </div>
      <div class="stat-card total">
        <div class="stat-icon">
          <el-icon><User /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ stats.total }}</div>
          <div class="stat-label">总学员数</div>
        </div>
      </div>
    </div>

    <!-- 筛选器 -->
    <div class="filters">
      <el-select v-model="filters.status" placeholder="申请状态" @change="handleFilterChange">
        <el-option label="全部" value=""></el-option>
        <el-option label="待审核" value="pending"></el-option>
        <el-option label="已通过" value="approved"></el-option>
        <el-option label="已拒绝" value="rejected"></el-option>
      </el-select>
      <el-date-picker
        v-model="filters.dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        @change="handleFilterChange"
      />
      <el-button type="primary" @click="refreshData">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>

    <!-- 申请列表 -->
    <div class="applications-list">
      <el-card v-for="application in applications" :key="application.id" class="application-card">
        <div class="application-header">
          <div class="student-info">
            <el-avatar :src="application.student.avatar || '/default-avatar.svg'" :size="50" />
            <div class="student-details">
              <h4 class="student-name">{{ application.student.real_name || application.student.username }}</h4>
              <p class="student-contact">{{ application.student.phone || application.student.email }}</p>
            </div>
          </div>
          <div class="application-status">
            <el-tag :type="getStatusTagType(application.status)" size="large">
              {{ getStatusText(application.status) }}
            </el-tag>
          </div>
        </div>
        
        <div class="application-content">
          <div class="application-info">
            <div class="info-item">
              <label>申请时间：</label>
              <span>{{ formatDate(application.applied_at) }}</span>
            </div>
            <div class="info-item" v-if="application.processed_at">
              <label>处理时间：</label>
              <span>{{ formatDate(application.processed_at) }}</span>
            </div>
            <div class="info-item" v-if="application.notes">
              <label>申请备注：</label>
              <span>{{ application.notes }}</span>
            </div>
          </div>
        </div>
        
        <div class="application-actions" v-if="application.status === 'pending'">
          <el-button type="success" @click="approveApplication(application)">
            <el-icon><Check /></el-icon>
            同意申请
          </el-button>
          <el-button type="danger" @click="rejectApplication(application)">
            <el-icon><Close /></el-icon>
            拒绝申请
          </el-button>
        </div>
      </el-card>
      
      <!-- 空状态 -->
      <div v-if="applications.length === 0" class="empty-state">
        <el-icon class="empty-icon"><DocumentRemove /></el-icon>
        <h3>暂无申请记录</h3>
        <p>还没有学员申请选择您为教练</p>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="total > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  UserFilled,
  Clock,
  Check,
  User,
  Refresh,
  Close,
  DocumentRemove
} from '@element-plus/icons-vue'
import api from '@/utils/api'

// 响应式数据
const applications = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 筛选器
const filters = reactive({
  status: '',
  dateRange: null
})

// 统计数据
const stats = reactive({
  pending: 0,
  approved: 0,
  total: 0
})

// 计算属性
const filteredApplications = computed(() => {
  return applications.value
})

// 获取申请列表
const fetchApplications = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      status: filters.status || undefined,
      start_date: filters.dateRange?.[0] || undefined,
      end_date: filters.dateRange?.[1] || undefined
    }
    
    const response = await api.get('/api/reservations/relations/', { params })
    
    if (response.data) {
      applications.value = response.data.results || []
      total.value = response.data.count || 0
      
      // 更新统计数据
      updateStats()
    }
  } catch (error) {
    console.error('获取申请列表失败:', error)
    ElMessage.error('获取申请列表失败')
  } finally {
    loading.value = false
  }
}

// 更新统计数据
const updateStats = () => {
  const allApplications = applications.value
  stats.pending = allApplications.filter(app => app.status === 'pending').length
  stats.approved = allApplications.filter(app => app.status === 'approved').length
  stats.total = allApplications.length
}

// 同意申请
const approveApplication = async (application) => {
  try {
    await ElMessageBox.confirm(
      `确定要同意 ${application.student.real_name || application.student.username} 的申请吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await api.post(`/api/reservations/relations/${application.id}/approve/`, {
      action: 'approve'
    })
    
    if (response.status === 200) {
      ElMessage.success('申请已同意')
      await fetchApplications()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('同意申请失败:', error)
      ElMessage.error(error.response?.data?.error || '同意申请失败')
    }
  }
}

// 拒绝申请
const rejectApplication = async (application) => {
  try {
    await ElMessageBox.confirm(
      `确定要拒绝 ${application.student.real_name || application.student.username} 的申请吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await api.post(`/api/reservations/relations/${application.id}/approve/`, {
      action: 'reject'
    })
    
    if (response.status === 200) {
      ElMessage.success('申请已拒绝')
      await fetchApplications()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('拒绝申请失败:', error)
      ElMessage.error(error.response?.data?.error || '拒绝申请失败')
    }
  }
}

// 筛选变化处理
const handleFilterChange = () => {
  currentPage.value = 1
  fetchApplications()
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchApplications()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchApplications()
}

// 刷新数据
const refreshData = () => {
  fetchApplications()
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

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 组件挂载时获取数据
onMounted(() => {
  fetchApplications()
})
</script>

<style scoped>
.teaching-management {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
  text-align: center;
}

.page-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 1.8rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.page-description {
  color: #7f8c8d;
  margin: 0;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-card.pending {
  border-left: 4px solid #e6a23c;
}

.stat-card.approved {
  border-left: 4px solid #67c23a;
}

.stat-card.total {
  border-left: 4px solid #409eff;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.pending .stat-icon {
  background: #e6a23c;
}

.approved .stat-icon {
  background: #67c23a;
}

.total .stat-icon {
  background: #409eff;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1;
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.applications-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.application-card {
  border-radius: 12px;
  overflow: hidden;
  transition: box-shadow 0.2s ease;
}

.application-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.application-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.student-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.student-details {
  flex: 1;
}

.student-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.25rem 0;
}

.student-contact {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0;
}

.application-content {
  margin-bottom: 1rem;
}

.application-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item {
  display: flex;
  gap: 0.5rem;
}

.info-item label {
  font-weight: 500;
  color: #606266;
  min-width: 80px;
}

.info-item span {
  color: #2c3e50;
}

.application-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
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

.pagination {
  display: flex;
  justify-content: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .teaching-management {
    padding: 1rem;
  }
  
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .application-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .application-actions {
    flex-direction: column;
  }
}
</style>