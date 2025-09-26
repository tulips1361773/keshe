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
        <div class="form-tip">请选择30天内的时间，不能早于当前时间</div>
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
          :disabled="!form.start_time"
          @change="handleEndTimeChange"
        />
        <div class="form-tip">预约时长：30分钟 - 8小时</div>
      </el-form-item>

      <!-- 时长显示 -->
      <el-form-item label="预约时长">
        <el-input 
          :value="durationText" 
          readonly 
          :class="{ 'duration-error': durationText.includes('必须') || durationText.includes('不能') }"
        />
        <div class="form-tip" v-if="form.start_time && form.end_time && durationText.includes('小时')">
          建议费用：¥{{ Math.round(parseFloat(durationText) * 100) }}
        </div>
      </el-form-item>

      <!-- 球台选择 -->
      <el-form-item label="球台" prop="table_id">
        <el-select 
          v-model="form.table_id" 
          placeholder="选择球台" 
          style="width: 100%"
          :loading="tablesLoading"
          :disabled="!availableTables.length || !form.start_time || !form.end_time || !form.campus_id"
          filterable
        >
          <el-option 
            v-for="table in availableTables" 
            :key="table.id" 
            :label="`${table.number}号台 - ${table.name || '标准台'}`" 
            :value="table.id"
          />
        </el-select>
        <div class="form-tip" v-if="!form.start_time || !form.end_time || !form.campus_id">
          请先选择校区和预约时间
        </div>
        <div class="form-tip" v-else-if="tablesLoading">
          正在加载可用球台...
        </div>
        <div class="form-tip" v-else-if="!availableTables.length">
          该时间段暂无可用球台，请调整时间
        </div>
        <div class="form-tip success" v-else>
          找到 {{ availableTables.length }} 个可用球台
        </div>
      </el-form-item>

      <!-- 费用 -->
      <el-form-item label="预约费用" prop="total_fee">
        <el-input-number 
          v-model="form.total_fee" 
          :min="0" 
          :precision="2" 
          style="width: 100%"
          readonly
        />
        <div class="form-tip">费用根据教练等级和预约时长自动计算</div>
        <div class="form-tip" v-if="form.relation_id && relations.length">
          <span v-for="relation in relations" :key="relation.id">
            <span v-if="relation.id === form.relation_id">
              教练：{{ relation.coach.real_name }} | 
              等级：{{ getCoachLevelText(relation.coach.coach_level) }} | 
              时薪：¥{{ relation.coach.hourly_rate }}/小时
            </span>
          </span>
        </div>
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
      <el-button 
        type="primary" 
        @click="submitForm" 
        :loading="submitting"
        :disabled="!isFormValid || submitting"
      >
        {{ submitting ? '创建中...' : '创建预约' }}
      </el-button>
    </div>
    
    <!-- 表单验证状态提示 -->
    <div class="validation-summary" v-if="!isFormValid">
      <el-alert
        title="请完善以下信息后提交"
        type="warning"
        :closable="false"
        show-icon
      >
        <ul class="validation-list">
          <li v-if="!form.relation_id">请选择师生关系</li>
          <li v-if="!form.campus_id">请选择校区</li>
          <li v-if="!form.start_time">请选择开始时间</li>
          <li v-if="!form.end_time">请选择结束时间</li>
          <li v-if="form.start_time && form.end_time && !durationText.includes('小时')">请检查预约时间设置</li>
          <li v-if="!form.table_id">请选择球台</li>
          <li v-if="!form.total_fee || form.total_fee <= 0">请输入有效的预约费用</li>
        </ul>
      </el-alert>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { handleError, handleApiError, logger, performance } from '@/utils/errorHandler'
import axios from '@/utils/axios'

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

// 验证函数
const validateStartTime = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请选择开始时间'))
    return
  }
  
  const now = new Date()
  const startTime = new Date(value)
  
  // 不能选择过去的时间
  if (startTime <= now) {
    callback(new Error('开始时间不能早于当前时间'))
    return
  }
  
  // 不能选择太远的未来时间（30天内）
  const maxDate = new Date()
  maxDate.setDate(maxDate.getDate() + 30)
  if (startTime > maxDate) {
    callback(new Error('开始时间不能超过30天后'))
    return
  }
  
  callback()
}

const validateEndTime = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请选择结束时间'))
    return
  }
  
  if (!form.start_time) {
    callback(new Error('请先选择开始时间'))
    return
  }
  
  const start = new Date(form.start_time)
  const end = new Date(value)
  const duration = (end - start) / (1000 * 60 * 60)
  
  if (duration <= 0) {
    callback(new Error('结束时间必须晚于开始时间'))
    return
  }
  
  if (duration < 0.5) {
    callback(new Error('预约时长不能少于30分钟'))
    return
  }
  
  if (duration > 8) {
    callback(new Error('预约时长不能超过8小时'))
    return
  }
  
  callback()
}

const validateTotalFee = (rule, value, callback) => {
  if (!value || value <= 0) {
    callback(new Error('预约费用必须大于0'))
    return
  }
  callback()
}

// 表单验证规则
const rules = {
  relation_id: [{ required: true, message: '请选择师生关系', trigger: 'change' }],
  campus_id: [{ required: true, message: '请选择校区', trigger: 'change' }],
  start_time: [
    { required: true, message: '请选择开始时间', trigger: 'change' },
    { validator: validateStartTime, trigger: 'change' }
  ],
  end_time: [
    { required: true, message: '请选择结束时间', trigger: 'change' },
    { validator: validateEndTime, trigger: 'change' }
  ],
  table_id: [{ required: true, message: '请选择球台', trigger: 'change' }],
  total_fee: [
    { required: true, message: '请输入预约费用', trigger: 'blur' },
    { validator: validateTotalFee, trigger: 'blur' }
  ]
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

const isFormValid = computed(() => {
  return form.relation_id && 
         form.campus_id && 
         form.start_time && 
         form.end_time && 
         form.table_id && 
         form.total_fee > 0 &&
         durationText.value.includes('小时')
})

// 方法
const loadRelations = async () => {
  try {
    performance.start('loadRelations')
    logger.debug('开始加载师生关系')
    
    const response = await axios.get('/api/reservations/relations/')
    
    relations.value = response.data.results?.filter(r => r.status === 'approved') || []
    logger.info(`加载师生关系成功，共${relations.value.length}条记录`)
  } catch (error) {
    await handleError(error, '加载师生关系')
  } finally {
    performance.end('loadRelations')
  }
}

const loadCampuses = async () => {
  try {
    performance.start('loadCampuses')
    logger.debug('开始加载校区列表')
    
    const response = await axios.get('/api/campus/api/list/')
    
    campuses.value = response.data.data || []
    logger.info(`加载校区成功，共${campuses.value.length}个校区`)
  } catch (error) {
    await handleError(error, '加载校区列表')
  } finally {
    performance.end('loadCampuses')
  }
}

const loadAvailableTables = async () => {
  // 检查必要参数
  if (!form.start_time || !form.end_time || !form.campus_id) {
    availableTables.value = []
    return
  }
  
  // 验证时间有效性
  const startTime = new Date(form.start_time)
  const endTime = new Date(form.end_time)
  const duration = (endTime - startTime) / (1000 * 60 * 60)
  
  // 如果时间无效，不发送请求
  if (duration <= 0) {
    logger.warn('时间无效，结束时间必须晚于开始时间', {
      start_time: form.start_time,
      end_time: form.end_time,
      duration
    })
    availableTables.value = []
    return
  }
  
  if (duration < 0.5 || duration > 8) {
    logger.warn('时间长度无效，必须在30分钟到8小时之间', {
      duration
    })
    availableTables.value = []
    return
  }
  
  tablesLoading.value = true
  try {
    performance.start('loadAvailableTables')
    logger.debug('开始加载可用球台', {
      start_time: form.start_time,
      end_time: form.end_time,
      campus_id: form.campus_id,
      duration: `${duration.toFixed(1)}小时`
    })
    
    const params = {
      start_time: form.start_time,
      end_time: form.end_time,
      campus_id: form.campus_id
    }
    
    const response = await axios.get('/api/reservations/tables/available/', { params })
    
    availableTables.value = response.data
    logger.info(`加载可用球台成功，共${response.data.length}个可用球台`)
    
    // 如果当前选择的球台不在可用列表中，清空选择
    if (form.table_id && !response.data.find(t => t.id === form.table_id)) {
      form.table_id = ''
      logger.warn('当前选择的球台不可用，已清空选择')
    }
  } catch (error) {
    availableTables.value = []
    await handleError(error, '加载可用球台')
  } finally {
    tablesLoading.value = false
    performance.end('loadAvailableTables')
  }
}

const handleRelationChange = () => {
  // 师生关系改变时，重新计算费用
  updateDuration()
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
    
    // 根据教练等级和时长自动计算费用
    if (duration > 0 && form.relation_id) {
      const selectedRelation = relations.value.find(r => r.id === form.relation_id)
      if (selectedRelation && selectedRelation.coach && selectedRelation.coach.hourly_rate) {
        // 使用教练的实际时薪计算费用
        const hourlyRate = parseFloat(selectedRelation.coach.hourly_rate)
        form.total_fee = Math.round(duration * hourlyRate * 100) / 100
      } else {
        // 如果没有获取到教练时薪信息，使用默认费用计算
        form.total_fee = Math.round(duration * 100 * 100) / 100
      }
    }
  }
}

const getRelationLabel = (relation) => {
  if (userStore.user?.user_type === 'coach') {
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
    performance.start('submitBooking')
    logger.info('开始创建预约', form)
    
    // 表单验证
    await formRef.value.validate()
    
    // 额外的业务逻辑验证
    if (!isFormValid.value) {
      ElMessage.warning('请完善所有必填信息')
      return
    }
    
    // 时间冲突检查
    const now = new Date()
    const startTime = new Date(form.start_time)
    if (startTime <= now) {
      ElMessage.error('开始时间不能早于当前时间')
      return
    }
    
    submitting.value = true
    
    // 准备提交数据
    const submitData = {
      ...form,
      duration_hours: parseFloat(((new Date(form.end_time) - new Date(form.start_time)) / (1000 * 60 * 60)).toFixed(1))
    }
    
    logger.debug('提交预约数据', submitData)
    
    const response = await axios.post('/api/reservations/bookings/', submitData)
    
    logger.info('预约创建成功', response.data)
    
    ElMessage.success({
      message: '预约创建成功！',
      duration: 3000,
      showClose: true
    })
    
    // 重置表单
    formRef.value.resetFields()
    Object.assign(form, {
      relation_id: '',
      campus_id: '',
      table_id: '',
      start_time: '',
      end_time: '',
      duration_hours: 0,
      total_fee: 0,
      notes: ''
    })
    
    // 清空可用球台列表
    availableTables.value = []
    
    emit('success', response.data)
  } catch (error) {
    await handleError(error, '创建预约')
  } finally {
    submitting.value = false
    performance.end('submitBooking')
  }
}

// 获取教练等级文本
const getCoachLevelText = (level) => {
  switch (level) {
    case 'junior': return '初级教练员'
    case 'intermediate': return '中级教练员'
    case 'senior': return '高级教练员'
    default: return '未知等级'
  }
}

// 监听时间变化，但只在时间有效时才加载球台
watch([() => form.start_time, () => form.end_time, () => form.campus_id], () => {
  // 延迟执行，避免频繁调用
  setTimeout(() => {
    loadAvailableTables()
  }, 300)
}, { deep: true })

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
  line-height: 1.4;
}

.form-tip.success {
  color: #67c23a;
  font-weight: 500;
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

.duration-error :deep(.el-input__inner) {
  border-color: #f56c6c;
  color: #f56c6c;
}

.validation-summary {
  margin-top: 16px;
}

.validation-list {
  margin: 8px 0 0 0;
  padding-left: 20px;
}

.validation-list li {
  margin-bottom: 4px;
  font-size: 13px;
  color: #e6a23c;
}

/* 表单项动画效果 */
.el-form-item {
  transition: all 0.3s ease;
}

.el-form-item:hover {
  transform: translateY(-1px);
}

/* 禁用状态样式 */
.el-select.is-disabled,
.el-date-picker.is-disabled {
  opacity: 0.6;
}

/* 加载状态样式 */
.el-select .el-input.is-focus .el-input__inner {
  border-color: #409eff;
}

/* 成功状态提示 */
.form-tip.success::before {
  content: '✓ ';
  color: #67c23a;
  font-weight: bold;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .booking-form {
    padding: 10px 0;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .el-button {
    width: 100%;
  }
}
</style>