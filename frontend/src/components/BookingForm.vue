<template>
  <div class="booking-form">
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
      <!-- 师生关系选择 -->
      <el-form-item label="师生关系" prop="relation_id">
        <el-select 
          v-model="form.relation_id" 
          placeholder="选择师生关系" 
          style="width: 100%"
          @change="handleRelationChange"
        >
          <el-option 
            v-for="relation in relations" 
            :key="relation.id" 
            :label="getRelationLabel(relation)" 
            :value="relation.id"
          />
        </el-select>
        <div class="form-tip">只显示已通过审核的师生关系</div>
      </el-form-item>

      <!-- 校区选择 -->
      <el-form-item label="校区" prop="campus_id">
        <el-select 
          v-model="form.campus_id" 
          placeholder="选择校区" 
          style="width: 100%"
          @change="handleCampusChange"
        >
          <el-option 
            v-for="campus in campuses" 
            :key="campus.id" 
            :label="campus.name" 
            :value="campus.id"
          />
        </el-select>
      </el-form-item>

      <!-- 预约时间 -->
      <el-form-item label="开始时间" prop="start_time">
        <el-date-picker
          v-model="form.start_time"
          type="datetime"
          placeholder="选择开始时间"
          format="YYYY-MM-DD HH:mm"
          value-format="YYYY-MM-DD HH:mm:ss"
          style="width: 100%"
          :disabled-date="disabledDate"
          :disabled-hours="disabledHours"
          :disabled-minutes="disabledMinutes"
          @change="handleStartTimeChange"
        />
      </el-form-item>

      <el-form-item label="结束时间" prop="end_time">
        <el-date-picker
          v-model="form.end_time"
          type="datetime"
          placeholder="选择结束时间"
          format="YYYY-MM-DD HH:mm"
          value-format="YYYY-MM-DD HH:mm:ss"
          style="width: 100%"
          :disabled-date="disabledDate"
          :disabled-hours="disabledHours"
          :disabled-minutes="disabledMinutes"
          @change="handleEndTimeChange"
        />
      </el-form-item>

      <!-- 时长显示 -->
      <el-form-item label="预约时长">
        <el-input :value="durationText" readonly />
      </el-form-item>

      <!-- 球台选择 -->
      <el-form-item label="球台" prop="table_id">
        <el-select 
          v-model="form.table_id" 
          placeholder="选择球台" 
          style="width: 100%"
          :loading="tablesLoading"
          :disabled="!availableTables.length"
        >
          <el-option 
            v-for="table in availableTables" 
            :key="table.id" 
            :label="`${table.number}号台 - ${table.name || '标准台'}`" 
            :value="table.id"
          />
        </el-select>
        <div class="form-tip" v-if="!availableTables.length && form.start_time && form.end_time">
          该时间段暂无可用球台
        </div>
      </el-form-item>

      <!-- 费用 -->
      <el-form-item label="预约费用" prop="total_fee">
        <el-input-number 
          v-model="form.total_fee" 
          :min="0" 
          :precision="2" 
          style="width: 100%"
        />
        <div class="form-tip">单位：元</div>
      </el-form-item>

      <!-- 备注 -->
      <el-form-item label="备注">
        <el-input 
          v-model="form.notes" 
          type="textarea" 
          :rows="3" 
          placeholder="请输入备注信息（可选）"
        />
      </el-form-item>
    </el-form>

    <div class="form-actions">
      <el-button @click="$emit('cancel')">取消</el-button>
      <el-button type="primary" @click="submitForm" :loading="submitting">
        创建预约
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const emit = defineEmits(['success', 'cancel'])

// 响应式数据
const formRef = ref()
const submitting = ref(false)
const tablesLoading = ref(false)

const relations = ref([])
const campuses = ref([])
const availableTables = ref([])

// 表单数据
const form = reactive({
  relation_id: '',
  campus_id: '',
  table_id: '',
  start_time: '',
  end_time: '',
  duration_hours: 0,
  total_fee: 0,
  notes: ''
})

// 表单验证规则
const rules = {
  relation_id: [{ required: true, message: '请选择师生关系', trigger: 'change' }],
  campus_id: [{ required: true, message: '请选择校区', trigger: 'change' }],
  start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
  end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }],
  table_id: [{ required: true, message: '请选择球台', trigger: 'change' }],
  total_fee: [{ required: true, message: '请输入预约费用', trigger: 'blur' }]
}

// 计算属性
const durationText = computed(() => {
  if (!form.start_time || !form.end_time) return '请选择时间'
  
  const start = new Date(form.start_time)
  const end = new Date(form.end_time)
  const duration = (end - start) / (1000 * 60 * 60)
  
  if (duration <= 0) return '结束时间必须晚于开始时间'
  if (duration < 0.5) return '预约时长不能少于30分钟'
  if (duration > 8) return '预约时长不能超过8小时'
  
  return `${duration.toFixed(1)}小时`
})

// 方法
const loadRelations = async () => {
  try {
    const response = await fetch('/api/reservations/api/relations/', {
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })
    
    if (response.ok) {
      const data = await response.json()
      relations.value = data.results?.filter(r => r.status === 'approved') || []
    }
  } catch (error) {
    console.error('加载师生关系失败:', error)
  }
}

const loadCampuses = async () => {
  try {
    const response = await fetch('/api/campus/api/list/', {
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })
    
    if (response.ok) {
      const data = await response.json()
      campuses.value = data.results || []
    }
  } catch (error) {
    console.error('加载校区失败:', error)
  }
}

const loadAvailableTables = async () => {
  if (!form.start_time || !form.end_time || !form.campus_id) {
    availableTables.value = []
    return
  }
  
  tablesLoading.value = true
  try {
    const params = new URLSearchParams({
      start_time: form.start_time,
      end_time: form.end_time,
      campus_id: form.campus_id
    })
    
    const response = await fetch(`/api/reservations/api/tables/available/?${params}`, {
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })
    
    if (response.ok) {
      const data = await response.json()
      availableTables.value = data
      
      // 如果当前选择的球台不在可用列表中，清空选择
      if (form.table_id && !data.find(t => t.id === form.table_id)) {
        form.table_id = ''
      }
    } else {
      availableTables.value = []
    }
  } catch (error) {
    console.error('加载可用球台失败:', error)
    availableTables.value = []
  } finally {
    tablesLoading.value = false
  }
}

const handleRelationChange = () => {
  // 师生关系改变时的处理逻辑
}

const handleCampusChange = () => {
  form.table_id = ''
  loadAvailableTables()
}

const handleStartTimeChange = () => {
  // 如果结束时间早于开始时间，清空结束时间
  if (form.end_time && new Date(form.end_time) <= new Date(form.start_time)) {
    form.end_time = ''
  }
  updateDuration()
  loadAvailableTables()
}

const handleEndTimeChange = () => {
  updateDuration()
  loadAvailableTables()
}

const updateDuration = () => {
  if (form.start_time && form.end_time) {
    const start = new Date(form.start_time)
    const end = new Date(form.end_time)
    const duration = (end - start) / (1000 * 60 * 60)
    form.duration_hours = Math.round(duration * 10) / 10
    
    // 根据时长自动计算费用（示例：每小时100元）
    if (duration > 0) {
      form.total_fee = Math.round(duration * 100 * 100) / 100
    }
  }
}

const getRelationLabel = (relation) => {
  if (userStore.user.user_type === 'coach') {
    return `学员: ${relation.student.real_name}`
  } else {
    return `教练: ${relation.coach.real_name}`
  }
}

// 时间选择限制
const disabledDate = (time) => {
  // 不能选择过去的日期
  return time.getTime() < Date.now() - 24 * 60 * 60 * 1000
}

const disabledHours = () => {
  const now = new Date()
  const selectedDate = new Date(form.start_time || form.end_time)
  
  // 如果是今天，禁用过去的小时
  if (selectedDate.toDateString() === now.toDateString()) {
    const hours = []
    for (let i = 0; i < now.getHours(); i++) {
      hours.push(i)
    }
    return hours
  }
  
  return []
}

const disabledMinutes = (hour) => {
  const now = new Date()
  const selectedDate = new Date(form.start_time || form.end_time)
  
  // 如果是今天的当前小时，禁用过去的分钟
  if (selectedDate.toDateString() === now.toDateString() && hour === now.getHours()) {
    const minutes = []
    for (let i = 0; i <= now.getMinutes(); i++) {
      minutes.push(i)
    }
    return minutes
  }
  
  return []
}

const submitForm = async () => {
  try {
    await formRef.value.validate()
    
    submitting.value = true
    
    const response = await fetch('/api/reservations/api/bookings/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(form)
    })
    
    if (response.ok) {
      ElMessage.success('预约创建成功')
      emit('success')
    } else {
      const error = await response.json()
      ElMessage.error(error.error || '创建预约失败')
    }
  } catch (error) {
    if (error.message) {
      console.error('创建预约错误:', error)
      ElMessage.error('创建预约失败')
    }
  } finally {
    submitting.value = false
  }
}

// 监听时间变化
watch([() => form.start_time, () => form.end_time, () => form.campus_id], () => {
  loadAvailableTables()
})

// 生命周期
onMounted(() => {
  loadRelations()
  loadCampuses()
})
</script>

<style scoped>
.booking-form {
  padding: 20px 0;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #ebeef5;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-input-number {
  width: 100%;
}
</style>