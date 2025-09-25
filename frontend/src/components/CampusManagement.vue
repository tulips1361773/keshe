<template>
  <div class="campus-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon><School /></el-icon>
        校区管理
      </h2>
      <p class="page-description">管理系统中的所有校区信息</p>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog = true" v-if="userStore.user?.user_type === 'super_admin'">
          <el-icon><Plus /></el-icon>
          新建校区
        </el-button>
      </div>
    </div>

    <!-- 筛选器 -->
    <div class="filters custom-card">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-input
            v-model="filters.search"
            placeholder="搜索校区名称、地址..."
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filters.is_active" placeholder="状态" @change="fetchCampuses">
            <el-option label="全部" value="" />
            <el-option label="启用" value="true" />
            <el-option label="禁用" value="false" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filters.campus_type" placeholder="类型" @change="fetchCampuses">
            <el-option label="全部" value="" />
            <el-option label="中心校区" value="center" />
            <el-option label="分校区" value="branch" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button @click="resetFilters">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 校区列表 -->
    <div class="campus-list custom-card">
      <el-table
        :data="campuses"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="name" label="校区名称" min-width="120">
          <template #default="{ row }">
            <div class="campus-name">
              <el-tag v-if="row.is_center_campus" type="warning" size="small">中心</el-tag>
              {{ row.name }}
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="code" label="校区代码" width="100" />
        
        <el-table-column prop="address" label="地址" min-width="200" show-overflow-tooltip />
        
        <el-table-column prop="contact_person" label="联系人" width="100" />
        
        <el-table-column prop="phone" label="联系电话" width="120" />
        
        <el-table-column label="管理员" width="120">
          <template #default="{ row }">
            <span v-if="row.manager">{{ row.manager.real_name }}</span>
            <el-tag v-else type="info" size="small">未指定</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewCampus(row)">
              查看
            </el-button>
            <el-button type="warning" size="small" @click="editCampus(row)" v-if="canEdit(row)">
              编辑
            </el-button>
            <el-button type="success" size="small" @click="assignManager(row)" v-if="userStore.user?.user_type === 'super_admin'">
              指定管理员
            </el-button>
            <el-button type="danger" size="small" @click="deleteCampus(row)" v-if="canDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 创建/编辑校区对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingCampus ? '编辑校区' : '新建校区'"
      width="600px"
      @close="resetForm"
    >
      <el-form
        ref="campusFormRef"
        :model="campusForm"
        :rules="campusRules"
        label-width="100px"
      >
        <el-form-item label="校区名称" prop="name">
          <el-input v-model="campusForm.name" placeholder="请输入校区名称" />
        </el-form-item>
        
        <el-form-item label="校区代码" prop="code">
          <el-input v-model="campusForm.code" placeholder="请输入校区代码" />
        </el-form-item>
        
        <el-form-item label="校区类型" prop="campus_type">
          <el-radio-group v-model="campusForm.campus_type">
            <el-radio label="center">中心校区</el-radio>
            <el-radio label="branch">分校区</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <!-- 分校区需要选择上级校区 -->
        <el-form-item 
          v-if="campusForm.campus_type === 'branch'" 
          label="上级校区" 
          prop="parent_campus"
        >
          <el-select 
            v-model="campusForm.parent_campus" 
            placeholder="请选择上级校区" 
            style="width: 100%"
          >
            <el-option
              v-for="campus in centerCampuses"
              :key="campus.id"
              :label="campus.name"
              :value="campus.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="地址" prop="address">
          <el-input v-model="campusForm.address" type="textarea" :rows="2" placeholder="请输入校区地址" />
        </el-form-item>
        
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="campusForm.contact_person" placeholder="请输入联系人姓名" />
        </el-form-item>
        
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="campusForm.phone" placeholder="请输入联系电话" />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="campusForm.email" placeholder="请输入邮箱地址" />
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input v-model="campusForm.description" type="textarea" :rows="3" placeholder="请输入校区描述" />
        </el-form-item>
        
        <el-form-item label="状态">
          <el-switch v-model="campusForm.is_active" active-text="启用" inactive-text="禁用" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="closeCreateDialog">取消</el-button>
        <el-button type="primary" @click="saveCampus" :loading="saving">
          {{ editingCampus ? '更新' : '创建' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 指定管理员对话框 -->
    <el-dialog
      v-model="showManagerDialog"
      title="指定校区管理员"
      width="500px"
    >
      <div v-if="selectedCampus">
        <p><strong>校区：</strong>{{ selectedCampus.name }}</p>
        <p><strong>当前管理员：</strong>{{ selectedCampus.manager?.real_name || '未指定' }}</p>
        
        <el-form label-width="100px">
          <el-form-item label="选择管理员">
            <el-select v-model="selectedManagerId" placeholder="请选择管理员" style="width: 100%">
              <el-option
                v-for="manager in availableManagers"
                :key="manager.id"
                :label="`${manager.real_name} (${manager.username})`"
                :value="manager.id"
              />
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      
      <template #footer>
        <el-button @click="showManagerDialog = false">取消</el-button>
        <el-button type="primary" @click="saveManager" :loading="saving">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 校区详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="校区详情"
      width="700px"
    >
      <div v-if="selectedCampus" class="campus-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="校区名称">{{ selectedCampus.name }}</el-descriptions-item>
          <el-descriptions-item label="校区代码">{{ selectedCampus.code }}</el-descriptions-item>
          <el-descriptions-item label="校区类型">
            <el-tag :type="selectedCampus.is_center_campus ? 'warning' : 'info'">
              {{ selectedCampus.is_center_campus ? '中心校区' : '分校区' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="selectedCampus.is_active ? 'success' : 'danger'">
              {{ selectedCampus.is_active ? '启用' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="地址" :span="2">{{ selectedCampus.address }}</el-descriptions-item>
          <el-descriptions-item label="联系人">{{ selectedCampus.contact_person }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ selectedCampus.phone }}</el-descriptions-item>
          <el-descriptions-item label="邮箱" :span="2">{{ selectedCampus.email }}</el-descriptions-item>
          <el-descriptions-item label="管理员" :span="2">
            {{ selectedCampus.manager?.real_name || '未指定' }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">{{ selectedCampus.description || '无' }}</el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">{{ formatDate(selectedCampus.created_at) }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import {
  School,
  Plus,
  Search,
  Refresh,
  Edit,
  Delete,
  View
} from '@element-plus/icons-vue'
import axios from '@/utils/axios'

const userStore = useUserStore()

// 响应式数据
const campuses = ref([])
const centerCampuses = ref([]) // 中心校区列表
const availableManagers = ref([])
const loading = ref(false)
const saving = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 对话框状态
const showCreateDialog = ref(false)
const showManagerDialog = ref(false)
const showDetailDialog = ref(false)

// 编辑状态
const editingCampus = ref(null)
const selectedCampus = ref(null)
const selectedManagerId = ref(null)

// 表单引用
const campusFormRef = ref()

// 筛选器
const filters = reactive({
  search: '',
  is_active: '',
  campus_type: ''
})

// 表单数据
const campusForm = reactive({
  name: '',
  code: '',
  campus_type: 'branch',
  address: '',
  contact_person: '',
  phone: '',
  email: '',
  description: '',
  is_active: true,
  parent_campus: null
})

// 表单验证规则
const campusRules = {
  name: [
    { required: true, message: '请输入校区名称', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入校区代码', trigger: 'blur' }
  ],
  parent_campus: [
    { 
      validator: (rule, value, callback) => {
        if (campusForm.campus_type === 'branch' && !value) {
          callback(new Error('分校区必须选择上级校区'))
        } else {
          callback()
        }
      }, 
      trigger: 'change' 
    }
  ],
  address: [
    { required: true, message: '请输入校区地址', trigger: 'blur' }
  ],
  contact_person: [
    { required: true, message: '请输入联系人', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 获取校区列表
const fetchCampuses = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: filters.search || undefined,
      is_active: filters.is_active || undefined,
      campus_type: filters.campus_type || undefined
    }
    
    const response = await axios.get('/api/campus/api/list/', { params })
    if (response.data.success) {
      campuses.value = response.data.data
      total.value = response.data.count || response.data.data.length
      
      // 同时获取中心校区列表
      centerCampuses.value = campuses.value.filter(campus => campus.campus_type === 'center')
    }
  } catch (error) {
    ElMessage.error('获取校区列表失败')
    console.error('获取校区列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取可用管理员列表
const fetchAvailableManagers = async () => {
  try {
    const response = await axios.get('/api/campus/api/available-managers/')
    if (response.data.success) {
      availableManagers.value = response.data.data
    }
  } catch (error) {
    ElMessage.error('获取管理员列表失败')
    console.error('获取管理员列表失败:', error)
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchCampuses()
}

// 重置筛选器
const resetFilters = () => {
  filters.search = ''
  filters.is_active = ''
  filters.campus_type = ''
  currentPage.value = 1
  fetchCampuses()
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchCampuses()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchCampuses()
}

// 权限检查
const canEdit = (campus) => {
  return userStore.user?.user_type === 'super_admin' || 
         (userStore.user?.user_type === 'campus_admin' && campus.manager?.id === userStore.user?.id)
}

const canDelete = (campus) => {
  return userStore.user?.user_type === 'super_admin'
}

// 查看校区详情
const viewCampus = (campus) => {
  selectedCampus.value = campus
  showDetailDialog.value = true
}

// 编辑校区
const editCampus = (campus) => {
  editingCampus.value = campus
  Object.assign(campusForm, campus)
  showCreateDialog.value = true
}

// 指定管理员
const assignManager = async (campus) => {
  selectedCampus.value = campus
  selectedManagerId.value = campus.manager?.id || null
  await fetchAvailableManagers()
  showManagerDialog.value = true
}

// 删除校区
const deleteCampus = async (campus) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除校区 "${campus.name}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await axios.delete(`/api/campus/api/${campus.id}/delete/`)
    if (response.data.success) {
      ElMessage.success('校区删除成功')
      fetchCampuses()
    } else {
      ElMessage.error(response.data.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除校区失败')
      console.error('删除校区失败:', error)
    }
  }
}

// 保存校区
const saveCampus = async () => {
  try {
    await campusFormRef.value.validate()
    
    saving.value = true
    let response
    
    if (editingCampus.value) {
      response = await axios.put(`/api/campus/api/${editingCampus.value.id}/update/`, campusForm)
    } else {
      response = await axios.post('/api/campus/api/create/', campusForm)
    }
    
    if (response.data.success) {
      ElMessage.success(editingCampus.value ? '校区更新成功' : '校区创建成功')
        showCreateDialog.value = false
        resetForm()
        await fetchCampuses()
    } else {
      ElMessage.error(response.data.message || '保存失败')
    }
  } catch (error) {
    ElMessage.error('保存校区失败')
    console.error('保存校区失败:', error)
  } finally {
    saving.value = false
  }
}

// 保存管理员指定
const saveManager = async () => {
  try {
    if (!selectedManagerId.value) {
      ElMessage.warning('请选择管理员')
      return
    }
    
    saving.value = true
    const response = await axios.post(`/api/campus/api/${selectedCampus.value.id}/assign-manager/`, {
      manager_id: selectedManagerId.value
    })
    
    if (response.data.success) {
      ElMessage.success('管理员指定成功')
      showManagerDialog.value = false
      fetchCampuses()
    } else {
      ElMessage.error(response.data.message || '指定失败')
    }
  } catch (error) {
    ElMessage.error('指定管理员失败')
    console.error('指定管理员失败:', error)
  } finally {
    saving.value = false
  }
}

// 关闭创建对话框
const closeCreateDialog = () => {
  showCreateDialog.value = false
  resetForm()
}

// 重置表单
const resetForm = () => {
  editingCampus.value = null
  Object.assign(campusForm, {
    name: '',
    code: '',
    campus_type: 'branch',
    address: '',
    contact_person: '',
    phone: '',
    email: '',
    description: '',
    is_active: true,
    parent_campus: null
  })
  // 清除表单验证状态
  if (campusFormRef.value) {
    campusFormRef.value.clearValidate()
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 组件挂载时获取数据
onMounted(() => {
  fetchCampuses()
})
</script>

<style scoped>
.campus-management {
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
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

.header-actions {
  display: flex;
  gap: 12px;
}

.filters {
  padding: 20px;
  margin-bottom: 24px;
}

.campus-list {
  padding: 20px;
}

.campus-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.campus-detail {
  padding: 16px 0;
}

.custom-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>