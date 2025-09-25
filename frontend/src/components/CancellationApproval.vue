<template>
  <div class="cancellation-approval">
    <div class="header">
      <h2>取消申请审核</h2>
      <el-button @click="loadPendingCancellations" :loading="loading">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>

    <div class="content">
      <!-- 待审核申请列表 -->
      <div v-if="cancellations.length > 0" class="cancellation-list">
        <el-card 
          v-for="cancellation in cancellations" 
          :key="cancellation.id" 
          class="cancellation-card"
          shadow="hover"
        >
          <div class="cancellation-header">
            <div class="student-info">
              <h3>{{ cancellation.student_name }}</h3>
              <p class="booking-time">预约时间：{{ cancellation.start_time }} - {{ cancellation.end_time }}</p>
              <p class="court-info">球台：{{ cancellation.court_name }}</p>
              <p class="fee-info">费用：¥{{ cancellation.total_fee }}</p>
            </div>
            <div class="request-info">
              <p class="request-time">申请时间：{{ cancellation.requested_at }}</p>
              <p class="requester">申请人：{{ cancellation.requested_by }}</p>
            </div>
          </div>

          <div class="cancellation-reason" v-if="cancellation.reason">
            <h4>取消原因：</h4>
            <p>{{ cancellation.reason }}</p>
          </div>

          <div class="cancellation-actions">
            <el-button 
              type="success" 
              @click="showApprovalDialog(cancellation, 'approve')"
              :loading="processing"
            >
              <el-icon><Check /></el-icon>
              批准
            </el-button>
            <el-button 
              type="danger" 
              @click="showApprovalDialog(cancellation, 'reject')"
              :loading="processing"
            >
              <el-icon><Close /></el-icon>
              拒绝
            </el-button>
          </div>
        </el-card>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <el-icon class="empty-icon"><DocumentRemove /></el-icon>
        <h3>暂无待审核申请</h3>
        <p>目前没有学员提交的取消申请</p>
      </div>
    </div>

    <!-- 审核对话框 -->
    <el-dialog
      v-model="approvalDialogVisible"
      :title="approvalAction === 'approve' ? '批准取消申请' : '拒绝取消申请'"
      width="500px"
    >
      <div class="approval-content">
        <div class="booking-summary">
          <h4>预约信息</h4>
          <p><strong>学员：</strong>{{ selectedCancellation?.student_name }}</p>
          <p><strong>时间：</strong>{{ selectedCancellation?.start_time }} - {{ selectedCancellation?.end_time }}</p>
          <p><strong>球台：</strong>{{ selectedCancellation?.court_name }}</p>
          <p><strong>费用：</strong>¥{{ selectedCancellation?.total_fee }}</p>
        </div>

        <div class="reason-display" v-if="selectedCancellation?.reason">
          <h4>取消原因</h4>
          <p>{{ selectedCancellation.reason }}</p>
        </div>

        <el-form :model="approvalForm" :rules="approvalRules" ref="approvalFormRef">
          <el-form-item label="审核意见" prop="comment">
            <el-input
              v-model="approvalForm.comment"
              type="textarea"
              :rows="4"
              :placeholder="approvalAction === 'approve' ? '请输入批准意见（可选）' : '请输入拒绝原因'"
            />
          </el-form-item>
        </el-form>
      </div>

      <template #footer>
        <el-button @click="approvalDialogVisible = false">取消</el-button>
        <el-button 
          :type="approvalAction === 'approve' ? 'success' : 'danger'"
          @click="confirmApproval"
          :loading="processing"
        >
          {{ approvalAction === 'approve' ? '确认批准' : '确认拒绝' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Check, Close, Refresh, DocumentRemove } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 响应式数据
const loading = ref(false)
const processing = ref(false)
const cancellations = ref([])
const approvalDialogVisible = ref(false)
const selectedCancellation = ref(null)
const approvalAction = ref('')
const approvalFormRef = ref()

const approvalForm = reactive({
  comment: ''
})

const approvalRules = {
  comment: [
    { 
      required: false, 
      message: '请输入审核意见', 
      trigger: 'blur' 
    }
  ]
}

// 加载待审核申请
const loadPendingCancellations = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/reservations/cancellations/pending/', {
      method: 'GET',
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })

    if (response.ok) {
      const result = await response.json()
      cancellations.value = result.cancellations || []
    } else {
      const error = await response.json()
      ElMessage.error(error.error || '加载取消申请失败')
    }
  } catch (error) {
    console.error('加载取消申请失败:', error)
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 显示审核对话框
const showApprovalDialog = (cancellation, action) => {
  selectedCancellation.value = cancellation
  approvalAction.value = action
  approvalForm.comment = ''
  approvalDialogVisible.value = true
}

// 确认审核
const confirmApproval = async () => {
  try {
    processing.value = true
    
    const response = await fetch(`/api/reservations/cancellations/${selectedCancellation.value.id}/approve/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        action: approvalAction.value,
        comment: approvalForm.comment
      })
    })

    if (response.ok) {
      const result = await response.json()
      ElMessage.success(result.message || '审核完成')
      approvalDialogVisible.value = false
      await loadPendingCancellations() // 重新加载列表
    } else {
      const error = await response.json()
      ElMessage.error(error.error || '审核失败')
    }
  } catch (error) {
    console.error('审核失败:', error)
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    processing.value = false
  }
}

// 生命周期
onMounted(() => {
  loadPendingCancellations()
})
</script>

<style scoped>
.cancellation-approval {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
  color: #303133;
}

.content {
  min-height: 400px;
}

.cancellation-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cancellation-card {
  border-radius: 8px;
}

.cancellation-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.student-info h3 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 18px;
}

.student-info p {
  margin: 4px 0;
  color: #606266;
  font-size: 14px;
}

.request-info {
  text-align: right;
}

.request-info p {
  margin: 4px 0;
  color: #909399;
  font-size: 12px;
}

.cancellation-reason {
  background-color: #f5f7fa;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 16px;
}

.cancellation-reason h4 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 14px;
}

.cancellation-reason p {
  margin: 0;
  color: #606266;
  line-height: 1.5;
}

.cancellation-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #909399;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  color: #c0c4cc;
}

.empty-state h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}

.approval-content {
  padding: 0 4px;
}

.booking-summary {
  background-color: #f5f7fa;
  padding: 16px;
  border-radius: 4px;
  margin-bottom: 16px;
}

.booking-summary h4 {
  margin: 0 0 12px 0;
  color: #303133;
}

.booking-summary p {
  margin: 6px 0;
  color: #606266;
}

.reason-display {
  margin-bottom: 16px;
}

.reason-display h4 {
  margin: 0 0 8px 0;
  color: #303133;
}

.reason-display p {
  margin: 0;
  color: #606266;
  background-color: #f5f7fa;
  padding: 12px;
  border-radius: 4px;
  line-height: 1.5;
}
</style>