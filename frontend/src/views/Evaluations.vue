<template>
  <div class="evaluations-container">
    <div class="header">
      <h1>课程评价</h1>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><EditPen /></el-icon>
        添加评价
      </el-button>
      <el-button type="warning" @click="testCommentArray">测试Comment数组问题</el-button>
    </div>

    <!-- 筛选条件 -->
    <el-card class="filter-card">
      <el-form :model="filters" inline>
        <el-form-item label="课程">
          <el-select v-model="filters.course" placeholder="选择课程" clearable filterable>
            <el-option 
              v-for="course in courses" 
              :key="course.id" 
              :label="course.name" 
              :value="course.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="教练">
          <el-select v-model="filters.coach" placeholder="选择教练" clearable filterable>
            <el-option 
              v-for="coach in coaches" 
              :key="coach.id" 
              :label="coach.name" 
              :value="coach.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="评分">
          <el-select v-model="filters.rating" placeholder="选择评分" clearable>
            <el-option label="5星" :value="5" />
            <el-option label="4星" :value="4" />
            <el-option label="3星" :value="3" />
            <el-option label="2星" :value="2" />
            <el-option label="1星" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadEvaluations">查询</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 评价列表 -->
    <el-card class="list-card">
      <el-table :data="evaluations" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column label="课程" width="150">
          <template #default="{ row }">
            <div class="course-info">
              <div class="course-name">{{ row.course_name }}</div>
              <div class="course-time">{{ formatDateTime(row.course_time) }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="教练" width="100">
          <template #default="{ row }">
            {{ row.coach_name }}
          </template>
        </el-table-column>
        <el-table-column label="评分" width="120">
          <template #default="{ row }">
            <el-rate 
              v-model="row.rating" 
              disabled 
              show-score 
              text-color="#ff9900"
              score-template="{value}分"
            />
          </template>
        </el-table-column>
        <el-table-column label="评价内容" min-width="200">
          <template #default="{ row }">
            <div class="comment-content">
              {{ row.comment || '无评价内容' }}
            </div>
          </template>
        </el-table-column>
        <el-table-column label="评价时间" width="160">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button size="small" @click="viewDetail(row)">详情</el-button>
            <el-button 
              v-if="row.user === userStore.user?.id" 
              size="small" 
              type="primary" 
              @click="editEvaluation(row)"
            >
              编辑
            </el-button>
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
          @size-change="loadEvaluations"
          @current-change="loadEvaluations"
        />
      </div>
    </el-card>

    <!-- 创建/编辑评价对话框 -->
    <el-dialog 
      v-model="showCreateDialog" 
      :title="isEditing ? '编辑评价' : '添加评价'" 
      width="600px"
    >
      <el-form :model="evaluationForm" :rules="evaluationRules" ref="evaluationFormRef" label-width="100px">
        <el-form-item label="选择课程" prop="course">
          <el-select 
            v-model="evaluationForm.course" 
            placeholder="请选择要评价的课程" 
            style="width: 100%"
            filterable
            @change="handleCourseChange"
          >
            <el-option 
              v-for="course in availableCourses" 
              :key="course.id" 
              :label="`${course.name} - ${course.coach_name} (${formatDateTime(course.start_time)})`" 
              :value="course.id"
            />
          </el-select>
          <div class="form-tip">只能评价已完成的课程</div>
        </el-form-item>
        
        <el-form-item label="课程评分" prop="rating">
          <el-rate 
            v-model="evaluationForm.rating" 
            show-text 
            :texts="['极差', '失望', '一般', '满意', '惊喜']"
          />
        </el-form-item>
        
        <el-form-item label="评价内容" prop="comment">
          <el-input 
            v-model="evaluationForm.comment" 
            type="textarea" 
            :rows="4" 
            placeholder="请详细描述您对本次课程的评价和建议"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="教学质量">
          <el-rate v-model="evaluationForm.teaching_quality" show-text />
        </el-form-item>
        
        <el-form-item label="服务态度">
          <el-rate v-model="evaluationForm.service_attitude" show-text />
        </el-form-item>
        
        <el-form-item label="场地环境">
          <el-rate v-model="evaluationForm.venue_environment" show-text />
        </el-form-item>
        
        <el-form-item label="推荐指数">
          <el-rate v-model="evaluationForm.recommendation" show-text />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="submitEvaluation" :loading="submitLoading">
          {{ isEditing ? '更新评价' : '提交评价' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 评价详情对话框 -->
    <el-dialog v-model="showDetailDialog" title="评价详情" width="700px">
      <div v-if="selectedEvaluation" class="evaluation-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="课程名称">
            {{ selectedEvaluation.course_name }}
          </el-descriptions-item>
          <el-descriptions-item label="教练">
            {{ selectedEvaluation.coach_name }}
          </el-descriptions-item>
          <el-descriptions-item label="课程时间">
            {{ formatDateTime(selectedEvaluation.course_time) }}
          </el-descriptions-item>
          <el-descriptions-item label="评价时间">
            {{ formatDateTime(selectedEvaluation.created_at) }}
          </el-descriptions-item>
        </el-descriptions>
        
        <div class="rating-section">
          <h3>评分详情</h3>
          <div class="rating-grid">
            <div class="rating-item">
              <span class="rating-label">总体评分：</span>
              <el-rate v-model="selectedEvaluation.rating" disabled show-score />
            </div>
            <div class="rating-item">
              <span class="rating-label">教学质量：</span>
              <el-rate v-model="selectedEvaluation.teaching_quality" disabled show-score />
            </div>
            <div class="rating-item">
              <span class="rating-label">服务态度：</span>
              <el-rate v-model="selectedEvaluation.service_attitude" disabled show-score />
            </div>
            <div class="rating-item">
              <span class="rating-label">场地环境：</span>
              <el-rate v-model="selectedEvaluation.venue_environment" disabled show-score />
            </div>
            <div class="rating-item">
              <span class="rating-label">推荐指数：</span>
              <el-rate v-model="selectedEvaluation.recommendation" disabled show-score />
            </div>
          </div>
        </div>
        
        <div class="comment-section">
          <h3>评价内容</h3>
          <div class="comment-text">
            {{ selectedEvaluation.comment || '无评价内容' }}
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { EditPen } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import axios from '@/utils/axios'

const userStore = useUserStore()

// 响应式数据
const loading = ref(false)
const evaluations = ref([])
const courses = ref([])
const coaches = ref([])
const availableCourses = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 筛选条件
const filters = reactive({
  course: '',
  coach: '',
  rating: ''
})

// 对话框状态
const showCreateDialog = ref(false)
const showDetailDialog = ref(false)
const selectedEvaluation = ref(null)
const isEditing = ref(false)
const submitLoading = ref(false)

// 评价表单
const evaluationFormRef = ref()
const evaluationForm = reactive({
  course: '',
  rating: 5,
  comment: '',
  teaching_quality: 5,
  service_attitude: 5,
  venue_environment: 5,
  recommendation: 5
})

const evaluationRules = {
  course: [
    { required: true, message: '请选择要评价的课程', trigger: 'change' }
  ],
  rating: [
    { required: true, message: '请给出评分', trigger: 'change' }
  ],
  comment: [
    { required: true, message: '请填写评价内容', trigger: 'blur' },
    { min: 10, message: '评价内容至少10个字符', trigger: 'blur' }
  ]
}

// 方法
const loadEvaluations = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      ...filters
    }
    
    const response = await axios.get('/api/courses/evaluations/', { params })
    evaluations.value = response.data.results || []
    total.value = response.data.count || 0
  } catch (error) {
    console.error('加载评价列表错误:', error)
    ElMessage.error('加载评价列表失败')
  } finally {
    loading.value = false
  }
}

const loadCourses = async () => {
  try {
    const response = await axios.get('/api/courses/list/')
    courses.value = response.data.data || []
  } catch (error) {
    console.error('加载课程列表错误:', error)
  }
}

const loadCoaches = async () => {
  try {
    const response = await axios.get('/api/reservations/coaches/')
    coaches.value = response.data || []
  } catch (error) {
    console.error('加载教练列表错误:', error)
  }
}

const loadAvailableCourses = async () => {
  try {
    const response = await axios.get('/api/courses/list/')
    availableCourses.value = response.data.data || []
  } catch (error) {
    console.error('加载可评价课程错误:', error)
  }
}

const submitEvaluation = async () => {
  if (!evaluationFormRef.value) return
  
  try {
    // 调试信息：验证前检查comment字段类型
    console.log('Before validation - evaluationForm.comment:', evaluationForm.comment, 'Type:', typeof evaluationForm.comment, 'IsArray:', Array.isArray(evaluationForm.comment))
    
    await evaluationFormRef.value.validate()
    
    // 调试信息：验证后检查comment字段类型
    console.log('After validation - evaluationForm.comment:', evaluationForm.comment, 'Type:', typeof evaluationForm.comment, 'IsArray:', Array.isArray(evaluationForm.comment))
    
    submitLoading.value = true
    
    // 确保comment字段是字符串，防止验证错误导致的数组问题
    const submitData = {
      ...evaluationForm,
      comment: Array.isArray(evaluationForm.comment) ? evaluationForm.comment.join('') : evaluationForm.comment
    }
    
    console.log('Processed submitData.comment:', submitData.comment, 'Type:', typeof submitData.comment)
    
    if (isEditing.value) {
      await axios.put(`/api/courses/evaluations/${selectedEvaluation.value.id}/`, submitData)
      ElMessage.success('评价更新成功')
    } else {
      await axios.post('/api/courses/evaluations/', submitData)
      ElMessage.success('评价提交成功')
    }
    
    showCreateDialog.value = false
    resetForm()
    loadEvaluations()
  } catch (error) {
    // 检查是否是表单验证错误
    if (error && typeof error === 'object' && !error.response) {
      console.log('Form validation failed - evaluationForm.comment after validation error:', evaluationForm.comment, 'Type:', typeof evaluationForm.comment, 'IsArray:', Array.isArray(evaluationForm.comment))
      ElMessage.error('请检查表单填写是否完整')
      return
    }
    
    console.error('提交评价错误:', error)
    console.error('Error details:', error.response?.data)
    ElMessage.error(error.response?.data?.message || error.response?.data?.error || '操作失败')
  } finally {
    submitLoading.value = false
  }
}

const editEvaluation = (evaluation) => {
  isEditing.value = true
  selectedEvaluation.value = evaluation
  Object.assign(evaluationForm, {
    course: evaluation.course,
    rating: evaluation.rating,
    comment: evaluation.comment,
    teaching_quality: evaluation.teaching_quality || 5,
    service_attitude: evaluation.service_attitude || 5,
    venue_environment: evaluation.venue_environment || 5,
    recommendation: evaluation.recommendation || 5
  })
  showCreateDialog.value = true
}

const viewDetail = (evaluation) => {
  selectedEvaluation.value = evaluation
  showDetailDialog.value = true
}

const handleCourseChange = () => {
  // 可以在这里添加课程选择后的逻辑
}

const resetFilters = () => {
  Object.assign(filters, {
    course: '',
    coach: '',
    rating: ''
  })
  loadEvaluations()
}

const resetForm = () => {
  Object.assign(evaluationForm, {
    course: '',
    rating: 5,
    comment: '',
    teaching_quality: 5,
    service_attitude: 5,
    venue_environment: 5,
    recommendation: 5
  })
  isEditing.value = false
  selectedEvaluation.value = null
}

const testCommentArray = () => {
  console.log('Testing comment array issue...')
  // 模拟comment变成数组的情况
  evaluationForm.comment = ['这是一个测试评价']
  console.log('Set evaluationForm.comment to array:', evaluationForm.comment)
  ElMessage.info('已将comment设置为数组，请尝试提交评价查看错误')
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

// 生命周期
onMounted(() => {
  loadEvaluations()
  loadCourses()
  loadCoaches()
  loadAvailableCourses()
})
</script>

<style scoped>
.evaluations-container {
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

.course-info {
  line-height: 1.4;
}

.course-name {
  font-weight: bold;
  color: #303133;
}

.course-time {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

.comment-content {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.evaluation-detail {
  padding: 10px 0;
}

.rating-section {
  margin: 20px 0;
}

.rating-section h3 {
  margin-bottom: 15px;
  color: #303133;
}

.rating-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.rating-item {
  display: flex;
  align-items: center;
}

.rating-label {
  width: 80px;
  font-size: 14px;
  color: #606266;
}

.comment-section {
  margin: 20px 0;
}

.comment-section h3 {
  margin-bottom: 10px;
  color: #303133;
}

.comment-text {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  line-height: 1.6;
  color: #606266;
  min-height: 60px;
}

.el-table {
  width: 100%;
}

.el-button + .el-button {
  margin-left: 8px;
}
</style>