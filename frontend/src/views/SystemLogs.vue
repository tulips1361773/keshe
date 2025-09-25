<template>
  <div class="system-logs">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon><Document /></el-icon>
        系统日志
      </h2>
      <p class="page-description">查看系统操作记录和用户活动日志</p>
    </div>

    <!-- 筛选器 -->
    <div class="filters custom-card">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-input
            v-model="filters.search"
            placeholder="搜索用户名、操作描述..."
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filters.action_type" placeholder="操作类型" @change="fetchLogs">
            <el-option label="全部" value="" />
            <el-option label="创建" value="create" />
            <el-option label="更新" value="update" />
            <el-option label="删除" value="delete" />
            <el-option label="查看" value="view" />
            <el-option label="登录" value="login" />
            <el-option label="登出" value="logout" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filters.resource_type" placeholder="资源类型" @change="fetchLogs">
            <el-option label="全部" value="" />
            <el-option label="用户" value="user" />
            <el-option label="课程" value="course" />
            <el-option label="预约" value="reservation" />
            <el-option label="支付" value="payment" />
            <el-option label="评价" value="evaluation" />
            <el-option label="比赛" value="competition" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="handleDateChange"
          />
        </el-col>
        <el-col :span="4">
          <el-button @click="resetFilters" :icon="Refresh">重置</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 日志列表 -->
    <div class="logs-list custom-card">
      <el-table
        :data="logs"
        v-loading="loading"
        stripe
        style="width: 100%"
        :default-sort="{ prop: 'created_at', order: 'descending' }"
      >
        <el-table-column prop="created_at" label="操作时间" width="180" sortable>
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="user_name" label="操作用户" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.user_name" type="primary" size="small">
              {{ row.user_name }}
            </el-tag>
            <el-tag v-else type="info" size="small">系统</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="action_type" label="操作类型" width="100">
          <template #default="{ row }">
            <el-tag 
              :type="getActionTypeColor(row.action_type)" 
              size="small"
            >
              {{ getActionTypeText(row.action_type) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="resource_type" label="资源类型" width="100">
          <template #default="{ row }">
            <el-tag type="success" size="small">
              {{ getResourceTypeText(row.resource_type) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="resource_name" label="资源名称" width="150" show-overflow-tooltip />
        
        <el-table-column prop="description" label="操作描述" min-width="200" show-overflow-tooltip />
        
        <el-table-column prop="ip_address" label="IP地址" width="120" />
        
        <el-table-column prop="campus_name" label="所属校区" width="120">
          <template #default="{ row }">
            <span v-if="row.campus_name">{{ row.campus_name }}</span>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="80" fixed="right">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              size="small" 
              @click="viewDetail(row)"
              :icon="View"
            >
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="日志详情"
      width="600px"
    >
      <div v-if="selectedLog" class="log-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="操作时间">
            {{ formatDateTime(selectedLog.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="操作用户">
            {{ selectedLog.user_name || '系统' }}
          </el-descriptions-item>
          <el-descriptions-item label="操作类型">
            {{ getActionTypeText(selectedLog.action_type) }}
          </el-descriptions-item>
          <el-descriptions-item label="资源类型">
            {{ getResourceTypeText(selectedLog.resource_type) }}
          </el-descriptions-item>
          <el-descriptions-item label="资源名称">
            {{ selectedLog.resource_name || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="操作描述">
            {{ selectedLog.description }}
          </el-descriptions-item>
          <el-descriptions-item label="IP地址">
            {{ selectedLog.ip_address || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="用户代理">
            {{ selectedLog.user_agent || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="所属校区">
            {{ selectedLog.campus_name || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="额外数据" v-if="selectedLog.extra_data">
            <pre>{{ JSON.stringify(selectedLog.extra_data, null, 2) }}</pre>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import {
  Document,
  Search,
  Refresh,
  View
} from '@element-plus/icons-vue'
import axios from '@/utils/axios'

const userStore = useUserStore()

// 响应式数据
const logs = ref([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const dateRange = ref([])

// 筛选器
const filters = reactive({
  search: '',
  action_type: '',
  resource_type: ''
})

// 对话框状态
const showDetailDialog = ref(false)
const selectedLog = ref(null)

// 获取日志列表
const fetchLogs = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: filters.search,
      action_type: filters.action_type,
      resource_type: filters.resource_type,
      ordering: '-created_at'
    }
    
    // 添加日期范围筛选
    if (dateRange.value && dateRange.value.length === 2) {
      params.created_at__gte = dateRange.value[0]
      params.created_at__lte = dateRange.value[1]
    }
    
    const response = await axios.get('/api/logs/api/system-logs/', { params })
    
    if (response.data.results) {
      logs.value = response.data.results
      total.value = response.data.count
    } else {
      logs.value = response.data.data || []
      total.value = response.data.count || logs.value.length
    }
  } catch (error) {
    ElMessage.error('获取系统日志失败')
    console.error('获取系统日志失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchLogs()
}

// 日期范围变化处理
const handleDateChange = () => {
  currentPage.value = 1
  fetchLogs()
}

// 重置筛选器
const resetFilters = () => {
  filters.search = ''
  filters.action_type = ''
  filters.resource_type = ''
  dateRange.value = []
  currentPage.value = 1
  fetchLogs()
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchLogs()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchLogs()
}

// 查看详情
const viewDetail = (log) => {
  selectedLog.value = log
  showDetailDialog.value = true
}

// 格式化日期时间
const formatDateTime = (dateTime) => {
  if (!dateTime) return '-'
  return new Date(dateTime).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 获取操作类型文本
const getActionTypeText = (actionType) => {
  const typeMap = {
    'create': '创建',
    'update': '更新',
    'delete': '删除',
    'view': '查看',
    'login': '登录',
    'logout': '登出'
  }
  return typeMap[actionType] || actionType
}

// 获取操作类型颜色
const getActionTypeColor = (actionType) => {
  const colorMap = {
    'create': 'success',
    'update': 'warning',
    'delete': 'danger',
    'view': 'info',
    'login': 'primary',
    'logout': 'primary'
  }
  return colorMap[actionType] || 'default'
}

// 获取资源类型文本
const getResourceTypeText = (resourceType) => {
  const typeMap = {
    'user': '用户',
    'course': '课程',
    'reservation': '预约',
    'payment': '支付',
    'evaluation': '评价',
    'competition': '比赛'
  }
  return typeMap[resourceType] || resourceType
}

// 组件挂载时加载数据
onMounted(() => {
  fetchLogs()
})
</script>

<style scoped>
.system-logs {
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.page-description {
  color: #606266;
  margin: 0;
  font-size: 14px;
}

.custom-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.filters {
  padding: 20px;
}

.logs-list {
  padding: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.log-detail {
  padding: 16px 0;
}

.text-muted {
  color: #909399;
}

pre {
  background: #f5f7fa;
  padding: 12px;
  border-radius: 4px;
  font-size: 12px;
  max-height: 200px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .system-logs {
    padding: 16px;
  }
  
  .filters .el-col {
    margin-bottom: 16px;
  }
}
</style>