<template>
  <div class="user-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon><User /></el-icon>
        用户管理
      </h2>
      <p class="page-description">管理系统中的所有用户信息和审核</p>
    </div>

    <!-- 标签页 -->
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <!-- 待审核用户 -->
      <el-tab-pane label="待审核用户" name="pending">
        <div class="tab-content">
          <!-- 筛选器 -->
          <div class="filters custom-card">
            <el-row :gutter="16">
              <el-col :span="6">
                <el-input
                  v-model="pendingFilters.search"
                  placeholder="搜索用户名、姓名..."
                  clearable
                  @input="handlePendingSearch"
                >
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-input>
              </el-col>
              <el-col :span="4">
                <el-select v-model="pendingFilters.user_type" placeholder="用户类型" @change="fetchPendingUsers">
                  <el-option label="全部" value="" />
                  <el-option label="学员" value="student" />
                  <el-option label="教练员" value="coach" />
                  <el-option label="校区管理员" value="campus_admin" />
                </el-select>
              </el-col>
              <el-col :span="4">
                <el-button @click="resetPendingFilters">
                  <el-icon><Refresh /></el-icon>
                  重置
                </el-button>
              </el-col>
            </el-row>
          </div>

          <!-- 待审核用户列表 -->
          <div class="user-list custom-card">
            <el-table
              :data="pendingUsers"
              v-loading="pendingLoading"
              stripe
              style="width: 100%"
            >
              <el-table-column prop="username" label="用户名" width="120" />
              
              <el-table-column prop="real_name" label="真实姓名" width="100" />
              
              <el-table-column prop="email" label="邮箱" min-width="180" />
              
              <el-table-column prop="phone" label="手机号" width="120" />
              
              <el-table-column label="用户类型" width="100">
                <template #default="{ row }">
                  <el-tag :type="getUserTypeColor(row.user_type)">
                    {{ getUserTypeText(row.user_type) }}
                  </el-tag>
                </template>
              </el-table-column>
              
              <el-table-column label="申请校区" width="120">
                <template #default="{ row }">
                  <span v-if="row.campus">{{ row.campus.name }}</span>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              
              <el-table-column prop="created_at" label="申请时间" width="160">
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" size="small" @click="viewUserDetail(row)">
                    查看
                  </el-button>
                  <el-button type="success" size="small" @click="approveUser(row)">
                    通过
                  </el-button>
                  <el-button type="danger" size="small" @click="rejectUser(row)">
                    拒绝
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <!-- 分页 -->
            <div class="pagination" v-if="pendingTotal > 0">
              <el-pagination
                v-model:current-page="pendingCurrentPage"
                v-model:page-size="pendingPageSize"
                :page-sizes="[10, 20, 50]"
                :total="pendingTotal"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handlePendingSizeChange"
                @current-change="handlePendingCurrentChange"
              />
            </div>
          </div>
        </div>
      </el-tab-pane>

      <!-- 已审核用户 -->
      <el-tab-pane label="已审核用户" name="approved">
        <div class="tab-content">
          <!-- 筛选器 -->
          <div class="filters custom-card">
            <el-row :gutter="16">
              <el-col :span="6">
                <el-input
                  v-model="approvedFilters.search"
                  placeholder="搜索用户名、姓名..."
                  clearable
                  @input="handleApprovedSearch"
                >
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-input>
              </el-col>
              <el-col :span="4">
                <el-select v-model="approvedFilters.user_type" placeholder="用户类型" @change="fetchApprovedUsers">
                  <el-option label="全部" value="" />
                  <el-option label="学员" value="student" />
                  <el-option label="教练员" value="coach" />
                  <el-option label="校区管理员" value="campus_admin" />
                </el-select>
              </el-col>
              <el-col :span="4">
                <el-select v-model="approvedFilters.is_active" placeholder="状态" @change="fetchApprovedUsers">
                  <el-option label="全部" value="" />
                  <el-option label="启用" value="true" />
                  <el-option label="禁用" value="false" />
                </el-select>
              </el-col>
              <el-col :span="4">
                <el-button @click="resetApprovedFilters">
                  <el-icon><Refresh /></el-icon>
                  重置
                </el-button>
              </el-col>
            </el-row>
          </div>

          <!-- 已审核用户列表 -->
          <div class="user-list custom-card">
            <el-table
              :data="approvedUsers"
              v-loading="approvedLoading"
              stripe
              style="width: 100%"
            >
              <el-table-column prop="username" label="用户名" width="120" />
              
              <el-table-column prop="real_name" label="真实姓名" width="100" />
              
              <el-table-column prop="email" label="邮箱" min-width="180" />
              
              <el-table-column prop="phone" label="手机号" width="120" />
              
              <el-table-column label="用户类型" width="100">
                <template #default="{ row }">
                  <el-tag :type="getUserTypeColor(row.user_type)">
                    {{ getUserTypeText(row.user_type) }}
                  </el-tag>
                </template>
              </el-table-column>
              
              <el-table-column label="所属校区" width="120">
                <template #default="{ row }">
                  <span v-if="row.campus">{{ row.campus.name }}</span>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              
              <el-table-column label="状态" width="80">
                <template #default="{ row }">
                  <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
                    {{ row.is_active ? '启用' : '禁用' }}
                  </el-tag>
                </template>
              </el-table-column>
              
              <el-table-column prop="last_login" label="最后登录" width="160">
                <template #default="{ row }">
                  {{ formatDate(row.last_login) }}
                </template>
              </el-table-column>
              
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" size="small" @click="viewUserDetail(row)">
                    查看
                  </el-button>
                  <el-button type="warning" size="small" @click="editUser(row)" v-if="canEditUser(row)">
                    编辑
                  </el-button>
                  <el-button 
                    :type="row.is_active ? 'danger' : 'success'" 
                    size="small" 
                    @click="toggleUserStatus(row)"
                    v-if="canToggleStatus(row)"
                  >
                    {{ row.is_active ? '禁用' : '启用' }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <!-- 分页 -->
            <div class="pagination" v-if="approvedTotal > 0">
              <el-pagination
                v-model:current-page="approvedCurrentPage"
                v-model:page-size="approvedPageSize"
                :page-sizes="[10, 20, 50]"
                :total="approvedTotal"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleApprovedSizeChange"
                @current-change="handleApprovedCurrentChange"
              />
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 用户详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="用户详情"
      width="700px"
    >
      <div v-if="selectedUser" class="user-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="用户名">{{ selectedUser.username }}</el-descriptions-item>
          <el-descriptions-item label="真实姓名">{{ selectedUser.real_name }}</el-descriptions-item>
          <el-descriptions-item label="用户类型">
            <el-tag :type="getUserTypeColor(selectedUser.user_type)">
              {{ getUserTypeText(selectedUser.user_type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="selectedUser.is_active ? 'success' : 'danger'">
              {{ selectedUser.is_active ? '启用' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="邮箱" :span="2">{{ selectedUser.email }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ selectedUser.phone }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ selectedUser.gender === 'M' ? '男' : selectedUser.gender === 'F' ? '女' : '未设置' }}</el-descriptions-item>
          <el-descriptions-item label="出生日期" :span="2">{{ selectedUser.birth_date || '未设置' }}</el-descriptions-item>
          <el-descriptions-item label="所属校区" :span="2">
            {{ selectedUser.campus?.name || '未分配' }}
          </el-descriptions-item>
          <el-descriptions-item label="注册时间" :span="2">{{ formatDate(selectedUser.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="最后登录" :span="2">{{ formatDate(selectedUser.last_login) }}</el-descriptions-item>
          <el-descriptions-item label="审核状态" :span="2">
            <el-tag v-if="selectedUser.is_approved === null" type="warning">待审核</el-tag>
            <el-tag v-else-if="selectedUser.is_approved" type="success">已通过</el-tag>
            <el-tag v-else type="danger">已拒绝</el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>

    <!-- 编辑用户对话框 -->
    <el-dialog
      v-model="showEditDialog"
      title="编辑用户"
      width="600px"
      @close="resetEditForm"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-width="100px"
      >
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="editForm.real_name" placeholder="请输入真实姓名" />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="editForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        
        <el-form-item label="性别">
          <el-radio-group v-model="editForm.gender">
            <el-radio label="M">男</el-radio>
            <el-radio label="F">女</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="出生日期">
          <el-date-picker
            v-model="editForm.birth_date"
            type="date"
            placeholder="选择出生日期"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="所属校区" v-if="userStore.user?.user_type === 'super_admin'">
          <el-select v-model="editForm.campus_id" placeholder="选择校区" style="width: 100%">
            <el-option
              v-for="campus in campusList"
              :key="campus.id"
              :label="campus.name"
              :value="campus.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-switch v-model="editForm.is_active" active-text="启用" inactive-text="禁用" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveUser" :loading="saving">
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import {
  User,
  Search,
  Refresh,
  Edit,
  Delete,
  View
} from '@element-plus/icons-vue'
import axios from '@/utils/axios'

const userStore = useUserStore()

// 响应式数据
const activeTab = ref('pending')
const pendingUsers = ref([])
const approvedUsers = ref([])
const campusList = ref([])
const pendingLoading = ref(false)
const approvedLoading = ref(false)
const saving = ref(false)

// 分页数据
const pendingCurrentPage = ref(1)
const pendingPageSize = ref(10)
const pendingTotal = ref(0)
const approvedCurrentPage = ref(1)
const approvedPageSize = ref(10)
const approvedTotal = ref(0)

// 对话框状态
const showDetailDialog = ref(false)
const showEditDialog = ref(false)

// 选中的用户
const selectedUser = ref(null)

// 筛选器
const pendingFilters = reactive({
  search: '',
  user_type: ''
})

const approvedFilters = reactive({
  search: '',
  user_type: '',
  is_active: ''
})

// 编辑表单
const editForm = reactive({
  real_name: '',
  email: '',
  phone: '',
  gender: '',
  birth_date: '',
  campus_id: null,
  is_active: true
})

// 编辑表单验证规则
const editRules = {
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

// 获取待审核用户列表
const fetchPendingUsers = async () => {
  try {
    pendingLoading.value = true
    const params = {
      page: pendingCurrentPage.value,
      page_size: pendingPageSize.value,
      search: pendingFilters.search || undefined,
      user_type: pendingFilters.user_type || undefined,
      is_approved: 'null'
    }
    
    const response = await axios.get('/accounts/api/users/', { params })
    if (response.data.success) {
      pendingUsers.value = response.data.data
      pendingTotal.value = response.data.count || response.data.data.length
    }
  } catch (error) {
    ElMessage.error('获取待审核用户列表失败')
    console.error('获取待审核用户列表失败:', error)
  } finally {
    pendingLoading.value = false
  }
}

// 获取已审核用户列表
const fetchApprovedUsers = async () => {
  try {
    approvedLoading.value = true
    const params = {
      page: approvedCurrentPage.value,
      page_size: approvedPageSize.value,
      search: approvedFilters.search || undefined,
      user_type: approvedFilters.user_type || undefined,
      is_active: approvedFilters.is_active || undefined,
      is_approved: 'true'
    }
    
    const response = await axios.get('/accounts/api/users/', { params })
    if (response.data.success) {
      approvedUsers.value = response.data.data
      approvedTotal.value = response.data.count || response.data.data.length
    }
  } catch (error) {
    ElMessage.error('获取已审核用户列表失败')
    console.error('获取已审核用户列表失败:', error)
  } finally {
    approvedLoading.value = false
  }
}

// 获取校区列表
const fetchCampusList = async () => {
  try {
    const response = await axios.get('/api/campus/api/list/')
    if (response.data.success) {
      campusList.value = response.data.data
    }
  } catch (error) {
    console.error('获取校区列表失败:', error)
  }
}

// 标签页切换
const handleTabChange = (tab) => {
  if (tab === 'pending') {
    fetchPendingUsers()
  } else if (tab === 'approved') {
    fetchApprovedUsers()
  }
}

// 搜索处理
const handlePendingSearch = () => {
  pendingCurrentPage.value = 1
  fetchPendingUsers()
}

const handleApprovedSearch = () => {
  approvedCurrentPage.value = 1
  fetchApprovedUsers()
}

// 重置筛选器
const resetPendingFilters = () => {
  pendingFilters.search = ''
  pendingFilters.user_type = ''
  pendingCurrentPage.value = 1
  fetchPendingUsers()
}

const resetApprovedFilters = () => {
  approvedFilters.search = ''
  approvedFilters.user_type = ''
  approvedFilters.is_active = ''
  approvedCurrentPage.value = 1
  fetchApprovedUsers()
}

// 分页处理
const handlePendingSizeChange = (size) => {
  pendingPageSize.value = size
  pendingCurrentPage.value = 1
  fetchPendingUsers()
}

const handlePendingCurrentChange = (page) => {
  pendingCurrentPage.value = page
  fetchPendingUsers()
}

const handleApprovedSizeChange = (size) => {
  approvedPageSize.value = size
  approvedCurrentPage.value = 1
  fetchApprovedUsers()
}

const handleApprovedCurrentChange = (page) => {
  approvedCurrentPage.value = page
  fetchApprovedUsers()
}

// 权限检查
const canEditUser = (user) => {
  return userStore.user?.user_type === 'super_admin' || 
         (userStore.user?.user_type === 'campus_admin' && user.campus?.id === userStore.user?.campus?.id)
}

const canToggleStatus = (user) => {
  return userStore.user?.user_type === 'super_admin' || 
         (userStore.user?.user_type === 'campus_admin' && user.campus?.id === userStore.user?.campus?.id)
}

// 查看用户详情
const viewUserDetail = (user) => {
  selectedUser.value = user
  showDetailDialog.value = true
}

// 编辑用户
const editUser = (user) => {
  selectedUser.value = user
  Object.assign(editForm, {
    real_name: user.real_name,
    email: user.email,
    phone: user.phone,
    gender: user.gender,
    birth_date: user.birth_date,
    campus_id: user.campus?.id,
    is_active: user.is_active
  })
  showEditDialog.value = true
}

// 审核用户
const approveUser = async (user) => {
  try {
    await ElMessageBox.confirm(
      `确定要通过用户 "${user.real_name}" 的申请吗？`,
      '确认审核',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }
    )
    
    const response = await axios.post(`/accounts/api/users/${user.id}/approve/`)
    if (response.data.success) {
      ElMessage.success('用户审核通过')
      fetchPendingUsers()
    } else {
      ElMessage.error(response.data.message || '审核失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('审核用户失败')
      console.error('审核用户失败:', error)
    }
  }
}

// 拒绝用户
const rejectUser = async (user) => {
  try {
    await ElMessageBox.confirm(
      `确定要拒绝用户 "${user.real_name}" 的申请吗？`,
      '确认拒绝',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await axios.post(`/accounts/api/users/${user.id}/reject/`)
    if (response.data.success) {
      ElMessage.success('用户申请已拒绝')
      fetchPendingUsers()
    } else {
      ElMessage.error(response.data.message || '拒绝失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('拒绝用户失败')
      console.error('拒绝用户失败:', error)
    }
  }
}

// 切换用户状态
const toggleUserStatus = async (user) => {
  try {
    const action = user.is_active ? '禁用' : '启用'
    await ElMessageBox.confirm(
      `确定要${action}用户 "${user.real_name}" 吗？`,
      `确认${action}`,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await axios.post(`/accounts/api/users/${user.id}/toggle-status/`)
    if (response.data.success) {
      ElMessage.success(`用户${action}成功`)
      fetchApprovedUsers()
    } else {
      ElMessage.error(response.data.message || `${action}失败`)
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(`${user.is_active ? '禁用' : '启用'}用户失败`)
      console.error('切换用户状态失败:', error)
    }
  }
}

// 保存用户编辑
const saveUser = async () => {
  try {
    const editFormRef = ref()
    await editFormRef.value.validate()
    
    saving.value = true
    const response = await axios.put(`/accounts/api/users/${selectedUser.value.id}/`, editForm)
    
    if (response.data.success) {
      ElMessage.success('用户信息更新成功')
      showEditDialog.value = false
      if (activeTab.value === 'approved') {
        fetchApprovedUsers()
      } else {
        fetchPendingUsers()
      }
    } else {
      ElMessage.error(response.data.message || '更新失败')
    }
  } catch (error) {
    ElMessage.error('更新用户信息失败')
    console.error('更新用户信息失败:', error)
  } finally {
    saving.value = false
  }
}

// 重置编辑表单
const resetEditForm = () => {
  selectedUser.value = null
  Object.assign(editForm, {
    real_name: '',
    email: '',
    phone: '',
    gender: '',
    birth_date: '',
    campus_id: null,
    is_active: true
  })
}

// 获取用户类型文本
const getUserTypeText = (type) => {
  const typeMap = {
    'student': '学员',
    'coach': '教练员',
    'campus_admin': '校区管理员',
    'super_admin': '超级管理员'
  }
  return typeMap[type] || type
}

// 获取用户类型颜色
const getUserTypeColor = (type) => {
  const colorMap = {
    'student': 'primary',
    'coach': 'success',
    'campus_admin': 'warning',
    'super_admin': 'danger'
  }
  return colorMap[type] || 'info'
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 组件挂载时获取数据
onMounted(() => {
  fetchPendingUsers()
  fetchCampusList()
})
</script>

<style scoped>
.user-management {
  padding: 24px;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-description {
  color: #666;
  margin: 0;
}

.tab-content {
  margin-top: 16px;
}

.filters {
  padding: 20px;
  margin-bottom: 24px;
}

.user-list {
  padding: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.user-detail {
  padding: 16px 0;
}

.custom-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>