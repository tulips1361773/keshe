<template>
  <div class="recharge-approval-container">
    <div class="header">
      <h1>充值审核管理</h1>
      <el-button @click="loadPendingRecharges" :loading="loading" type="primary">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>

    <!-- 统计信息 -->
    <div class="stats-cards">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">{{ pendingCount }}</div>
          <div class="stat-label">待审核订单</div>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">¥{{ totalAmount.toFixed(2) }}</div>
          <div class="stat-label">待审核金额</div>
        </div>
      </el-card>
    </div>

    <!-- 待审核充值订单列表 -->
    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>待审核充值订单</span>
        </div>
      </template>

      <el-table 
        :data="rechargeList" 
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="payment_id" label="订单号" width="180" />
        <el-table-column label="用户信息" width="150">
          <template #default="scope">
            <div>
              <div class="user-name">{{ scope.row.user.real_name || scope.row.user.username }}</div>
              <div class="user-type">{{ scope.row.user.username }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="充值金额" width="120">
          <template #default="scope">
            <span class="amount-text">¥{{ parseFloat(scope.row.amount).toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="支付方式" width="120">
          <template #default="scope">
            <el-tag :type="getPaymentMethodType(scope.row.payment_method.method_type)">
              {{ scope.row.payment_method.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="备注" min-width="150" show-overflow-tooltip />
        <el-table-column prop="created_at" label="申请时间" width="180">
          <template #default="scope">
            {{ formatDateTime(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button 
              type="success" 
              size="small" 
              @click="approveRecharge(scope.row, true)"
              :loading="scope.row.approving"
            >
              通过
            </el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="showRejectDialog(scope.row)"
              :loading="scope.row.rejecting"
            >
              拒绝
            </el-button>
            <el-button 
              type="info" 
              size="small" 
              @click="viewDetail(scope.row)"
            >
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="totalCount"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 拒绝确认对话框 -->
    <el-dialog v-model="showRejectConfirm" title="拒绝充值" width="400px">
      <div class="reject-content">
        <p>确定要拒绝以下充值订单吗？</p>
        <div class="order-info" v-if="selectedOrder">
          <p><strong>订单号：</strong>{{ selectedOrder.payment_id }}</p>
          <p><strong>用户：</strong>{{ selectedOrder.user.real_name || selectedOrder.user.username }}</p>
          <p><strong>金额：</strong>¥{{ parseFloat(selectedOrder.amount).toFixed(2) }}</p>
        </div>
        <el-form :model="rejectForm" label-width="80px">
          <el-form-item label="拒绝原因">
            <el-input 
              v-model="rejectForm.reason" 
              type="textarea" 
              :rows="3" 
              placeholder="请输入拒绝原因（可选）"
            />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="showRejectConfirm = false">取消</el-button>
        <el-button type="danger" @click="confirmReject" :loading="rejecting">
          确认拒绝
        </el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="showDetailDialog" title="充值订单详情" width="600px">
      <div class="detail-content" v-if="selectedOrder">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ selectedOrder.payment_id }}</el-descriptions-item>
          <el-descriptions-item label="订单状态">
            <el-tag :type="getStatusType(selectedOrder.status)">
              {{ getStatusText(selectedOrder.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="用户姓名">{{ selectedOrder.user.real_name || selectedOrder.user.username }}</el-descriptions-item>
          <el-descriptions-item label="用户名">{{ selectedOrder.user.username }}</el-descriptions-item>
          <el-descriptions-item label="充值金额">¥{{ parseFloat(selectedOrder.amount).toFixed(2) }}</el-descriptions-item>
          <el-descriptions-item label="支付方式">{{ selectedOrder.payment_method.name }}</el-descriptions-item>
          <el-descriptions-item label="申请时间" :span="2">{{ formatDateTime(selectedOrder.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ selectedOrder.description || '无' }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="showDetailDialog = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

// 响应式数据
const loading = ref(false)
const rechargeList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)
const showRejectConfirm = ref(false)
const showDetailDialog = ref(false)
const selectedOrder = ref(null)
const rejecting = ref(false)

// 拒绝表单
const rejectForm = reactive({
  reason: ''
})

// 计算属性
const pendingCount = computed(() => totalCount.value)
const totalAmount = computed(() => {
  return rechargeList.value.reduce((sum, item) => sum + parseFloat(item.amount), 0)
})

// 方法
const loadPendingRecharges = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/payments/api/admin/pending-recharges/', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value
      }
    })
    
    if (response.data.code === 200) {
      rechargeList.value = response.data.data.results.map(item => ({
        ...item,
        approving: false,
        rejecting: false
      }))
      totalCount.value = response.data.data.count
    } else {
      ElMessage.error(response.data.message || '获取待审核充值订单失败')
    }
  } catch (error) {
    console.error('获取待审核充值订单失败:', error)
    ElMessage.error('获取待审核充值订单失败')
  } finally {
    loading.value = false
  }
}

const approveRecharge = async (order, approve) => {
  const action = approve ? '通过' : '拒绝'
  
  try {
    await ElMessageBox.confirm(
      `确定要${action}充值订单 ${order.payment_id} 吗？`,
      `${action}充值`,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: approve ? 'success' : 'warning'
      }
    )
    
    if (approve) {
      order.approving = true
    } else {
      order.rejecting = true
    }
    
    const response = await axios.post(
      `/api/payments/api/admin/recharge/${order.payment_id}/approve/`,
      { approve }
    )
    
    if (response.data.code === 200) {
      ElMessage.success(response.data.message)
      loadPendingRecharges() // 重新加载列表
    } else {
      ElMessage.error(response.data.message || `${action}充值订单失败`)
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error(`${action}充值订单失败:`, error)
      ElMessage.error(`${action}充值订单失败`)
    }
  } finally {
    if (approve) {
      order.approving = false
    } else {
      order.rejecting = false
    }
  }
}

const showRejectDialog = (order) => {
  selectedOrder.value = order
  rejectForm.reason = ''
  showRejectConfirm.value = true
}

const confirmReject = async () => {
  rejecting.value = true
  try {
    const response = await axios.post(
      `/api/payments/api/admin/recharge/${selectedOrder.value.payment_id}/approve/`,
      { 
        approve: false,
        reason: rejectForm.reason
      }
    )
    
    if (response.data.code === 200) {
      ElMessage.success(response.data.message)
      showRejectConfirm.value = false
      loadPendingRecharges() // 重新加载列表
    } else {
      ElMessage.error(response.data.message || '拒绝充值订单失败')
    }
  } catch (error) {
    console.error('拒绝充值订单失败:', error)
    ElMessage.error('拒绝充值订单失败')
  } finally {
    rejecting.value = false
  }
}

const viewDetail = (order) => {
  selectedOrder.value = order
  showDetailDialog.value = true
}

const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1
  loadPendingRecharges()
}

const handleCurrentChange = (newPage) => {
  currentPage.value = newPage
  loadPendingRecharges()
}

const getPaymentMethodType = (methodType) => {
  const types = {
    'cash': 'info',
    'wechat': 'success',
    'alipay': 'primary',
    'bank_card': 'warning'
  }
  return types[methodType] || 'info'
}

const getStatusType = (status) => {
  const types = {
    'pending': 'warning',
    'processing': 'info',
    'completed': 'success',
    'failed': 'danger',
    'cancelled': 'info'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    'pending': '待审核',
    'processing': '处理中',
    'completed': '已完成',
    'failed': '已拒绝',
    'cancelled': '已取消'
  }
  return texts[status] || status
}

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

// 生命周期
onMounted(async () => {
  // 初始化用户认证状态
  const userStore = useUserStore()
  if (!userStore.isAuthenticated) {
    ElMessage.error('请先登录')
    return
  }
  
  // 检查管理员权限
  if (!['super_admin', 'campus_admin'].includes(userStore.user?.user_type)) {
    ElMessage.error('权限不足，只有管理员可以访问此页面')
    return
  }
  
  // 确保认证头已设置
  await userStore.initializeAuth()
  
  // 加载数据
  loadPendingRecharges()
})
</script>

<style scoped>
.recharge-approval-container {
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

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 10px;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.table-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-name {
  font-weight: bold;
  color: #303133;
}

.user-type {
  font-size: 12px;
  color: #909399;
}

.amount-text {
  font-weight: bold;
  color: #E6A23C;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.reject-content {
  text-align: left;
}

.order-info {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin: 15px 0;
}

.order-info p {
  margin: 5px 0;
  color: #606266;
}

.detail-content {
  margin: 20px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .recharge-approval-container {
    padding: 10px;
  }
  
  .header {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }
  
  .stats-cards {
    grid-template-columns: 1fr;
  }
}
</style>