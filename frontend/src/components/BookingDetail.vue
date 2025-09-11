<template>
  <el-dialog
    v-model="visible"
    :title="isEditing ? '编辑预约' : '预约详情'"
    width="600px"
    :before-close="handleClose"
  >
    <div class="booking-detail">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="预约编号">
          {{ booking.id }}
        </el-descriptions-item>
        
        <el-descriptions-item label="预约状态">
          <el-tag :type="getStatusTagType(booking.status)">
            {{ getStatusText(booking.status) }}
          </el-tag>
        </el-descriptions-item>
        
        <el-descriptions-item label="师生关系">
          {{ getRelationText(booking.relation) }}
        </el-descriptions-item>
        
        <el-descriptions-item label="校区">
          {{ booking.table?.campus?.name || '未知校区' }}
        </el-descriptions-item>
        
        <el-descriptions-item label="球台">
          {{ booking.table ? `${booking.table.number}号台 - ${booking.table.name || '标准台'}` : '未知球台' }}
        </el-descriptions-item>
        
        <el-descriptions-item label="预约时长">
          {{ booking.duration_hours }}小时
        </el-descriptions-item>
        
        <el-descriptions-item label="开始时间">
          {{ formatDateTime(booking.start_time) }}
        </el-descriptions-item>
        
        <el-descriptions-item label="结束时间">
          {{ formatDateTime(booking.end_time) }}
        </el-descriptions-item>
        
        <el-descriptions-item label="预约费用">
          <span class="fee-amount">¥{{ booking.total_fee }}</span>
        </el-descriptions-item>
        
        <el-descriptions-item label="支付状态">
          <el-tag :type="getPaymentStatusTagType(booking.payment_status)">
            {{ getPaymentStatusText(booking.payment_status) }}
          </el-tag>
        </el-descriptions-item>
        
        <el-descriptions-item label="创建时间" :span="2">
          {{ formatDateTime(booking.created_at) }}
        </el-descriptions-item>
        
        <el-descriptions-item v-if="booking.notes" label="备注" :span="2">
          {{ booking.notes }}
        </el-descriptions-item>
      </el-descriptions>
      
      <!-- 取消记录 -->
      <div v-if="booking.cancellation" class="cancellation-info">
        <h4>取消信息</h4>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="取消时间">
            {{ formatDateTime(booking.cancellation.cancelled_at) }}
          </el-descriptions-item>
          
          <el-descriptions-item label="取消原因">
            {{ booking.cancellation.reason || '无' }}
          </el-descriptions-item>
          
          <el-descriptions-item label="退款金额">
            ¥{{ booking.cancellation.refund_amount || 0 }}
          </el-descriptions-item>
          
          <el-descriptions-item label="退款状态">
            <el-tag :type="getRefundStatusTagType(booking.cancellation.refund_status)">
              {{ getRefundStatusText(booking.cancellation.refund_status) }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
        
        <template v-if="canCancel">
          <el-button 
            type="danger" 
            @click="handleCancel"
            :loading="cancelling"
          >
            取消预约
          </el-button>
        </template>
        
        <template v-if="canPay">
          <el-button 
            type="success" 
            @click="handlePay"
            :loading="paying"
          >
            立即支付
          </el-button>
        </template>
      </div>
    </template>
  </el-dialog>
  
  <!-- 取消预约对话框 -->
  <el-dialog
    v-model="cancelDialogVisible"
    title="取消预约"
    width="400px"
  >
    <el-form :model="cancelForm" :rules="cancelRules" ref="cancelFormRef">
      <el-form-item label="取消原因" prop="reason">
        <el-input
          v-model="cancelForm.reason"
          type="textarea"
          :rows="4"
          placeholder="请输入取消原因"
        />
      </el-form-item>
    </el-form>
    
    <template #footer>
      <el-button @click="cancelDialogVisible = false">取消</el-button>
      <el-button 
        type="danger" 
        @click="confirmCancel"
        :loading="cancelling"
      >
        确认取消
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  booking: {
    type: Object,
    default: () => ({})
  },
  isEditing: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'refresh'])

// 响应式数据
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const cancelling = ref(false)
const paying = ref(false)
const cancelDialogVisible = ref(false)
const cancelFormRef = ref()

const cancelForm = reactive({
  reason: ''
})

const cancelRules = {
  reason: [{ required: true, message: '请输入取消原因', trigger: 'blur' }]
}

// 计算属性
const canCancel = computed(() => {
  return props.booking.status === 'confirmed' && 
         new Date(props.booking.start_time) > new Date()
})

const canPay = computed(() => {
  return props.booking.status === 'confirmed' && 
         props.booking.payment_status === 'pending'
})

// 方法
const handleClose = () => {
  visible.value = false
}

const getStatusTagType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'confirmed': 'success',
    'cancelled': 'danger',
    'completed': 'info'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status) => {
  const textMap = {
    'pending': '待确认',
    'confirmed': '已确认',
    'cancelled': '已取消',
    'completed': '已完成'
  }
  return textMap[status] || '未知'
}

const getPaymentStatusTagType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'paid': 'success',
    'refunded': 'info',
    'failed': 'danger'
  }
  return typeMap[status] || 'info'
}

const getPaymentStatusText = (status) => {
  const textMap = {
    'pending': '待支付',
    'paid': '已支付',
    'refunded': '已退款',
    'failed': '支付失败'
  }
  return textMap[status] || '未知'
}

const getRefundStatusTagType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'completed': 'success',
    'failed': 'danger'
  }
  return typeMap[status] || 'info'
}

const getRefundStatusText = (status) => {
  const textMap = {
    'pending': '退款中',
    'completed': '已退款',
    'failed': '退款失败'
  }
  return textMap[status] || '未知'
}

const getRelationText = (relation) => {
  if (!relation) return '未知关系'
  
  if (userStore.user.user_type === 'coach') {
    return `学员: ${relation.student?.real_name || '未知'}`
  } else {
    return `教练: ${relation.coach?.real_name || '未知'}`
  }
}

const formatDateTime = (dateTime) => {
  if (!dateTime) return '未知时间'
  return new Date(dateTime).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleCancel = () => {
  cancelForm.reason = ''
  cancelDialogVisible.value = true
}

const confirmCancel = async () => {
  try {
    await cancelFormRef.value.validate()
    
    cancelling.value = true
    
    const response = await fetch(`/api/reservations/bookings/${props.booking.id}/cancel/`, {
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
      cancelDialogVisible.value = false
      visible.value = false
      emit('refresh')
    } else {
      const error = await response.json()
      ElMessage.error(error.error || '取消预约失败')
    }
  } catch (error) {
    if (error.message) {
      console.error('取消预约错误:', error)
      ElMessage.error('取消预约失败')
    }
  } finally {
    cancelling.value = false
  }
}

const handlePay = async () => {
  try {
    await ElMessageBox.confirm(
      `确认支付 ¥${props.booking.total_fee} 吗？`,
      '确认支付',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    paying.value = true
    
    // 这里应该调用支付接口
    // 暂时模拟支付成功
    setTimeout(() => {
      ElMessage.success('支付成功')
      paying.value = false
      visible.value = false
      emit('refresh')
    }, 2000)
    
  } catch {
    // 用户取消支付
  }
}
</script>

<style scoped>
.booking-detail {
  padding: 0;
}

.fee-amount {
  font-weight: bold;
  color: #e6a23c;
  font-size: 16px;
}

.cancellation-info {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #ebeef5;
}

.cancellation-info h4 {
  margin: 0 0 16px 0;
  color: #f56c6c;
  font-size: 16px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.el-descriptions {
  margin-bottom: 0;
}

.el-descriptions :deep(.el-descriptions__label) {
  font-weight: 500;
}
</style>