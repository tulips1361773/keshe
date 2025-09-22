<template>
  <div class="coach-schedule">
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
              @click="handleTimeSlotClick(day.fullDate, hour)"
            >
              <!-- 预约块 -->
              <div 
                v-for="booking in getBookingsForTimeSlot(day.fullDate, hour)"
                :key="booking.id"
                class="booking-block"
                :class="getBookingClass(booking)"
                @click.stop="showBookingDetail(booking)"
              >
                <div class="booking-time">{{ formatBookingTime(booking) }}</div>
                <div class="booking-student">{{ booking.relation.student.real_name }}</div>
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
            <div class="time-content" @click="handleTimeSlotClick(currentDate, hour)">
              <div 
                v-for="booking in getBookingsForTimeSlot(currentDate, hour)"
                :key="booking.id"
                class="booking-item"
                :class="getBookingClass(booking)"
                @click.stop="showBookingDetail(booking)"
              >
                <div class="booking-info">
                  <div class="booking-title">
                    {{ formatBookingTime(booking) }} - {{ booking.relation.student.real_name }}
                  </div>
                  <div class="booking-details">
                    {{ booking.table.campus.name }} {{ booking.table.number }}号台
                    <el-tag :type="getStatusTagType(booking.status)" size="small">
                      {{ getStatusText(booking.status) }}
                    </el-tag>
                  </div>
                </div>
                <div class="booking-actions">
                  <el-button 
                    v-if="booking.status === 'pending'"
                    type="success" 
                    size="small"
                    @click.stop="confirmBooking(booking)"
                  >
                    确认
                  </el-button>
                  <el-button 
                    v-if="canCancelBooking(booking)"
                    type="danger" 
                    size="small"
                    @click.stop="cancelBooking(booking)"
                  >
                    取消
                  </el-button>
                </div>
              </div>
              
              <!-- 空白时间段提示 -->
              <div 
                v-if="getBookingsForTimeSlot(currentDate, hour).length === 0 && !isPastTime(currentDate, hour)"
                class="empty-slot"
              >
                <span class="empty-text">空闲时间</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 预约详情对话框 -->
    <el-dialog v-model="showDetailDialog" title="预约详情" width="500px">
      <div v-if="selectedBooking" class="booking-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="学员">{{ selectedBooking.relation.student.real_name }}</el-descriptions-item>
          <el-descriptions-item label="时间">{{ formatBookingTime(selectedBooking) }}</el-descriptions-item>
          <el-descriptions-item label="球台">{{ selectedBooking.table.campus.name }} {{ selectedBooking.table.number }}号台</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusTagType(selectedBooking.status)">
              {{ getStatusText(selectedBooking.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="费用">¥{{ selectedBooking.total_fee }}</el-descriptions-item>
          <el-descriptions-item label="备注" v-if="selectedBooking.notes">{{ selectedBooking.notes }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showDetailDialog = false">关闭</el-button>
          <el-button 
            v-if="selectedBooking && selectedBooking.status === 'pending'"
            type="success" 
            @click="confirmBooking(selectedBooking)"
          >
            确认预约
          </el-button>
          <el-button 
            v-if="selectedBooking && canCancelBooking(selectedBooking)"
            type="danger" 
            @click="cancelBooking(selectedBooking)"
          >
            取消预约
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Calendar,
  Refresh,
  ArrowLeft,
  ArrowRight
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 响应式数据
const viewMode = ref('week')
const currentDate = ref(new Date())
const loading = ref(false)
const bookings = ref([])
const showDetailDialog = ref(false)
const selectedBooking = ref(null)

// 时间配置
const timeSlots = Array.from({ length: 14 }, (_, i) => i + 8) // 8:00 - 21:00

// 计算属性
const weekDays = computed(() => {
  const days = []
  const startOfWeek = getStartOfWeek(currentDate.value)
  const today = new Date()
  
  for (let i = 0; i < 7; i++) {
    const date = new Date(startOfWeek)
    date.setDate(startOfWeek.getDate() + i)
    
    days.push({
      name: getDayName(i),
      date: formatDate(date),
      fullDate: date,
      isToday: isSameDay(date, today)
    })
  }
  
  return days
})

const weekRangeText = computed(() => {
  const start = weekDays.value[0].date
  const end = weekDays.value[6].date
  return `${start} - ${end}`
})

const dayTitle = computed(() => {
  return formatFullDate(currentDate.value)
})

// 方法
const getStartOfWeek = (date) => {
  const d = new Date(date)
  const day = d.getDay()
  const diff = d.getDate() - day + (day === 0 ? -6 : 1) // 周一为第一天
  return new Date(d.setDate(diff))
}

const getDayName = (index) => {
  const names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  return names[index]
}

const formatDate = (date) => {
  return `${date.getMonth() + 1}/${date.getDate()}`
}

const formatFullDate = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const dayName = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][date.getDay()]
  return `${year}年${month}月${day}日 ${dayName}`
}

const formatHour = (hour) => {
  return `${hour}:00`
}

const formatBookingTime = (booking) => {
  const start = new Date(booking.start_time)
  const end = new Date(booking.end_time)
  return `${start.getHours()}:${String(start.getMinutes()).padStart(2, '0')}-${end.getHours()}:${String(end.getMinutes()).padStart(2, '0')}`
}

const isSameDay = (date1, date2) => {
  return date1.toDateString() === date2.toDateString()
}

const isPastTime = (date, hour) => {
  const now = new Date()
  const timeSlot = new Date(date)
  timeSlot.setHours(hour, 0, 0, 0)
  return timeSlot < now
}

const getBookingsForTimeSlot = (date, hour) => {
  return bookings.value.filter(booking => {
    const bookingStart = new Date(booking.start_time)
    const bookingEnd = new Date(booking.end_time)
    const slotStart = new Date(date)
    slotStart.setHours(hour, 0, 0, 0)
    const slotEnd = new Date(date)
    slotEnd.setHours(hour + 1, 0, 0, 0)
    
    return bookingStart < slotEnd && bookingEnd > slotStart
  })
}

const getBookingClass = (booking) => {
  return {
    'booking-pending': booking.status === 'pending',
    'booking-confirmed': booking.status === 'confirmed',
    'booking-completed': booking.status === 'completed',
    'booking-cancelled': booking.status === 'cancelled'
  }
}

const getStatusTagType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'confirmed': 'success',
    'pending_cancellation': 'warning',
    'completed': 'info',
    'cancelled': 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    'pending': '待确认',
    'confirmed': '已确认',
    'pending_cancellation': '待审核取消',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return textMap[status] || '未知'
}

const canCancelBooking = (booking) => {
  if (booking.status !== 'pending' && booking.status !== 'confirmed') {
    return false
  }
  
  const now = new Date()
  const bookingStart = new Date(booking.start_time)
  const timeDiff = bookingStart - now
  const hoursDiff = timeDiff / (1000 * 60 * 60)
  
  return hoursDiff > 24 // 24小时前可以取消
}

// 事件处理
const handleDateChange = () => {
  loadBookings()
}

const previousWeek = () => {
  const newDate = new Date(currentDate.value)
  newDate.setDate(newDate.getDate() - 7)
  currentDate.value = newDate
  loadBookings()
}

const nextWeek = () => {
  const newDate = new Date(currentDate.value)
  newDate.setDate(newDate.getDate() + 7)
  currentDate.value = newDate
  loadBookings()
}

const previousDay = () => {
  const newDate = new Date(currentDate.value)
  newDate.setDate(newDate.getDate() - 1)
  currentDate.value = newDate
  loadBookings()
}

const nextDay = () => {
  const newDate = new Date(currentDate.value)
  newDate.setDate(newDate.getDate() + 1)
  currentDate.value = newDate
  loadBookings()
}

const handleTimeSlotClick = (date, hour) => {
  if (isPastTime(date, hour)) {
    ElMessage.warning('不能选择过去的时间')
    return
  }
  
  // 这里可以触发创建新预约的逻辑
  ElMessage.info(`点击了 ${formatFullDate(date)} ${formatHour(hour)} 时间段`)
}

const showBookingDetail = (booking) => {
  selectedBooking.value = booking
  showDetailDialog.value = true
}

const confirmBooking = async (booking) => {
  try {
    const response = await fetch(`/api/reservations/bookings/${booking.id}/confirm/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (response.ok) {
      ElMessage.success('预约确认成功')
      booking.status = 'confirmed'
      showDetailDialog.value = false
    } else {
      const error = await response.json()
      ElMessage.error(error.error || '确认失败')
    }
  } catch (error) {
    ElMessage.error('网络错误，请重试')
  }
}

const cancelBooking = async (booking) => {
  try {
    await ElMessageBox.confirm(
      '确定要取消这个预约吗？',
      '取消预约',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await fetch(`/api/reservations/bookings/${booking.id}/cancel/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        reason: '教练取消'
      })
    })
    
    if (response.ok) {
      ElMessage.success('预约取消成功')
      booking.status = 'cancelled'
      showDetailDialog.value = false
    } else {
      const error = await response.json()
      ElMessage.error(error.error || '取消失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('网络错误，请重试')
    }
  }
}

const refreshSchedule = () => {
  loadBookings()
}

const loadBookings = async () => {
  try {
    loading.value = true
    
    // 计算查询日期范围
    let startDate, endDate
    if (viewMode.value === 'week') {
      startDate = getStartOfWeek(currentDate.value)
      endDate = new Date(startDate)
      endDate.setDate(startDate.getDate() + 6)
    } else {
      startDate = new Date(currentDate.value)
      endDate = new Date(currentDate.value)
    }
    
    const params = new URLSearchParams({
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0]
    })
    
    const response = await fetch(`http://127.0.0.1:8000/api/reservations/bookings/?${params}`, {
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      bookings.value = data.results || data
    } else {
      ElMessage.error('加载课表失败')
    }
  } catch (error) {
    ElMessage.error('网络错误，请重试')
  } finally {
    loading.value = false
  }
}

// 生命周期
onMounted(() => {
  loadBookings()
})

// 监听视图模式变化
watch(viewMode, () => {
  loadBookings()
})
</script>

<style scoped>
.coach-schedule {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.schedule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.schedule-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.schedule-controls {
  display: flex;
  align-items: center;
}

/* 周视图样式 */
.week-view {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.week-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.week-navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.week-range {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.week-calendar {
  display: flex;
  overflow-x: auto;
}

.time-axis {
  min-width: 80px;
  border-right: 1px solid #eee;
}

.time-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
}

.time-slot {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #eee;
  font-size: 0.9rem;
  color: #666;
}

.day-column {
  flex: 1;
  min-width: 120px;
  border-right: 1px solid #eee;
}

.day-header {
  height: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
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
  color: #666;
}

.time-grid {
  position: relative;
}

.time-cell {
  height: 60px;
  border-bottom: 1px solid #eee;
  position: relative;
  cursor: pointer;
  transition: background-color 0.2s;
}

.time-cell:hover {
  background: #f5f5f5;
}

.time-cell.past-time {
  background: #fafafa;
  cursor: not-allowed;
}

.booking-block {
  position: absolute;
  left: 2px;
  right: 2px;
  top: 2px;
  bottom: 2px;
  border-radius: 4px;
  padding: 4px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.booking-block:hover {
  transform: scale(1.02);
  z-index: 10;
}

.booking-pending {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  color: #856404;
}

.booking-confirmed {
  background: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
}

.booking-completed {
  background: #d1ecf1;
  border: 1px solid #bee5eb;
  color: #0c5460;
}

.booking-cancelled {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.booking-time {
  font-weight: 600;
  margin-bottom: 2px;
}

.booking-student {
  margin-bottom: 1px;
}

.booking-table {
  font-size: 0.7rem;
  opacity: 0.8;
}

/* 日视图样式 */
.day-view {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.day-header-large {
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.day-navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.day-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
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
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: hidden;
}

.time-slot-row.past-time {
  opacity: 0.6;
}

.time-label {
  width: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-right: 1px solid #eee;
  font-weight: 600;
  color: #666;
}

.time-content {
  flex: 1;
  padding: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.time-content:hover {
  background: #f5f5f5;
}

.booking-item {
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.booking-info {
  flex: 1;
}

.booking-title {
  font-weight: 600;
  margin-bottom: 4px;
}

.booking-details {
  font-size: 0.9rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 8px;
}

.booking-actions {
  display: flex;
  gap: 8px;
}

.empty-slot {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60px;
  color: #999;
  font-style: italic;
}

.empty-text {
  font-size: 0.9rem;
}

/* 对话框样式 */
.booking-detail {
  padding: 20px 0;
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
  }
  
  .schedule-controls {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .week-calendar {
    overflow-x: scroll;
  }
  
  .day-column {
    min-width: 100px;
  }
  
  .booking-block {
    font-size: 0.7rem;
  }
}
</style>