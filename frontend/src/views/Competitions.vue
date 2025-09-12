<template>
  <div class="competitions-container">
    <div class="header">
      <h1>比赛管理</h1>
      <button 
        v-if="userStore.user?.user_type === 'coach'" 
        @click="showCreateModal = true" 
        class="btn btn-primary"
      >
        创建比赛
      </button>
    </div>

    <!-- 比赛列表 -->
    <div class="competitions-grid">
      <div 
        v-for="competition in competitions" 
        :key="competition.id" 
        class="competition-card"
        @click="viewCompetition(competition.id)"
      >
        <div class="card-header">
          <h3>{{ competition.name }}</h3>
          <span class="status-badge" :class="competition.status">
            {{ getStatusText(competition.status) }}
          </span>
        </div>
        <div class="card-body">
          <p><strong>类型:</strong> {{ getTypeText(competition.competition_type) }}</p>
          <p><strong>校区:</strong> {{ competition.campus_name }}</p>
          <p><strong>报名截止:</strong> {{ formatDate(competition.registration_deadline) }}</p>
          <p><strong>比赛时间:</strong> {{ formatDate(competition.start_date) }}</p>
          <p><strong>已报名:</strong> {{ competition.registration_count }}/{{ competition.max_participants }}</p>
        </div>
        <div class="card-actions">
          <button 
            v-if="canRegister(competition)" 
            @click.stop="registerCompetition(competition.id)"
            class="btn btn-success btn-sm"
          >
            报名参赛
          </button>
          <button 
            v-if="isRegistered(competition.id)"
            @click.stop="cancelRegistration(competition.id)"
            class="btn btn-warning btn-sm"
          >
            取消报名
          </button>
        </div>
      </div>
    </div>

    <!-- 创建比赛模态框 -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h2>创建比赛</h2>
          <button @click="showCreateModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="createCompetition" class="modal-body">
          <div class="form-group">
            <label>比赛名称</label>
            <input v-model="newCompetition.name" type="text" required class="form-control">
          </div>
          <div class="form-group">
            <label>比赛类型</label>
            <select v-model="newCompetition.competition_type" required class="form-control">
              <option value="single">单打</option>
              <option value="double">双打</option>
              <option value="team">团体赛</option>
            </select>
          </div>
          <div class="form-group">
            <label>校区</label>
            <select v-model="newCompetition.campus" required class="form-control">
              <option v-for="campus in campuses" :key="campus.id" :value="campus.id">
                {{ campus.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>最大参赛人数</label>
            <input v-model.number="newCompetition.max_participants" type="number" min="2" required class="form-control">
          </div>
          <div class="form-group">
            <label>报名截止时间</label>
            <input v-model="newCompetition.registration_deadline" type="datetime-local" required class="form-control">
          </div>
          <div class="form-group">
            <label>比赛开始时间</label>
            <input v-model="newCompetition.start_date" type="datetime-local" required class="form-control">
          </div>
          <div class="form-group">
            <label>比赛描述</label>
            <textarea v-model="newCompetition.description" class="form-control" rows="3"></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showCreateModal = false" class="btn btn-secondary">取消</button>
            <button type="submit" class="btn btn-primary">创建比赛</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from '@/utils/axios'

export default {
  name: 'Competitions',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
    const competitions = ref([])
    const campuses = ref([])
    const showCreateModal = ref(false)
    const userRegistrations = ref([])
    
    const newCompetition = ref({
      name: '',
      competition_type: 'single',
      campus: '',
      max_participants: 16,
      registration_deadline: '',
      start_date: '',
      description: ''
    })

    // 获取比赛列表
    const fetchCompetitions = async () => {
      try {
        const response = await axios.get('/api/competitions/')
        competitions.value = response.data.results || response.data
      } catch (error) {
        console.error('获取比赛列表失败:', error)
      }
    }

    // 获取校区列表
    const fetchCampuses = async () => {
      try {
        const response = await axios.get('/api/campus/api/list/')
        campuses.value = response.data.results || response.data
      } catch (error) {
        console.error('获取校区列表失败:', error)
      }
    }

    // 获取用户报名记录
    const fetchUserRegistrations = async () => {
      if (userStore.user?.user_type === 'student') {
        try {
          const response = await axios.get('/api/competitions/my-registrations/')
          userRegistrations.value = response.data
        } catch (error) {
          console.error('获取报名记录失败:', error)
        }
      }
    }

    // 创建比赛
    const createCompetition = async () => {
      try {
        await axios.post('/api/competitions/', newCompetition.value)
        showCreateModal.value = false
        // 重置表单
        newCompetition.value = {
          name: '',
          competition_type: 'single',
          campus: '',
          max_participants: 16,
          registration_deadline: '',
          start_date: '',
          description: ''
        }
        await fetchCompetitions()
        alert('比赛创建成功！')
      } catch (error) {
        console.error('创建比赛失败:', error)
        alert('创建比赛失败，请重试')
      }
    }

    // 报名参赛
    const registerCompetition = async (competitionId) => {
      try {
        await axios.post(`/api/competitions/${competitionId}/register/`)
        await fetchCompetitions()
        await fetchUserRegistrations()
        alert('报名成功！')
      } catch (error) {
        console.error('报名失败:', error)
        alert(error.response?.data?.error || '报名失败，请重试')
      }
    }

    // 取消报名
    const cancelRegistration = async (competitionId) => {
      try {
        await axios.post(`/api/competitions/${competitionId}/cancel-registration/`)
        await fetchCompetitions()
        await fetchUserRegistrations()
        alert('取消报名成功！')
      } catch (error) {
        console.error('取消报名失败:', error)
        alert(error.response?.data?.error || '取消报名失败，请重试')
      }
    }

    // 查看比赛详情
    const viewCompetition = (competitionId) => {
      router.push(`/competitions/${competitionId}`)
    }

    // 判断是否可以报名
    const canRegister = (competition) => {
      return userStore.user?.user_type === 'student' && 
             competition.status === 'registration' && 
             !isRegistered(competition.id) &&
             competition.registration_count < competition.max_participants
    }

    // 判断是否已报名
    const isRegistered = (competitionId) => {
      return userRegistrations.value.some(reg => reg.competition === competitionId)
    }

    // 获取状态文本
    const getStatusText = (status) => {
      const statusMap = {
        'registration': '报名中',
        'in_progress': '进行中',
        'completed': '已结束',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    }

    // 获取类型文本
    const getTypeText = (type) => {
      const typeMap = {
        'single': '单打',
        'double': '双打',
        'team': '团体赛'
      }
      return typeMap[type] || type
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString('zh-CN')
    }

    onMounted(() => {
      fetchCompetitions()
      fetchCampuses()
      fetchUserRegistrations()
    })

    return {
      competitions,
      campuses,
      showCreateModal,
      newCompetition,
      userStore,
      createCompetition,
      registerCompetition,
      cancelRegistration,
      viewCompetition,
      canRegister,
      isRegistered,
      getStatusText,
      getTypeText,
      formatDate
    }
  }
}
</script>

<style scoped>
.competitions-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  color: #333;
  margin: 0;
}

.competitions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.competition-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 20px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.competition-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.card-header h3 {
  margin: 0;
  color: #333;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.registration {
  background: #e3f2fd;
  color: #1976d2;
}

.status-badge.in_progress {
  background: #fff3e0;
  color: #f57c00;
}

.status-badge.completed {
  background: #e8f5e8;
  color: #388e3c;
}

.status-badge.cancelled {
  background: #ffebee;
  color: #d32f2f;
}

.card-body p {
  margin: 8px 0;
  color: #666;
}

.card-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.btn-primary {
  background: #1976d2;
  color: white;
}

.btn-primary:hover {
  background: #1565c0;
}

.btn-success {
  background: #388e3c;
  color: white;
}

.btn-success:hover {
  background: #2e7d32;
}

.btn-warning {
  background: #f57c00;
  color: white;
}

.btn-warning:hover {
  background: #ef6c00;
}

.btn-secondary {
  background: #757575;
  color: white;
}

.btn-secondary:hover {
  background: #616161;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-control:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25,118,210,0.2);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>