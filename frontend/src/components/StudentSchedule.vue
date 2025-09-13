<template>
  <div class="student-schedule">
    <!-- 课表头部 -->
    <div class="schedule-header">
      <h3 class="schedule-title">
        <el-icon><Calendar /></el-icon>
        我的课表
      </h3>
      <div class="schedule-controls">
        <el-button-group>
          <el-button 
            :type="viewMode === 'week' ? 'primary' : 'default'"
            @click="viewMode = 'week'"
          >
            周视图
          </el-button>
          <el-button 
            :type="viewMode === 'day' ? 'primary' : 'default'"
            @click="viewMode = 'day'"
          >
            日视图
          </el-button>
        </el-button-group>
        <el-date-picker
          v-model="currentDate"
          type="date"
          placeholder="选择日期"
          @change="handleDateChange"
          style="margin-left: 12px;"
        />
        <el-button @click="refreshSchedule" :loading="loading" style="margin-left: 12px;">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 周视图 -->
    <div v-if="viewMode === 'week'" class="week-view">
      <div class="week-header">
        <div class="week-navigation">
          <el-button @click="previousWeek" :icon="ArrowLeft" circle />
          <span class="week-range">{{ weekRangeText }}</span>
          <el-button @click="nextWeek" :icon="ArrowRight" circle />
        </div>
      </div>
      
      <div class="week-calendar">
        <!-- 时间轴 -->
        <div class="time-axis">
          <div class="time-header">时间</div>
          <div 
            v-for="hour in timeSlots" 
            :key="hour"
            class="time-slot"
          >
            {{ formatHour(hour) }}
          </div>
        </div>
        
        <!-- 日期列 -->
        <div 
          v-for="(day, index) in weekDays" 
          :key="day.date"
          class="day-column"
        >
          <div class="day-header" :class="{ 'today': day.isToday }">
            <div class="day-name">{{ day.name }}</div>
            <div class="day-date">{{ day.date }}</div>
          </div>
          
          <!-- 时间段网格 -->
          <div class="time-grid">
            <div 
              v-for="hour in timeSlots" 
              :key="hour"
              class="time-cell"
              :class="{ 'past-time': isPastTime(day.fullDate, hour) }"
            >
              <!-- 预约块 -->
              <div 
                v-for="booking in getBookingsForTimeSlot(day.fullDate, hour)"
                :key="booking.id"
                class="booking-block"
                :class="getBookingClass(booking)"
                @click="showBookingDetail(booking)"
              >
                <div class="booking-time">{{ formatBookingTime(booking) }}</div>
                <div class="booking-coach">{{ booking.relation.coach.real_name }}</div>
                <div class="booking-table">{{ booking.table.number }}号台</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 日视图 -->
    <div v-if="viewMode === 'day'" class="day-view">
      <div class="day-header-large">
        <div class="day-navigation">
          <el-button @click="previousDay" :icon="ArrowLeft" circle />
          <span class="day-title">{{ dayTitle }}</span>
          <el-button @click="nextDay" :icon="ArrowRight" circle />
        </div>
      </div>
      
      <div class="day-schedule">
        <div class="time-slots-list">
          <div 
            v-for="hour in timeSlots" 
            :key="hour"
            class="time-slot-row"
            :class="{ 'past-time': isPastTime(currentDate, hour) }"
          >
            <div class="time-label">{{ formatHour(hour) }}</div>
            <div class="time-content">
              <div 
                v-for="booking in getBookingsForTimeSlot(currentDate, hour)"
                :key="booking.id"
                class="booking-item"
                :class="getBookingClass(booking)"
                @click="showBookingDetail(booking)"
              >
                <div class="booking-info">
                  <div class="booking-title">
                    {{ formatBookingTime(booking) }} - {{ booking.relation.coach.real_name }}
                  </div>
                  <div class="booking-details">
                    <span class="booking-table">{{ booking.table.number }}号台</span>
                    <span class="booking-status">{{ getStatusText(booking.status) }}</span>
                  </div>
                </div>
              </div>
              <div v-if="getBookingsForTimeSlot(currentDate, hour).length === 0" class="empty-slot">
                暂无课程安排
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 预约详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="课程详情"
      width="500px"
      :before-close="handleCloseDetail"
    >
      <div v-if="selectedBooking" class="booking-detail">
        <div class="detail-item">
          <label>教练：</label>
          <span>{{ selectedBooking.relation.coach.real_name }}</span>
        </div>
        <div class="detail-item">
          <label>时间：</label>
          <span>{{ formatBookingTime(selectedBooking) }}</span>
        </div>
        <div class="detail-item">
          <label>球台：</label>
          <span>{{ selectedBooking.table.number }}号台</span>
        </div>
        <div class="detail-item">
          <label>状态：</label>
          <el-tag :type="getStatusTagType(selectedBooking.status)">
            {{ getStatusText(selectedBooking.status) }}
          </el-tag>
        </div>
        <div class="detail-item">
          <label>费用：</label>
          <span>¥{{ selectedBooking.total_fee }}</span>
        </div>
        <div v-if="selectedBooking.notes" class="detail-item">
          <label>备注：</label>
          <span>{{ selectedBooking.notes }}</span>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDetailDialog = false">关闭</el-button>
          <el-button 
            v-if="selectedBooking && canCancelBooking(selectedBooking)"
            type="danger" 
            @click="handleCancelBooking"
          >
            取消预约
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Calendar,
  Refresh,
  ArrowLeft,
  ArrowRight
} from '@element-plus/icons-vue'
import axios from '@/utils/axios'

export default {
  name: 'StudentSchedule',
  components: {
    Calendar,
    Refresh,
    ArrowLeft,
    ArrowRight
  },
  setup() {
    // 响应式数据
    const viewMode = ref('week')
    const currentDate = ref(new Date())
    const loading = ref(false)
    const bookings = ref([])
    const showDetailDialog = ref(false)
    const selectedBooking = ref(null)
    
    // 时间段配置
    const timeSlots = ref([
      8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21
    ])
    
    // 计算属性
    const weekRangeText = computed(() => {
      const monday = getMonday(currentDate.value)
      const sunday = new Date(monday)
      sunday.setDate(monday.getDate() + 6)
      
      return `${formatDate(monday)} - ${formatDate(sunday)}`
    })
    
    const dayTitle = computed(() => {
      return formatFullDate(currentDate.value)
    })
    
    const weekDays = computed(() => {
      const monday = getMonday(currentDate.value)
      const days = []
      const dayNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
      
      for (let i = 0; i < 7; i++) {
        const date = new Date(monday)
        date.setDate(monday.getDate() + i)
        
        days.push({
          name: dayNames[i],
          date: formatDate(date),
          fullDate: date,
          isToday: isToday(date)
        })
      }
      
      return days
    })
    
    // 方法
    const getMonday = (date) => {
      const d = new Date(date)
      const day = d.getDay()
      const diff = d.getDate() - day + (day === 0 ? -6 : 1)
      return new Date(d.setDate(diff))
    }
    
    const formatDate = (date) => {
      return `${date.getMonth() + 1}/${date.getDate()}`
    }
    
    const formatFullDate = (date) => {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const dayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
      const dayName = dayNames[date.getDay()]
      
      return `${year}年${month}月${day}日 ${dayName}`
    }
    
    const isToday = (date) => {
      const today = new Date()
      return date.toDateString() === today.toDateString()
    }
    
    const formatHour = (hour) => {
      return `${hour}:00`
    }
    
    const formatBookingTime = (booking) => {
      const start = new Date(booking.start_time)
      const end = new Date(booking.end_time)
      return `${start.getHours()}:${String(start.getMinutes()).padStart(2, '0')}-${end.getHours()}:${String(end.getMinutes()).padStart(2, '0')}`
    }
    
    const isPastTime = (date, hour) => {
      const now = new Date()
      const timeSlot = new Date(date)
      timeSlot.setHours(hour, 0, 0, 0)
      return timeSlot < now
    }
    
    const getBookingsForTimeSlot = (date, hour) => {
      return bookings.value.filter(booking => {
        const bookingDate = new Date(booking.start_time)
        return bookingDate.toDateString() === date.toDateString() &&
               bookingDate.getHours() === hour
      })
    }
    
    const getBookingClass = (booking) => {
      const classes = ['booking-block']
      
      switch (booking.status) {
        case 'pending':
          classes.push('status-pending')
          break
        case 'confirmed':
          classes.push('status-confirmed')
          break
        case 'completed':
          classes.push('status-completed')
          break
        case 'cancelled':
          classes.push('status-cancelled')
          break
      }
      
      return classes.join(' ')
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        'pending': '待确认',
        'confirmed': '已确认',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    }
    
    const getStatusTagType = (status) => {
      const typeMap = {
        'pending': 'warning',
        'confirmed': 'success',
        'completed': 'info',
        'cancelled': 'danger'
      }
      return typeMap[status] || 'default'
    }
    
    const canCancelBooking = (booking) => {
      if (booking.status !== 'pending' && booking.status !== 'confirmed') {
        return false
      }
      
      const now = new Date()
      const startTime = new Date(booking.start_time)
      const timeDiff = startTime - now
      
      // 24小时内不能取消
      return timeDiff > 24 * 60 * 60 * 1000
    }
    
    // 事件处理
    const handleDateChange = () => {
      loadSchedule()
    }
    
    const previousWeek = () => {
      const newDate = new Date(currentDate.value)
      newDate.setDate(newDate.getDate() - 7)
      currentDate.value = newDate
      loadSchedule()
    }
    
    const nextWeek = () => {
      const newDate = new Date(currentDate.value)
      newDate.setDate(newDate.getDate() + 7)
      currentDate.value = newDate
      loadSchedule()
    }
    
    const previousDay = () => {
      const newDate = new Date(currentDate.value)
      newDate.setDate(newDate.getDate() - 1)
      currentDate.value = newDate
      loadSchedule()
    }
    
    const nextDay = () => {
      const newDate = new Date(currentDate.value)
      newDate.setDate(newDate.getDate() + 1)
      currentDate.value = newDate
      loadSchedule()
    }
    
    const showBookingDetail = (booking) => {
      selectedBooking.value = booking
      showDetailDialog.value = true
    }
    
    const handleCloseDetail = () => {
      showDetailDialog.value = false
      selectedBooking.value = null
    }
    
    const handleCancelBooking = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要取消这个预约吗？取消后无法恢复。',
          '确认取消',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await axios.post(`/api/reservations/bookings/${selectedBooking.value.id}/cancel/`)
        
        ElMessage.success('预约已取消')
        showDetailDialog.value = false
        selectedBooking.value = null
        loadSchedule()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('取消预约失败：' + (error.response?.data?.error || error.message))
        }
      }
    }
    
    const refreshSchedule = () => {
      loadSchedule()
    }
    
    // API调用
    const loadSchedule = async () => {
      try {
        loading.value = true
        
        let dateFrom, dateTo
        
        if (viewMode.value === 'week') {
          const monday = getMonday(currentDate.value)
          const sunday = new Date(monday)
          sunday.setDate(monday.getDate() + 6)
          
          dateFrom = monday.toISOString().split('T')[0]
          dateTo = sunday.toISOString().split('T')[0]
        } else {
          dateFrom = currentDate.value.toISOString().split('T')[0]
          dateTo = dateFrom
        }
        
        const response = await axios.get('/api/reservations/bookings/my_schedule/', {
          params: {
            date_from: dateFrom,
            date_to: dateTo
          }
        })
        
        bookings.value = response.data.bookings || []
      } catch (error) {
        console.error('加载课表失败:', error)
        ElMessage.error('加载课表失败：' + (error.response?.data?.error || error.message))
      } finally {
        loading.value = false
      }
    }
    
    // 监听视图模式变化
    watch(viewMode, () => {
      loadSchedule()
    })
    
    // 组件挂载时加载数据
    onMounted(() => {
      loadSchedule()
    })
    
    return {
      viewMode,
      currentDate,
      loading,
      bookings,
      showDetailDialog,
      selectedBooking,
      timeSlots,
      weekRangeText,
      dayTitle,
      weekDays,
      formatHour,
      formatBookingTime,
      isPastTime,
      getBookingsForTimeSlot,
      getBookingClass,
      getStatusText,
      getStatusTagType,
      canCancelBooking,
      handleDateChange,
      previousWeek,
      nextWeek,
      previousDay,
      nextDay,
      showBookingDetail,
      handleCloseDetail,
      handleCancelBooking,
      refreshSchedule
    }
  }
}
</script>

<style scoped>
.student-schedule {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.schedule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.schedule-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.schedule-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 周视图样式 */
.week-view {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.week-header {
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  background: #fafbfc;
}

.week-navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.week-range {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  min-width: 200px;
  text-align: center;
}

.week-calendar {
  display: flex;
  overflow-x: auto;
}

.time-axis {
  min-width: 80px;
  border-right: 1px solid #ebeef5;
}

.time-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #606266;
  border-bottom: 1px solid #ebeef5;
  background: #fafbfc;
}

.time-slot {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #ebeef5;
  font-size: 0.9rem;
  color: #909399;
}

.day-column {
  flex: 1;
  min-width: 120px;
  border-right: 1px solid #ebeef5;
}

.day-header {
  height: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #ebeef5;
  background: #fafbfc;
}

.day-header.today {
  background: #e3f2fd;
  color: #1976d2;
}

.day-name {
  font-size: 0.9rem;
  font-weight: 600;
}

.day-date {
  font-size: 0.8rem;
  color: #909399;
}

.time-grid {
  position: relative;
}

.time-cell {
  height: 60px;
  border-bottom: 1px solid #ebeef5;
  position: relative;
  cursor: pointer;
  transition: background-color 0.2s;
}

.time-cell:hover {
  background: #f5f7fa;
}

.time-cell.past-time {
  background: #fafafa;
  opacity: 0.6;
}

.booking-block {
  position: absolute;
  top: 2px;
  left: 2px;
  right: 2px;
  bottom: 2px;
  border-radius: 6px;
  padding: 4px 6px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
  overflow: hidden;
}

.booking-block:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.booking-block.status-pending {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  color: #856404;
}

.booking-block.status-confirmed {
  background: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
}

.booking-block.status-completed {
  background: #d1ecf1;
  border: 1px solid #bee5eb;
  color: #0c5460;
}

.booking-block.status-cancelled {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.booking-time {
  font-weight: 600;
  margin-bottom: 2px;
}

.booking-coach,
.booking-table {
  font-size: 0.7rem;
  opacity: 0.8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 日视图样式 */
.day-view {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.day-header-large {
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  background: #fafbfc;
}

.day-navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.day-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  min-width: 300px;
  text-align: center;
}

.day-schedule {
  padding: 20px;
}

.time-slots-list {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.time-slot-row {
  display: flex;
  min-height: 80px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.time-slot-row.past-time {
  background: #fafafa;
  opacity: 0.6;
}

.time-label {
  width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafbfc;
  border-right: 1px solid #ebeef5;
  font-weight: 600;
  color: #606266;
}

.time-content {
  flex: 1;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.booking-item {
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.booking-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.booking-item.status-pending {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
}

.booking-item.status-confirmed {
  background: #d4edda;
  border: 1px solid #c3e6cb;
}

.booking-item.status-completed {
  background: #d1ecf1;
  border: 1px solid #bee5eb;
}

.booking-item.status-cancelled {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
}

.booking-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.booking-title {
  font-weight: 600;
  color: #2c3e50;
}

.booking-details {
  display: flex;
  gap: 12px;
  font-size: 0.9rem;
  color: #606266;
}

.empty-slot {
  color: #c0c4cc;
  font-style: italic;
  text-align: center;
  padding: 20px;
}

/* 对话框样式 */
.booking-detail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.detail-item label {
  font-weight: 600;
  color: #606266;
  min-width: 60px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .schedule-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .schedule-controls {
    justify-content: center;
  }
  
  .week-calendar {
    overflow-x: scroll;
  }
  
  .day-column {
    min-width: 100px;
  }
  
  .booking-block {
    font-size: 0.7rem;
    padding: 2px 4px;
  }
  
  .time-slot-row {
    flex-direction: column;
  }
  
  .time-label {
    width: 100%;
    height: 40px;
    border-right: none;
    border-bottom: 1px solid #ebeef5;
  }
}
</style>