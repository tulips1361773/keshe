<template>
  <div class="reservations-container">
    <div class="header">
      <h1>课程预约</h1>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon>
        新建预约
      </el-button>
    </div>

    <!-- 筛选条件 -->
    <el-card class="filter-card">
      <el-form :model="filters" inline>
        <el-form-item label="状态">
          <el-select v-model="filters.status" placeholder="选择状态" clearable>
            <el-option label="待确认" value="pending" />
            <el-option label="已确认" value="confirmed" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
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
          <el-button type="primary" @click="loadBookings">查询</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 预约列表 -->
    <el-card class="list-card">
      <el-table :data="bookings" v-loading="loading" stripe>
        <el-table-column prop="id" label="预约ID" width="80" />
        <el-table-column label="教练" width="100">
          <template #default="{ row }">
            {{ row.relation.coach.real_name }}
          </template>
        </el-table-column>
        <el-table-column label="学员" width="100">
          <template #default="{ row }">
            {{ row.relation.student.real_name }}
          </template>
        </el-table-column>
        <el-table-column label="球台" width="120">
          <template #default="{ row }">
            {{ row.table.campus.name }} - {{ row.table.number }}号台
          </template>
        </el-table-column>
        <el-table-column label="预约时间" width="160">
          <template #default="{ row }">
            {{ formatDateTime(row.start_time) }}
          </template>
        </el-table-column>
        <el-table-column label="时长" width="80">
          <template #default="{ row }">
            {{ row.duration_hours }}小时
          </template>
        </el-table-column>
        <el-table-column label="费用" width="80">
          <template #default="{ row }">
            ¥{{ row.total_fee }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="viewBooking(row)">详情</el-button>
            <el-button 
              v-if="row.status === 'pending' && userStore.user.user_type === 'coach'"
              size="small" 
              type="success" 
              @click="confirmBooking(row)"
            >
              确认
            </el-button>
            <el-button 
              v-if="['pending', 'confirmed'].includes(row.status)"
              size="small" 
              type="danger" 
              @click="cancelBooking(row)"
            >
              取消
            </el-button>
            <el-button 
              v-if="row.status === 'confirmed' && new Date() > new Date(row.end_time)"
              size="small" 
              type="warning" 
              @click="completeBooking(row)"
            >
              完成
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
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
    </el-card>

    <!-- 创建预约对话框 -->
    <el-dialog v-model="showCreateDialog" title="新建预约" width="600px">
      <BookingForm 
        @success="handleCreateSuccess" 
        @cancel="showCreateDialog = false"
      />
    </el-dialog>

    <!-- 预约详情对话框 -->
    <el-dialog v-model="showDetailDialog" title="预约详情" width="600px">
      <BookingDetail 
        v-if="selectedBooking"
        :booking="selectedBooking"
        @close="showDetailDialog = false"
      />
    </el-dialog>

    <!-- 取消预约对话框 -->
    <el-dialog v-model="showCancelDialog" title="取消预约" width="400px">
      <el-form :model="cancelForm" label-width="80px">
        <el-form-item label="取消原因" required>
          <el-input 
            v-model="cancelForm.reason" 
            type="textarea" 
            :rows="4" 
            placeholder="请输入取消原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCancelDialog = false">取消</el-button>
        <el-button type="danger" @click="submitCancel" :loading="cancelLoading">
          确认取消
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import BookingForm from '@/components/BookingForm.vue'
import BookingDetail from '@/components/BookingDetail.vue'

const userStore = useUserStore()

// 响应式数据
const loading = ref(false)
const bookings = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 筛选条件
const filters = reactive({
  status: '',
  date_from: '',
  date_to: ''
})

const dateRange = ref([])

// 对话框状态
const showCreateDialog = ref(false)
const showDetailDialog = ref(false)
const showCancelDialog = ref(false)
const selectedBooking = ref(null)

// 取消表单
const cancelForm = reactive({
  reason: ''
})
const cancelLoading = ref(false)

// 方法
const loadBookings = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      ...filters
    }
    
    const response = await fetch('/api/reservations/bookings/', {
      method: 'GET',
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })
    
    if (response.ok) {
      const data = await response.json()
      bookings.value = data.results || []
      total.value = data.count || 0
    } else {
      ElMessage.error('加载预约列表失败')
    }
  } catch (error) {
    console.error('加载预约列表错误:', error)
    ElMessage.error('加载预约列表失败')
  } finally {
    loading.value = false
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
  filters.status = ''
  filters.date_from = ''
  filters.date_to = ''
  dateRange.value = []
  currentPage.value = 1
  loadBookings()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  loadBookings()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  loadBookings()
}

const viewBooking = (booking) => {
  selectedBooking.value = booking
  showDetailDialog.value = true
}

const confirmBooking = async (booking) => {
  try {
    const response = await fetch(`/api/reservations/api/bookings/${booking.id}/confirm/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })
    
    if (response.ok) {
      ElMessage.success('预约已确认')
      loadBookings()
    } else {
      const error = await response.json()
      ElMessage.error(error.error || '确认预约失败')
    }
  } catch (error) {
    console.error('确认预约错误:', error)
    ElMessage.error('确认预约失败')
  }
}

const cancelBooking = (booking) => {
  selectedBooking.value = booking
  cancelForm.reason = ''
  showCancelDialog.value = true
}

const submitCancel = async () => {
  if (!cancelForm.reason.trim()) {
    ElMessage.warning('请输入取消原因')
    return
  }
  
  cancelLoading.value = true
  try {
    const response = await fetch(`/api/reservations/bookings/${selectedBooking.value.id}/cancel/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        reason: cancelForm.reason
      })
    })
    
    if (response.ok) {
      ElMessage.success('预约已取消')
      showCancelDialog.value = false
      loadBookings()
    } else {
      const error = await response.json()
      ElMessage.error(error.error || '取消预约失败')
    }
  } catch (error) {
    console.error('取消预约错误:', error)
    ElMessage.error('取消预约失败')
  } finally {
    cancelLoading.value = false
  }
}

const completeBooking = async (booking) => {
  try {
    await ElMessageBox.confirm('确认标记此预约为已完成？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await fetch(`/api/reservations/bookings/${booking.id}/complete/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })
    
    if (response.ok) {
      ElMessage.success('预约已完成')
      loadBookings()
    } else {
      const error = await response.json()
      ElMessage.error(error.error || '完成预约失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('完成预约错误:', error)
      ElMessage.error('完成预约失败')
    }
  }
}

const handleCreateSuccess = () => {
  showCreateDialog.value = false
  loadBookings()
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

const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    confirmed: 'success',
    completed: 'info',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待确认',
    confirmed: '已确认',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

// 生命周期
onMounted(() => {
  loadBookings()
})
</script>

<style scoped>
.reservations-container {
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

.filter-card {
  margin-bottom: 20px;
}

.list-card {
  margin-bottom: 20px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.el-table {
  width: 100%;
}

.el-tag {
  font-size: 12px;
}

.el-button + .el-button {
  margin-left: 8px;
}
</style>