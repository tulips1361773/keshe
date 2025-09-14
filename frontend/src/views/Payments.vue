<template>
  <div class="payments-container">
    <div class="header">
      <h1>支付管理</h1>
      <div class="header-buttons">
        <el-button type="primary" @click="showRechargeDialog = true">
          <el-icon><CreditCard /></el-icon>
          账户充值
        </el-button>
        <el-button v-if="isAdmin" type="success" @click="showAdminPaymentDialog = true">
          <el-icon><Money /></el-icon>
          线下支付录入
        </el-button>
      </div>
    </div>

    <!-- 账户余额卡片 -->
    <el-card class="balance-card">
      <div class="balance-info">
        <div class="balance-item">
          <span class="label">账户余额</span>
          <span class="amount">¥{{ accountBalance.toFixed(2) }}</span>
        </div>
        <div class="balance-item">
          <span class="label">冻结金额</span>
          <span class="amount frozen">¥{{ frozenAmount.toFixed(2) }}</span>
        </div>
        <div class="balance-item">
          <span class="label">可用余额</span>
          <span class="amount available">¥{{ availableBalance.toFixed(2) }}</span>
        </div>
      </div>
    </el-card>

    <!-- 筛选条件 -->
    <el-card class="filter-card">
      <el-form :model="filters" inline>
        <el-form-item label="交易类型">
          <el-select v-model="filters.transaction_type" placeholder="选择类型" clearable>
            <el-option label="充值" value="recharge" />
            <el-option label="支付" value="payment" />
            <el-option label="退款" value="refund" />
            <el-option label="冻结" value="freeze" />
            <el-option label="解冻" value="unfreeze" />
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
          <el-button type="primary" @click="loadTransactions">查询</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 交易记录列表 -->
    <el-card class="list-card">
      <el-table :data="transactions" v-loading="loading" stripe>
        <el-table-column prop="id" label="交易ID" width="80" />
        <el-table-column label="交易类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getTransactionTypeTag(row.transaction_type)">
              {{ getTransactionTypeText(row.transaction_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="金额" width="120">
          <template #default="{ row }">
            <span :class="getAmountClass(row.transaction_type)">
              {{ formatAmount(row.amount, row.transaction_type) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
        <el-table-column label="交易时间" width="160">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button size="small" @click="viewDetail(row)">详情</el-button>
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
          @size-change="loadTransactions"
          @current-change="loadTransactions"
        />
      </div>
    </el-card>

    <!-- 充值对话框 -->
    <el-dialog v-model="showRechargeDialog" title="账户充值" width="500px">
      <el-form :model="rechargeForm" :rules="rechargeRules" ref="rechargeFormRef" label-width="100px">
        <el-form-item label="充值金额" prop="amount">
          <el-input-number 
            v-model="rechargeForm.amount" 
            :min="1" 
            :max="10000"
            :precision="2" 
            style="width: 100%"
            placeholder="请输入充值金额"
          />
          <div class="form-tip">单次充值金额：1-10000元</div>
        </el-form-item>
        <el-form-item label="支付方式" prop="payment_method_id">
          <el-radio-group v-model="rechargeForm.payment_method_id">
            <el-radio :label="1">现金支付</el-radio>
            <el-radio :label="2">微信支付</el-radio>
            <el-radio :label="3">支付宝</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注">
          <el-input 
            v-model="rechargeForm.description" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入备注信息（可选）"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRechargeDialog = false">取消</el-button>
        <el-button type="primary" @click="submitRecharge" :loading="rechargeLoading">
          确认充值
        </el-button>
      </template>
    </el-dialog>

    <!-- 管理员线下支付录入对话框 -->
    <el-dialog v-model="showAdminPaymentDialog" title="线下支付录入" width="600px">
      <el-form :model="adminPaymentForm" :rules="adminPaymentRules" ref="adminPaymentFormRef" label-width="120px">
        <el-form-item label="选择学员" prop="student_id">
          <el-select 
            v-model="adminPaymentForm.student_id" 
            placeholder="请选择学员" 
            filterable 
            remote 
            :remote-method="searchStudents"
            :loading="studentsLoading"
            style="width: 100%"
          >
            <el-option 
              v-for="student in students" 
              :key="student.id" 
              :label="`${student.real_name} (${student.username})`" 
              :value="student.id"
            />
          </el-select>
          <div class="form-tip">输入学员姓名或用户名进行搜索</div>
        </el-form-item>
        <el-form-item label="支付金额" prop="amount">
          <el-input-number 
            v-model="adminPaymentForm.amount" 
            :min="1" 
            :max="10000"
            :precision="2" 
            style="width: 100%"
            placeholder="请输入支付金额"
          />
          <div class="form-tip">单次录入金额：1-10000元</div>
        </el-form-item>
        <el-form-item label="支付类型" prop="payment_type">
          <el-select v-model="adminPaymentForm.payment_type" placeholder="请选择支付类型" style="width: 100%">
            <el-option label="课程费用" value="course_fee" />
            <el-option label="注册费" value="registration_fee" />
            <el-option label="器材费" value="equipment_fee" />
            <el-option label="会员费" value="membership_fee" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注说明" prop="description">
          <el-input 
            v-model="adminPaymentForm.description" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入线下支付的详细说明"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAdminPaymentDialog = false">取消</el-button>
        <el-button type="primary" @click="submitAdminPayment" :loading="adminPaymentLoading">
          确认录入
        </el-button>
      </template>
    </el-dialog>

    <!-- 交易详情对话框 -->
    <el-dialog v-model="showDetailDialog" title="交易详情" width="600px">
      <el-descriptions v-if="selectedTransaction" :column="2" border>
        <el-descriptions-item label="交易ID">
          {{ selectedTransaction.id }}
        </el-descriptions-item>
        <el-descriptions-item label="交易类型">
          <el-tag :type="getTransactionTypeTag(selectedTransaction.transaction_type)">
            {{ getTransactionTypeText(selectedTransaction.transaction_type) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="交易金额">
          <span :class="getAmountClass(selectedTransaction.transaction_type)">
            {{ formatAmount(selectedTransaction.amount, selectedTransaction.transaction_type) }}
          </span>
        </el-descriptions-item>
        <el-descriptions-item label="交易状态">
          <el-tag :type="getStatusType(selectedTransaction.status)">
            {{ getStatusText(selectedTransaction.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="交易时间" :span="2">
          {{ formatDateTime(selectedTransaction.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ selectedTransaction.description || '无' }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { CreditCard, Money } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import axios from '@/utils/axios'

const userStore = useUserStore()

// 管理员权限检查
const isAdmin = computed(() => userStore.isAdmin)

// 响应式数据
const loading = ref(false)
const transactions = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 账户信息
const accountBalance = ref(0)
const frozenAmount = ref(0)
const availableBalance = computed(() => accountBalance.value - frozenAmount.value)

// 筛选条件
const filters = reactive({
  transaction_type: '',
  date_from: '',
  date_to: ''
})

const dateRange = ref([])

// 对话框状态
const showRechargeDialog = ref(false)
const showDetailDialog = ref(false)
const showAdminPaymentDialog = ref(false)
const selectedTransaction = ref(null)

// 充值表单
const rechargeFormRef = ref()
const rechargeLoading = ref(false)
const rechargeForm = reactive({
  amount: null,
  payment_method_id: 1, // 默认使用第一个支付方式
  description: ''
})

const rechargeRules = {
  amount: [
    { required: true, message: '请输入充值金额', trigger: 'blur' },
    { type: 'number', min: 1, max: 10000, message: '充值金额必须在1-10000元之间', trigger: 'blur' }
  ],
  payment_method_id: [
    { required: true, message: '请选择支付方式', trigger: 'change' }
  ]
}

// 管理员线下支付录入表单
const adminPaymentFormRef = ref()
const adminPaymentLoading = ref(false)
const adminPaymentForm = reactive({
  student_id: null,
  amount: null,
  payment_type: 'course_fee',
  description: ''
})

const adminPaymentRules = {
  student_id: [
    { required: true, message: '请选择学员', trigger: 'change' }
  ],
  amount: [
    { required: true, message: '请输入支付金额', trigger: 'blur' },
    { type: 'number', min: 1, max: 10000, message: '支付金额必须在1-10000元之间', trigger: 'blur' }
  ],
  payment_type: [
    { required: true, message: '请选择支付类型', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入备注说明', trigger: 'blur' }
  ]
}

// 学员搜索相关
const students = ref([])
const studentsLoading = ref(false)

// 方法
const loadAccountInfo = async () => {
  try {
    const response = await axios.get('/api/payments/api/account/')
    if (response.data) {
      accountBalance.value = parseFloat(response.data.balance || 0)
      frozenAmount.value = parseFloat(response.data.frozen_amount || 0)
    }
  } catch (error) {
    console.error('加载账户信息错误:', error)
    ElMessage.error('加载账户信息失败')
  }
}

const loadTransactions = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      ...filters
    }
    
    const response = await axios.get('/api/payments/api/account/transactions/', { params })
    
    if (response.data) {
      transactions.value = response.data.results || []
      total.value = response.data.count || 0
    }
  } catch (error) {
    console.error('加载交易记录错误:', error)
    ElMessage.error('加载交易记录失败')
  } finally {
    loading.value = false
  }
}

const submitRecharge = async () => {
  if (!rechargeFormRef.value) return
  
  try {
    await rechargeFormRef.value.validate()
    rechargeLoading.value = true
    
    await axios.post('/api/payments/api/account/recharge/', rechargeForm)
    
    ElMessage.success('充值申请提交成功')
    showRechargeDialog.value = false
    Object.assign(rechargeForm, {
      amount: null,
      payment_method_id: 1,
      description: ''
    })
    loadAccountInfo()
    loadTransactions()
  } catch (error) {
    console.error('充值错误:', error)
    const message = error.response?.data?.error || '充值失败'
    ElMessage.error(message)
  } finally {
    rechargeLoading.value = false
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
    transaction_type: '',
    date_from: '',
    date_to: ''
  })
  dateRange.value = []
  loadTransactions()
}

const viewDetail = (transaction) => {
  selectedTransaction.value = transaction
  showDetailDialog.value = true
}

// 管理员线下支付录入相关方法
const searchStudents = async (query) => {
  if (!query || query.length < 2) {
    students.value = []
    return
  }
  
  studentsLoading.value = true
  try {
    const response = await axios.get('/api/payments/api/admin/students/', {
      params: { search: query }
    })
    students.value = response.data.results || []
  } catch (error) {
    console.error('搜索学员失败:', error)
    ElMessage.error('搜索学员失败')
  } finally {
    studentsLoading.value = false
  }
}

const submitAdminPayment = async () => {
  if (!adminPaymentFormRef.value) return
  
  try {
    await adminPaymentFormRef.value.validate()
  } catch (error) {
    return
  }
  
  adminPaymentLoading.value = true
  try {
    await axios.post('/api/payments/api/admin/offline-payment/', adminPaymentForm)
    
    ElMessage.success('线下支付录入成功')
    showAdminPaymentDialog.value = false
    
    // 重置表单
    Object.assign(adminPaymentForm, {
      student_id: null,
      amount: null,
      payment_type: 'course_fee',
      description: ''
    })
    students.value = []
    
    // 刷新交易记录
    loadTransactions()
  } catch (error) {
    console.error('线下支付录入失败:', error)
    const message = error.response?.data?.message || '线下支付录入失败'
    ElMessage.error(message)
  } finally {
    adminPaymentLoading.value = false
  }
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

const getTransactionTypeTag = (type) => {
  const tags = {
    recharge: 'success',
    payment: 'warning',
    refund: 'info',
    freeze: 'danger',
    unfreeze: 'success'
  }
  return tags[type] || 'info'
}

const getTransactionTypeText = (type) => {
  const texts = {
    recharge: '充值',
    payment: '支付',
    refund: '退款',
    freeze: '冻结',
    unfreeze: '解冻'
  }
  return texts[type] || type
}

const getAmountClass = (type) => {
  return {
    'amount-positive': ['recharge', 'refund', 'unfreeze'].includes(type),
    'amount-negative': ['payment', 'freeze'].includes(type)
  }
}

const formatAmount = (amount, type) => {
  const prefix = ['recharge', 'refund', 'unfreeze'].includes(type) ? '+' : '-'
  return `${prefix}¥${Math.abs(amount).toFixed(2)}`
}

const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    processing: 'info',
    completed: 'success',
    failed: 'danger',
    cancelled: 'info'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待处理',
    processing: '处理中',
    completed: '已完成',
    failed: '失败',
    cancelled: '已取消'
  }
  return texts[status] || status
}

// 生命周期
onMounted(async () => {
  // 初始化用户认证状态
  const userStore = useUserStore()
  if (!userStore.isAuthenticated) {
    ElMessage.error('请先登录')
    return
  }
  
  // 确保认证头已设置
  await userStore.initializeAuth()
  
  // 加载数据
  loadAccountInfo()
  loadTransactions()
})
</script>

<style scoped>
.payments-container {
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

.header-buttons {
  display: flex;
  gap: 12px;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.balance-card {
  margin-bottom: 20px;
}

.balance-info {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 20px 0;
}

.balance-item {
  text-align: center;
}

.balance-item .label {
  display: block;
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.balance-item .amount {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.balance-item .amount.frozen {
  color: #F56C6C;
}

.balance-item .amount.available {
  color: #67C23A;
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

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.amount-positive {
  color: #67C23A;
  font-weight: bold;
}

.amount-negative {
  color: #F56C6C;
  font-weight: bold;
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