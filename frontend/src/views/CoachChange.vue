<template>
  <div class="coach-change-container">
    <div class="page-header">
      <h1>教练更换</h1>
      <p class="page-description">申请更换教练或查看更换进度</p>
    </div>

    <!-- 学员视图 -->
    <div v-if="userStore.user?.user_type === 'student'" class="student-view">
      <!-- 申请新的教练更换 -->
      <div class="section-card">
        <h2>申请更换教练</h2>
        <el-form 
          ref="changeFormRef" 
          :model="changeForm" 
          :rules="changeFormRules" 
          label-width="120px"
          class="change-form"
        >
          <el-form-item label="当前教练" prop="current_coach">
            <el-select 
              v-model="changeForm.current_coach" 
              placeholder="选择当前教练"
              style="width: 100%"
            >
              <el-option
                v-for="coach in myCoaches"
                :key="coach.id"
                :label="`${coach.real_name} (${coach.username})`"
                :value="coach.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="目标教练" prop="target_coach">
            <el-select 
              v-model="changeForm.target_coach" 
              placeholder="选择目标教练"
              style="width: 100%"
            >
              <el-option
                v-for="coach in availableCoaches"
                :key="coach.id"
                :label="`${coach.real_name} (${coach.username}) - ${coach.level || '未设置'}`"
                :value="coach.id"
              >
                <div class="coach-option">
                  <span>{{ coach.real_name }} ({{ coach.username }})</span>
                  <div class="coach-info">
                    <span class="level">{{ coach.level || '未设置' }}</span>
                    <span class="rate" v-if="coach.hourly_rate">¥{{ coach.hourly_rate }}/小时</span>
                  </div>
                </div>
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="更换原因" prop="reason">
            <el-input
              v-model="changeForm.reason"
              type="textarea"
              :rows="4"
              placeholder="请详细说明更换教练的原因..."
              maxlength="500"
              show-word-limit
            />
          </el-form-item>

          <el-form-item>
            <el-button 
              type="primary" 
              @click="submitChangeRequest"
              :loading="submitting"
            >
              提交申请
            </el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 我的更换请求 -->
      <div class="section-card">
        <h2>我的更换请求</h2>
        <el-table 
          :data="myRequests" 
          v-loading="loading"
          empty-text="暂无更换请求"
        >
          <el-table-column prop="id" label="请求ID" width="80" />
          <el-table-column label="当前教练" width="120">
            <template #default="scope">
              {{ scope.row.current_coach.real_name }}
            </template>
          </el-table-column>
          <el-table-column label="目标教练" width="120">
            <template #default="scope">
              {{ scope.row.target_coach.real_name }}
            </template>
          </el-table-column>
          <el-table-column prop="reason" label="更换原因" min-width="200" show-overflow-tooltip />
          <el-table-column label="审批状态" width="300">
            <template #default="scope">
              <div class="approval-status">
                <el-tag 
                  :type="getApprovalTagType(scope.row.current_coach_approval)"
                  size="small"
                >
                  当前教练: {{ getApprovalText(scope.row.current_coach_approval) }}
                </el-tag>
                <el-tag 
                  :type="getApprovalTagType(scope.row.target_coach_approval)"
                  size="small"
                >
                  目标教练: {{ getApprovalText(scope.row.target_coach_approval) }}
                </el-tag>
                <el-tag 
                  :type="getApprovalTagType(scope.row.campus_admin_approval)"
                  size="small"
                >
                  管理员: {{ getApprovalText(scope.row.campus_admin_approval) }}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="总状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTagType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="申请时间" width="180">
            <template #default="scope">
              {{ formatDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="scope">
              <el-button 
                type="text" 
                size="small" 
                @click="viewRequestDetail(scope.row)"
              >
                查看详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 教练视图 -->
    <div v-else-if="userStore.user?.user_type === 'coach'" class="coach-view">
      <!-- 待我审批的请求 -->
      <div class="section-card">
        <h2>待我审批的更换请求</h2>
        <el-table 
          :data="pendingApprovals" 
          v-loading="loading"
          empty-text="暂无待审批请求"
        >
          <el-table-column prop="id" label="请求ID" width="80" />
          <el-table-column label="学员" width="120">
            <template #default="scope">
              {{ scope.row.student.real_name }}
            </template>
          </el-table-column>
          <el-table-column label="当前教练" width="120">
            <template #default="scope">
              {{ scope.row.current_coach.real_name }}
            </template>
          </el-table-column>
          <el-table-column label="目标教练" width="120">
            <template #default="scope">
              {{ scope.row.target_coach.real_name }}
            </template>
          </el-table-column>
          <el-table-column prop="reason" label="更换原因" min-width="200" show-overflow-tooltip />
          <el-table-column label="我的角色" width="100">
            <template #default="scope">
              <el-tag v-if="scope.row.current_coach.id === userStore.user.id" type="warning">
                当前教练
              </el-tag>
              <el-tag v-else-if="scope.row.target_coach.id === userStore.user.id" type="success">
                目标教练
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="申请时间" width="180">
            <template #default="scope">
              {{ formatDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button 
                type="success" 
                size="small" 
                @click="approveRequest(scope.row, 'approve')"
              >
                同意
              </el-button>
              <el-button 
                type="danger" 
                size="small" 
                @click="approveRequest(scope.row, 'reject')"
              >
                拒绝
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 相关的更换请求 -->
      <div class="section-card">
        <h2>相关的更换请求</h2>
        <el-table 
          :data="relatedRequests" 
          v-loading="loading"
          empty-text="暂无相关请求"
        >
          <el-table-column prop="id" label="请求ID" width="80" />
          <el-table-column label="学员" width="120">
            <template #default="scope">
              {{ scope.row.student.real_name }}
            </template>
          </el-table-column>
          <el-table-column label="当前教练" width="120">
            <template #default="scope">
              {{ scope.row.current_coach.real_name }}
            </template>
          </el-table-column>
          <el-table-column label="目标教练" width="120">
            <template #default="scope">
              {{ scope.row.target_coach.real_name }}
            </template>
          </el-table-column>
          <el-table-column label="审批状态" width="300">
            <template #default="scope">
              <div class="approval-status">
                <el-tag 
                  :type="getApprovalTagType(scope.row.current_coach_approval)"
                  size="small"
                >
                  当前教练: {{ getApprovalText(scope.row.current_coach_approval) }}
                </el-tag>
                <el-tag 
                  :type="getApprovalTagType(scope.row.target_coach_approval)"
                  size="small"
                >
                  目标教练: {{ getApprovalText(scope.row.target_coach_approval) }}
                </el-tag>
                <el-tag 
                  :type="getApprovalTagType(scope.row.campus_admin_approval)"
                  size="small"
                >
                  管理员: {{ getApprovalText(scope.row.campus_admin_approval) }}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="总状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTagType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="申请时间" width="180">
            <template #default="scope">
              {{ formatDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 管理员视图 -->
    <div v-else-if="userStore.user?.user_type === 'campus_admin'" class="admin-view">
      <!-- 统计信息 -->
      <div class="stats-cards">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ statistics.total_requests }}</div>
            <div class="stat-label">总请求数</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ statistics.pending_requests }}</div>
            <div class="stat-label">待处理</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ statistics.approved_requests }}</div>
            <div class="stat-label">已通过</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ statistics.approval_rate }}%</div>
            <div class="stat-label">通过率</div>
          </div>
        </el-card>
      </div>

      <!-- 待审批的请求 -->
      <div class="section-card">
        <h2>待我审批的更换请求</h2>
        <el-table 
          :data="pendingApprovals" 
          v-loading="loading"
          empty-text="暂无待审批请求"
        >
          <el-table-column prop="id" label="请求ID" width="80" />
          <el-table-column label="学员" width="120">
            <template #default="scope">
              {{ scope.row.student.real_name }}
            </template>
          </el-table-column>
          <el-table-column label="当前教练" width="120">
            <template #default="scope">
              {{ scope.row.current_coach.real_name }}
            </template>
          </el-table-column>
          <el-table-column label="目标教练" width="120">
            <template #default="scope">
              {{ scope.row.target_coach.real_name }}
            </template>
          </el-table-column>
          <el-table-column prop="reason" label="更换原因" min-width="200" show-overflow-tooltip />
          <el-table-column label="教练审批状态" width="200">
            <template #default="scope">
              <div class="approval-status">
                <el-tag 
                  :type="getApprovalTagType(scope.row.current_coach_approval)"
                  size="small"
                >
                  当前: {{ getApprovalText(scope.row.current_coach_approval) }}
                </el-tag>
                <el-tag 
                  :type="getApprovalTagType(scope.row.target_coach_approval)"
                  size="small"
                >
                  目标: {{ getApprovalText(scope.row.target_coach_approval) }}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="申请时间" width="180">
            <template #default="scope">
              {{ formatDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button 
                type="success" 
                size="small" 
                @click="approveRequest(scope.row, 'approve')"
              >
                同意
              </el-button>
              <el-button 
                type="danger" 
                size="small" 
                @click="approveRequest(scope.row, 'reject')"
              >
                拒绝
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 所有更换请求 -->
      <div class="section-card">
        <h2>所有更换请求</h2>
        <el-table 
          :data="allRequests" 
          v-loading="loading"
          empty-text="暂无更换请求"
        >
          <el-table-column prop="id" label="请求ID" width="80" />
          <el-table-column label="学员" width="120">
            <template #default="scope">
              {{ scope.row.student.real_name }}
            </template>
          </el-table-column>
          <el-table-column label="当前教练" width="120">
            <template #default="scope">
              {{ scope.row.current_coach.real_name }}
            </template>
          </el-table-column>
          <el-table-column label="目标教练" width="120">
            <template #default="scope">
              {{ scope.row.target_coach.real_name }}
            </template>
          </el-table-column>
          <el-table-column label="审批状态" width="300">
            <template #default="scope">
              <div class="approval-status">
                <el-tag 
                  :type="getApprovalTagType(scope.row.current_coach_approval)"
                  size="small"
                >
                  当前教练: {{ getApprovalText(scope.row.current_coach_approval) }}
                </el-tag>
                <el-tag 
                  :type="getApprovalTagType(scope.row.target_coach_approval)"
                  size="small"
                >
                  目标教练: {{ getApprovalText(scope.row.target_coach_approval) }}
                </el-tag>
                <el-tag 
                  :type="getApprovalTagType(scope.row.campus_admin_approval)"
                  size="small"
                >
                  管理员: {{ getApprovalText(scope.row.campus_admin_approval) }}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="总状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTagType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="申请时间" width="180">
            <template #default="scope">
              {{ formatDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 审批对话框 -->
    <el-dialog 
      v-model="approvalDialogVisible" 
      title="审批教练更换请求"
      width="500px"
    >
      <el-form :model="approvalForm" label-width="80px">
        <el-form-item label="操作">
          <el-tag :type="approvalForm.action === 'approve' ? 'success' : 'danger'">
            {{ approvalForm.action === 'approve' ? '同意' : '拒绝' }}
          </el-tag>
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="approvalForm.notes"
            type="textarea"
            :rows="4"
            placeholder="请输入审批备注（可选）..."
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="approvalDialogVisible = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="confirmApproval"
            :loading="submitting"
          >
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog 
      v-model="detailDialogVisible" 
      title="更换请求详情"
      width="600px"
    >
      <div v-if="selectedRequest" class="request-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="请求ID">{{ selectedRequest.id }}</el-descriptions-item>
          <el-descriptions-item label="学员">{{ selectedRequest.student.real_name }}</el-descriptions-item>
          <el-descriptions-item label="当前教练">{{ selectedRequest.current_coach.real_name }}</el-descriptions-item>
          <el-descriptions-item label="目标教练">{{ selectedRequest.target_coach.real_name }}</el-descriptions-item>
          <el-descriptions-item label="申请时间" :span="2">
            {{ formatDateTime(selectedRequest.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="更换原因" :span="2">
            {{ selectedRequest.reason }}
          </el-descriptions-item>
        </el-descriptions>

        <h4 style="margin-top: 20px;">审批进度</h4>
        <el-steps :active="getStepActive(selectedRequest)" finish-status="success">
          <el-step title="当前教练审批">
            <template #description>
              <div>
                状态: {{ getApprovalText(selectedRequest.current_coach_approval) }}
                <div v-if="selectedRequest.current_coach_approved_at">
                  时间: {{ formatDateTime(selectedRequest.current_coach_approved_at) }}
                </div>
                <div v-if="selectedRequest.current_coach_notes">
                  备注: {{ selectedRequest.current_coach_notes }}
                </div>
              </div>
            </template>
          </el-step>
          <el-step title="目标教练审批">
            <template #description>
              <div>
                状态: {{ getApprovalText(selectedRequest.target_coach_approval) }}
                <div v-if="selectedRequest.target_coach_approved_at">
                  时间: {{ formatDateTime(selectedRequest.target_coach_approved_at) }}
                </div>
                <div v-if="selectedRequest.target_coach_notes">
                  备注: {{ selectedRequest.target_coach_notes }}
                </div>
              </div>
            </template>
          </el-step>
          <el-step title="管理员审批">
            <template #description>
              <div>
                状态: {{ getApprovalText(selectedRequest.campus_admin_approval) }}
                <div v-if="selectedRequest.campus_admin_approved_at">
                  时间: {{ formatDateTime(selectedRequest.campus_admin_approved_at) }}
                </div>
                <div v-if="selectedRequest.campus_admin_notes">
                  备注: {{ selectedRequest.campus_admin_notes }}
                </div>
              </div>
            </template>
          </el-step>
        </el-steps>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import api from '@/utils/api'

const userStore = useUserStore()

// 响应式数据
const loading = ref(false)
const submitting = ref(false)
const approvalDialogVisible = ref(false)
const detailDialogVisible = ref(false)

// 表单数据
const changeForm = reactive({
  current_coach: '',
  target_coach: '',
  reason: ''
})

const approvalForm = reactive({
  action: '',
  notes: '',
  requestId: null
})

// 表单验证规则
const changeFormRules = {
  current_coach: [
    { required: true, message: '请选择当前教练', trigger: 'change' }
  ],
  target_coach: [
    { required: true, message: '请选择目标教练', trigger: 'change' }
  ],
  reason: [
    { required: true, message: '请输入更换原因', trigger: 'blur' },
    { min: 10, message: '更换原因至少10个字符', trigger: 'blur' }
  ]
}

// 数据列表
const myCoaches = ref([])
const availableCoaches = ref([])
const myRequests = ref([])
const pendingApprovals = ref([])
const relatedRequests = ref([])
const allRequests = ref([])
const statistics = ref({
  total_requests: 0,
  pending_requests: 0,
  approved_requests: 0,
  rejected_requests: 0,
  approval_rate: 0
})

const selectedRequest = ref(null)
const changeFormRef = ref(null)

// 计算属性
const filteredAvailableCoaches = computed(() => {
  return availableCoaches.value.filter(coach => 
    coach.id !== changeForm.current_coach
  )
})

// 方法
const loadData = async () => {
  loading.value = true
  try {
    await Promise.all([
      loadCoaches(),
      loadMyRequests(),
      loadPendingApprovals(),
      loadStatistics()
    ])
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

const loadCoaches = async () => {
  try {
    const response = await api.get('/api/reservations/coaches/')
    // coaches API 返回数组
    availableCoaches.value = Array.isArray(response.data) ? response.data : []
    
    // 如果是学员，获取我的教练
    if (userStore.user?.user_type === 'student') {
      const relationsResponse = await api.get('/api/reservations/relations/')
      // relations API 可能返回分页对象
      const relations = relationsResponse.data.results || relationsResponse.data || []
      const approvedRelations = relations.filter(r => r.status === 'approved')
      myCoaches.value = approvedRelations.map(r => ({
        id: r.coach.id,
        username: r.coach.username,
        real_name: r.coach.real_name
      }))
    }
  } catch (error) {
    console.error('加载教练列表失败:', error)
  }
}

const loadMyRequests = async () => {
  if (userStore.user?.user_type !== 'student') return
  
  try {
    const response = await api.get('/api/reservations/my-coach-change-requests/')
    // my-coach-change-requests 可能返回数组或分页对象
    myRequests.value = response.data.results || response.data || []
  } catch (error) {
    console.error('加载我的请求失败:', error)
  }
}

const loadPendingApprovals = async () => {
  if (userStore.user?.user_type === 'student') return
  
  try {
    const response = await api.get('/api/reservations/pending-coach-change-approvals/')
    // pending-coach-change-approvals 返回数组
    pendingApprovals.value = Array.isArray(response.data) ? response.data : []
    
    if (userStore.user?.user_type === 'coach') {
      // 教练还需要加载相关的请求
      const allResponse = await api.get('/api/reservations/coach-change-requests/')
      // coach-change-requests 返回分页对象
      relatedRequests.value = allResponse.data.results || allResponse.data || []
    } else if (userStore.user?.user_type === 'campus_admin') {
      // 管理员加载所有请求
      const allResponse = await api.get('/api/reservations/coach-change-requests/')
      // coach-change-requests 返回分页对象
      allRequests.value = allResponse.data.results || allResponse.data || []
    }
  } catch (error) {
    console.error('加载待审批请求失败:', error)
  }
}

const loadStatistics = async () => {
  if (userStore.user?.user_type === 'student') return
  
  try {
    const response = await api.get('/api/reservations/coach-change-statistics/')
    statistics.value = response.data
  } catch (error) {
    console.error('加载统计信息失败:', error)
  }
}

const submitChangeRequest = async () => {
  if (!changeFormRef.value) return
  
  const valid = await changeFormRef.value.validate().catch(() => false)
  if (!valid) return
  
  submitting.value = true
  try {
    // 转换字段名称以匹配后端序列化器
    const requestData = {
      current_coach_id: changeForm.current_coach,
      target_coach_id: changeForm.target_coach,
      reason: changeForm.reason
    }
    
    await api.post('/api/reservations/coach-change-requests/', requestData)
    ElMessage.success('教练更换申请提交成功')
    resetForm()
    await loadMyRequests()
  } catch (error) {
    console.error('提交申请失败:', error)
    // 处理不同类型的错误响应
    let errorMessage = '提交申请失败'
    if (error.response?.data) {
      if (error.response.data.non_field_errors) {
        errorMessage = error.response.data.non_field_errors[0]
      } else if (error.response.data.error) {
        errorMessage = error.response.data.error
      } else if (error.response.data.message) {
        errorMessage = error.response.data.message
      }
    }
    ElMessage.error(errorMessage)
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  if (changeFormRef.value) {
    changeFormRef.value.resetFields()
  }
  Object.assign(changeForm, {
    current_coach: '',
    target_coach: '',
    reason: ''
  })
}

const approveRequest = (request, action) => {
  approvalForm.action = action
  approvalForm.notes = ''
  approvalForm.requestId = request.id
  approvalDialogVisible.value = true
}

const confirmApproval = async () => {
  submitting.value = true
  try {
    await api.post(`/api/reservations/coach-change-requests/${approvalForm.requestId}/approve/`, {
      action: approvalForm.action,
      notes: approvalForm.notes
    })
    
    ElMessage.success(`${approvalForm.action === 'approve' ? '同意' : '拒绝'}成功`)
    approvalDialogVisible.value = false
    await loadData()
  } catch (error) {
    console.error('审批失败:', error)
    ElMessage.error(error.response?.data?.error || '审批失败')
  } finally {
    submitting.value = false
  }
}

const viewRequestDetail = (request) => {
  selectedRequest.value = request
  detailDialogVisible.value = true
}

// 辅助方法
const getApprovalText = (approval) => {
  const map = {
    'pending': '待审批',
    'approved': '已同意',
    'rejected': '已拒绝'
  }
  return map[approval] || '未知'
}

const getApprovalTagType = (approval) => {
  const map = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger'
  }
  return map[approval] || 'info'
}

const getStatusText = (status) => {
  const map = {
    'pending': '待处理',
    'approved': '已通过',
    'rejected': '已拒绝'
  }
  return map[status] || '未知'
}

const getStatusTagType = (status) => {
  const map = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger'
  }
  return map[status] || 'info'
}

const getStepActive = (request) => {
  if (request.status === 'rejected') return -1
  if (request.campus_admin_approval === 'approved') return 3
  if (request.target_coach_approval === 'approved') return 2
  if (request.current_coach_approval === 'approved') return 1
  return 0
}

const formatDateTime = (dateTime) => {
  if (!dateTime) return '-'
  return new Date(dateTime).toLocaleString('zh-CN')
}

// 生命周期
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.coach-change-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 30px;
  text-align: center;
}

.page-header h1 {
  color: #303133;
  margin-bottom: 10px;
}

.page-description {
  color: #606266;
  font-size: 14px;
}

.section-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.section-card h2 {
  color: #303133;
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: 600;
}

.change-form {
  max-width: 600px;
}

.coach-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.coach-info {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #909399;
}

.level {
  background: #f0f9ff;
  color: #0369a1;
  padding: 2px 6px;
  border-radius: 4px;
}

.rate {
  background: #f0fdf4;
  color: #166534;
  padding: 2px 6px;
  border-radius: 4px;
}

.approval-status {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 20px;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 8px;
}

.stat-label {
  color: #606266;
  font-size: 14px;
}

.request-detail {
  padding: 10px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .coach-change-container {
    padding: 10px;
  }
  
  .section-card {
    padding: 16px;
  }
  
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .approval-status {
    flex-direction: column;
  }
}
</style>