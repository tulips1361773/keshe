<template>
  <div class="notifications-container">
    <div class="header">
      <h1>消息通知</h1>
      <div class="header-actions">
        <el-button @click="markAllAsRead" :disabled="!hasUnreadMessages">
          <el-icon><Check /></el-icon>
          全部标记为已读
        </el-button>
        <el-button type="danger" @click="clearAllNotifications">
          <el-icon><Delete /></el-icon>
          清空所有消息
        </el-button>
      </div>
    </div>

    <!-- 统计信息 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ totalCount }}</div>
            <div class="stat-label">总消息数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card unread">
          <div class="stat-content">
            <div class="stat-number">{{ unreadCount }}</div>
            <div class="stat-label">未读消息</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card system">
          <div class="stat-content">
            <div class="stat-number">{{ systemCount }}</div>
            <div class="stat-label">系统消息</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card booking">
          <div class="stat-content">
            <div class="stat-number">{{ bookingCount }}</div>
            <div class="stat-label">预约消息</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 筛选条件 -->
    <el-card class="filter-card">
      <el-form :model="filters" inline>
        <el-form-item label="消息类型">
          <el-select v-model="filters.message_type" placeholder="选择类型" clearable>
            <el-option label="系统消息" value="system" />
            <el-option label="预约通知" value="booking" />
            <el-option label="课程通知" value="course" />
            <el-option label="支付通知" value="payment" />
            <el-option label="评价提醒" value="evaluation" />
          </el-select>
        </el-form-item>
        <el-form-item label="阅读状态">
          <el-select v-model="filters.is_read" placeholder="选择状态" clearable>
            <el-option label="未读" :value="false" />
            <el-option label="已读" :value="true" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="handleDateRangeChange"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadNotifications">查询</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 消息列表 -->
    <el-card class="list-card">
      <div class="notification-list">
        <div 
          v-for="notification in notifications" 
          :key="notification.id"
          class="notification-item"
          :class="{ 'unread': !notification.is_read }"
          @click="handleNotificationClick(notification)"
        >
          <div class="notification-icon">
            <el-icon :size="24" :color="getIconColor(notification.message_type)">
              <component :is="getIconComponent(notification.message_type)" />
            </el-icon>
          </div>
          
          <div class="notification-content">
            <div class="notification-header">
              <span class="notification-title">{{ notification.title }}</span>
              <div class="notification-meta">
                <el-tag 
                  :type="getTypeTag(notification.message_type)" 
                  size="small"
                >
                  {{ getTypeText(notification.message_type) }}
                </el-tag>
                <span class="notification-time">{{ formatDateTime(notification.created_at) }}</span>
              </div>
            </div>
            
            <div class="notification-message">
              {{ notification.message }}
            </div>
            
            <div class="notification-actions">
              <el-button 
                v-if="!notification.is_read" 
                size="small" 
                type="primary" 
                @click.stop="markAsRead(notification)"
              >
                标记已读
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                @click.stop="deleteNotification(notification)"
              >
                删除
              </el-button>
            </div>
          </div>
          
          <div v-if="!notification.is_read" class="unread-indicator"></div>
        </div>
        
        <div v-if="notifications.length === 0" class="empty-state">
          <el-empty description="暂无消息通知" />
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadNotifications"
          @current-change="loadNotifications"
        />
      </div>
    </el-card>

    <!-- 消息详情对话框 -->
    <el-dialog v-model="showDetailDialog" title="消息详情" width="600px">
      <div v-if="selectedNotification" class="notification-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="消息标题">
            {{ selectedNotification.title }}
          </el-descriptions-item>
          <el-descriptions-item label="消息类型">
            <el-tag :type="getTypeTag(selectedNotification.message_type)">
              {{ getTypeText(selectedNotification.message_type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="发送时间">
            {{ formatDateTime(selectedNotification.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="阅读状态">
            <el-tag :type="selectedNotification.is_read ? 'success' : 'warning'">
              {{ selectedNotification.is_read ? '已读' : '未读' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
        
        <div class="message-content">
          <h3>消息内容</h3>
          <div class="message-text">
            {{ selectedNotification.message }}
          </div>
        </div>
        
        <div v-if="selectedNotification.data" class="extra-data">
          <h3>相关数据</h3>
          <pre class="data-content">{{ JSON.stringify(selectedNotification.data, null, 2) }}</pre>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="showDetailDialog = false">关闭</el-button>
        <el-button 
          v-if="selectedNotification && !selectedNotification.is_read" 
          type="primary" 
          @click="markAsRead(selectedNotification)"
        >
          标记已读
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Check, 
  Delete, 
  Bell, 
  Calendar, 
  CreditCard, 
  Star, 
  Warning 
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import axios from '@/utils/axios'

const userStore = useUserStore()

// 响应式数据
const loading = ref(false)
const notifications = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 统计数据
const totalCount = ref(0)
const unreadCount = ref(0)
const systemCount = ref(0)
const bookingCount = ref(0)

// 筛选条件
const filters = reactive({
  message_type: '',
  is_read: '',
  date_from: '',
  date_to: ''
})

const dateRange = ref([])

// 对话框状态
const showDetailDialog = ref(false)
const selectedNotification = ref(null)

// 计算属性
const hasUnreadMessages = computed(() => unreadCount.value > 0)

// 方法
const loadNotifications = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      ...filters
    }
    
    const response = await axios.get('/api/notifications/list/', { params })
    
    // 处理后端返回的数据结构
    const data = response.data
    notifications.value = data.results || []
    total.value = data.count || 0
  } catch (error) {
    console.error('加载消息列表错误:', error)
    ElMessage.error('加载消息列表失败')
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const response = await axios.get('/api/notifications/stats/')
    
    // 处理后端返回的数据结构
    const data = response.data
    totalCount.value = data.total || 0
    unreadCount.value = data.unread || 0
    systemCount.value = data.system || 0
    bookingCount.value = data.booking || 0
  } catch (error) {
    console.error('加载统计数据错误:', error)
  }
}

const markAsRead = async (notification) => {
  try {
    await axios.post(`/api/notifications/${notification.id}/mark-read/`)
    notification.is_read = true
    if (selectedNotification.value && selectedNotification.value.id === notification.id) {
      selectedNotification.value.is_read = true
    }
    loadStats()
    ElMessage.success('已标记为已读')
  } catch (error) {
    console.error('标记已读错误:', error)
    ElMessage.error('操作失败')
  }
}

const markAllAsRead = async () => {
  try {
    await axios.post('/api/notifications/mark-all-read/')
    notifications.value.forEach(n => n.is_read = true)
    loadStats()
    ElMessage.success('所有消息已标记为已读')
  } catch (error) {
    console.error('批量标记已读错误:', error)
    ElMessage.error('操作失败')
  }
}

const deleteNotification = async (notification) => {
  try {
    await ElMessageBox.confirm('确定要删除这条消息吗？', '确认删除', {
      type: 'warning'
    })
    
    await axios.delete(`/api/notifications/${notification.id}/delete/`)
    const index = notifications.value.findIndex(n => n.id === notification.id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
    loadStats()
    ElMessage.success('消息已删除')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除消息错误:', error)
      ElMessage.error('删除失败')
    }
  }
}

const clearAllNotifications = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有消息吗？此操作不可恢复！', '确认清空', {
      type: 'warning'
    })
    
    await axios.post('/api/notifications/clear-all/')
    notifications.value = []
    loadStats()
    ElMessage.success('所有消息已清空')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('清空消息错误:', error)
      ElMessage.error('操作失败')
    }
  }
}

const handleNotificationClick = (notification) => {
  selectedNotification.value = notification
  showDetailDialog.value = true
  
  // 如果是未读消息，自动标记为已读
  if (!notification.is_read) {
    markAsRead(notification)
  }
}

const handleDateRangeChange = (dates) => {
  if (dates && dates.length === 2) {
    filters.date_from = dates[0]
    filters.date_to = dates[1]
  } else {
    filters.date_from = ''
    filters.date_to = ''
  }
}

const resetFilters = () => {
  Object.assign(filters, {
    message_type: '',
    is_read: '',
    date_from: '',
    date_to: ''
  })
  dateRange.value = []
  loadNotifications()
}

// 工具方法
const formatDateTime = (dateTime) => {
  return new Date(dateTime).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getTypeTag = (type) => {
  const tags = {
    system: 'info',
    booking: 'warning',
    course: 'success',
    payment: 'danger',
    evaluation: 'primary'
  }
  return tags[type] || 'info'
}

const getTypeText = (type) => {
  const texts = {
    system: '系统消息',
    booking: '预约通知',
    course: '课程通知',
    payment: '支付通知',
    evaluation: '评价提醒'
  }
  return texts[type] || type
}

const getIconComponent = (type) => {
  const icons = {
    system: Warning,
    booking: Calendar,
    course: Bell,
    payment: CreditCard,
    evaluation: Star
  }
  return icons[type] || Bell
}

const getIconColor = (type) => {
  const colors = {
    system: '#909399',
    booking: '#E6A23C',
    course: '#67C23A',
    payment: '#F56C6C',
    evaluation: '#409EFF'
  }
  return colors[type] || '#909399'
}

// 生命周期
onMounted(() => {
  loadNotifications()
  loadStats()
})
</script>

<style scoped>
.notifications-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  margin: 0;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-card.unread {
  border-color: #E6A23C;
}

.stat-card.system {
  border-color: #909399;
}

.stat-card.booking {
  border-color: #67C23A;
}

.stat-content {
  padding: 10px;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.filter-card {
  margin-bottom: 20px;
}

.list-card {
  margin-bottom: 20px;
}

.notification-list {
  min-height: 400px;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 15px;
  border-bottom: 1px solid #EBEEF5;
  cursor: pointer;
  transition: background-color 0.3s;
  position: relative;
}

.notification-item:hover {
  background-color: #F5F7FA;
}

.notification-item.unread {
  background-color: #FDF6EC;
  border-left: 3px solid #E6A23C;
}

.notification-icon {
  margin-right: 15px;
  margin-top: 5px;
}

.notification-content {
  flex: 1;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.notification-title {
  font-weight: bold;
  color: #303133;
  font-size: 16px;
}

.notification-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.notification-time {
  font-size: 12px;
  color: #909399;
}

.notification-message {
  color: #606266;
  line-height: 1.5;
  margin-bottom: 10px;
}

.notification-actions {
  display: flex;
  gap: 8px;
}

.unread-indicator {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 8px;
  height: 8px;
  background-color: #E6A23C;
  border-radius: 50%;
}

.empty-state {
  text-align: center;
  padding: 50px 0;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.notification-detail {
  padding: 10px 0;
}

.message-content {
  margin: 20px 0;
}

.message-content h3 {
  margin-bottom: 10px;
  color: #303133;
}

.message-text {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  line-height: 1.6;
  color: #606266;
}

.extra-data {
  margin: 20px 0;
}

.extra-data h3 {
  margin-bottom: 10px;
  color: #303133;
}

.data-content {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 12px;
  color: #606266;
  overflow-x: auto;
}

.el-button + .el-button {
  margin-left: 8px;
}
</style>