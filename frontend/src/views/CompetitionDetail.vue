<template>
  <div class="competition-detail-container">
    <div v-if="loading" class="loading">加载中...</div>
    
    <div v-else-if="competition" class="competition-detail">
      <!-- 比赛基本信息 -->
      <div class="competition-info">
        <div class="info-header">
          <h1>{{ competition.name }}</h1>
          <span class="status-badge" :class="competition.status">
            {{ getStatusText(competition.status) }}
          </span>
        </div>
        
        <div class="info-grid">
          <div class="info-item">
            <label>比赛类型:</label>
            <span>{{ getTypeText(competition.competition_type) }}</span>
          </div>
          <div class="info-item">
            <label>校区:</label>
            <span>{{ competition.campus_name }}</span>
          </div>
          <div class="info-item">
            <label>最大参赛人数:</label>
            <span>{{ competition.max_participants }}</span>
          </div>
          <div class="info-item">
            <label>已报名人数:</label>
            <span>{{ competition.registration_count }}</span>
          </div>
          <div class="info-item">
            <label>报名截止时间:</label>
            <span>{{ formatDate(competition.registration_deadline) }}</span>
          </div>
          <div class="info-item">
            <label>比赛开始时间:</label>
            <span>{{ formatDate(competition.start_date) }}</span>
          </div>
        </div>
        
        <div v-if="competition.description" class="description">
          <h3>比赛描述</h3>
          <p>{{ competition.description }}</p>
        </div>
        
        <!-- 操作按钮 -->
        <div class="actions">
          <button 
            v-if="canRegister" 
            @click="registerCompetition"
            class="btn btn-success"
          >
            报名参赛
          </button>
          <button 
            v-if="isRegistered && competition.status === 'registration'"
            @click="cancelRegistration"
            class="btn btn-warning"
          >
            取消报名
          </button>
          <button 
            v-if="canManage"
            @click="createGroups"
            :disabled="competition.status !== 'registration'"
            class="btn btn-primary"
          >
            创建分组
          </button>
          <button 
            v-if="canManage"
            @click="generateMatches"
            :disabled="!hasGroups"
            class="btn btn-primary"
          >
            生成对阵
          </button>
        </div>
      </div>

      <!-- 标签页 -->
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.key"
          @click="activeTab = tab.key"
          :class="['tab-btn', { active: activeTab === tab.key }]"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- 标签页内容 -->
      <div class="tab-content">
        <!-- 报名列表 -->
        <div v-if="activeTab === 'registrations'" class="registrations">
          <h3>报名列表</h3>
          <div v-if="registrations.length === 0" class="empty-state">
            暂无报名记录
          </div>
          <div v-else class="registration-list">
            <div 
              v-for="registration in registrations" 
              :key="registration.id"
              class="registration-item"
            >
              <div class="student-info">
                <h4>{{ registration.student_name }}</h4>
                <p>{{ registration.student_real_name }}</p>
                <p>{{ registration.student_phone }}</p>
              </div>
              <div class="registration-time">
                {{ formatDate(registration.registration_time) }}
              </div>
            </div>
          </div>
        </div>

        <!-- 分组信息 -->
        <div v-if="activeTab === 'groups'" class="groups">
          <h3>分组信息</h3>
          <div v-if="groups.length === 0" class="empty-state">
            暂未创建分组
          </div>
          <div v-else class="group-list">
            <div 
              v-for="group in groups" 
              :key="group.id"
              class="group-item"
            >
              <h4>{{ group.name }}</h4>
              <div class="group-members">
                <div 
                  v-for="member in group.members" 
                  :key="member.id"
                  class="member-item"
                >
                  <span class="seed">{{ member.seed_number }}</span>
                  <span class="name">{{ member.student_name }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 对阵表 -->
        <div v-if="activeTab === 'matches'" class="matches">
          <h3>对阵表</h3>
          <div v-if="matches.length === 0" class="empty-state">
            暂未生成对阵
          </div>
          <div v-else class="match-list">
            <div 
              v-for="match in matches" 
              :key="match.id"
              class="match-item"
              :class="{ completed: match.status === 'completed' }"
            >
              <div class="match-header">
                <span class="round">{{ match.round_name }}</span>
                <span class="status">{{ getMatchStatusText(match.status) }}</span>
              </div>
              <div class="match-players">
                <div class="player">
                  <span class="name">{{ match.player1_name }}</span>
                  <span v-if="match.player1_score !== null" class="score">{{ match.player1_score }}</span>
                </div>
                <div class="vs">VS</div>
                <div class="player">
                  <span class="name">{{ match.player2_name }}</span>
                  <span v-if="match.player2_score !== null" class="score">{{ match.player2_score }}</span>
                </div>
              </div>
              <div v-if="match.scheduled_time" class="match-time">
                {{ formatDate(match.scheduled_time) }}
              </div>
              <div v-if="canManage && match.status === 'scheduled'" class="match-actions">
                <button @click="recordResult(match)" class="btn btn-sm btn-primary">
                  记录结果
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 记录比赛结果模态框 -->
    <div v-if="showResultModal" class="modal-overlay" @click="showResultModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h2>记录比赛结果</h2>
          <button @click="showResultModal = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="match-info">
            <h3>{{ selectedMatch?.player1_name }} VS {{ selectedMatch?.player2_name }}</h3>
          </div>
          <form @submit.prevent="submitResult">
            <div class="score-input">
              <div class="player-score">
                <label>{{ selectedMatch?.player1_name }} 得分:</label>
                <input v-model.number="resultForm.player1_score" type="number" min="0" required class="form-control">
              </div>
              <div class="player-score">
                <label>{{ selectedMatch?.player2_name }} 得分:</label>
                <input v-model.number="resultForm.player2_score" type="number" min="0" required class="form-control">
              </div>
            </div>
            <div class="modal-actions">
              <button type="button" @click="showResultModal = false" class="btn btn-secondary">取消</button>
              <button type="submit" class="btn btn-primary">提交结果</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from '@/utils/axios'

export default {
  name: 'CompetitionDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const userStore = useUserStore()
    
    const loading = ref(true)
    const competition = ref(null)
    const registrations = ref([])
    const groups = ref([])
    const matches = ref([])
    const activeTab = ref('registrations')
    const showResultModal = ref(false)
    const selectedMatch = ref(null)
    const isRegistered = ref(false)
    
    const resultForm = ref({
      player1_score: 0,
      player2_score: 0
    })
    
    const tabs = [
      { key: 'registrations', label: '报名列表' },
      { key: 'groups', label: '分组信息' },
      { key: 'matches', label: '对阵表' }
    ]

    // 计算属性
    const canRegister = computed(() => {
      return userStore.user?.user_type === 'student' && 
             competition.value?.status === 'registration' && 
             !isRegistered.value &&
             competition.value?.registration_count < competition.value?.max_participants
    })

    const canManage = computed(() => {
      return userStore.user?.user_type === 'coach'
    })

    const hasGroups = computed(() => {
      return groups.value.length > 0
    })

    // 获取比赛详情
    const fetchCompetition = async () => {
      try {
        const response = await axios.get(`/api/competitions/${route.params.id}/`)
        competition.value = response.data
      } catch (error) {
        console.error('获取比赛详情失败:', error)
        router.push('/competitions')
      }
    }

    // 获取报名列表
    const fetchRegistrations = async () => {
      try {
        const response = await axios.get(`/api/competitions/${route.params.id}/registrations/`)
        registrations.value = response.data
        
        // 检查当前用户是否已报名
        if (userStore.user?.user_type === 'student') {
          isRegistered.value = registrations.value.some(
            reg => reg.student === userStore.user.id
          )
        }
      } catch (error) {
        console.error('获取报名列表失败:', error)
      }
    }

    // 获取分组信息
    const fetchGroups = async () => {
      try {
        const response = await axios.get(`/api/competitions/${route.params.id}/groups/`)
        groups.value = response.data
      } catch (error) {
        console.error('获取分组信息失败:', error)
      }
    }

    // 获取对阵信息
    const fetchMatches = async () => {
      try {
        const response = await axios.get(`/api/competitions/${route.params.id}/matches/`)
        matches.value = response.data
      } catch (error) {
        console.error('获取对阵信息失败:', error)
      }
    }

    // 报名参赛
    const registerCompetition = async () => {
      try {
        await axios.post(`/api/competitions/${route.params.id}/register/`)
        await fetchCompetition()
        await fetchRegistrations()
        alert('报名成功！')
      } catch (error) {
        console.error('报名失败:', error)
        alert(error.response?.data?.error || '报名失败，请重试')
      }
    }

    // 取消报名
    const cancelRegistration = async () => {
      try {
        await axios.post(`/api/competitions/${route.params.id}/cancel-registration/`)
        await fetchCompetition()
        await fetchRegistrations()
        alert('取消报名成功！')
      } catch (error) {
        console.error('取消报名失败:', error)
        alert(error.response?.data?.error || '取消报名失败，请重试')
      }
    }

    // 创建分组
    const createGroups = async () => {
      try {
        await axios.post(`/api/competitions/${route.params.id}/create-groups/`)
        await fetchGroups()
        alert('分组创建成功！')
      } catch (error) {
        console.error('创建分组失败:', error)
        alert(error.response?.data?.error || '创建分组失败，请重试')
      }
    }

    // 生成对阵
    const generateMatches = async () => {
      try {
        await axios.post(`/api/competitions/${route.params.id}/generate-matches/`)
        await fetchMatches()
        alert('对阵生成成功！')
      } catch (error) {
        console.error('生成对阵失败:', error)
        alert(error.response?.data?.error || '生成对阵失败，请重试')
      }
    }

    // 记录比赛结果
    const recordResult = (match) => {
      selectedMatch.value = match
      resultForm.value = {
        player1_score: 0,
        player2_score: 0
      }
      showResultModal.value = true
    }

    // 提交比赛结果
    const submitResult = async () => {
      try {
        await axios.post(`/api/competitions/matches/${selectedMatch.value.id}/record-result/`, resultForm.value)
        showResultModal.value = false
        await fetchMatches()
        alert('比赛结果记录成功！')
      } catch (error) {
        console.error('记录比赛结果失败:', error)
        alert(error.response?.data?.error || '记录比赛结果失败，请重试')
      }
    }

    // 工具函数
    const getStatusText = (status) => {
      const statusMap = {
        'registration': '报名中',
        'in_progress': '进行中',
        'completed': '已结束',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    }

    const getTypeText = (type) => {
      const typeMap = {
        'single': '单打',
        'double': '双打',
        'team': '团体赛'
      }
      return typeMap[type] || type
    }

    const getMatchStatusText = (status) => {
      const statusMap = {
        'scheduled': '待进行',
        'in_progress': '进行中',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString('zh-CN')
    }

    // 初始化数据
    const initData = async () => {
      loading.value = true
      await fetchCompetition()
      await Promise.all([
        fetchRegistrations(),
        fetchGroups(),
        fetchMatches()
      ])
      loading.value = false
    }

    onMounted(() => {
      initData()
    })

    return {
      loading,
      competition,
      registrations,
      groups,
      matches,
      activeTab,
      tabs,
      showResultModal,
      selectedMatch,
      resultForm,
      canRegister,
      canManage,
      hasGroups,
      isRegistered,
      registerCompetition,
      cancelRegistration,
      createGroups,
      generateMatches,
      recordResult,
      submitResult,
      getStatusText,
      getTypeText,
      getMatchStatusText,
      formatDate
    }
  }
}
</script>

<style scoped>
.competition-detail-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.loading {
  text-align: center;
  padding: 50px;
  font-size: 18px;
  color: #666;
}

.competition-info {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 30px;
  margin-bottom: 30px;
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.info-header h1 {
  margin: 0;
  color: #333;
}

.status-badge {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
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

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item label {
  font-weight: bold;
  color: #666;
  margin-bottom: 5px;
}

.info-item span {
  color: #333;
  font-size: 16px;
}

.description {
  margin-bottom: 30px;
}

.description h3 {
  color: #333;
  margin-bottom: 10px;
}

.description p {
  color: #666;
  line-height: 1.6;
}

.actions {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.tabs {
  display: flex;
  background: white;
  border-radius: 8px 8px 0 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.tab-btn {
  flex: 1;
  padding: 15px 20px;
  border: none;
  background: #f5f5f5;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
  border-bottom: 3px solid transparent;
}

.tab-btn:hover {
  background: #e0e0e0;
}

.tab-btn.active {
  background: white;
  color: #1976d2;
  border-bottom-color: #1976d2;
}

.tab-content {
  background: white;
  border-radius: 0 0 8px 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 30px;
  min-height: 400px;
}

.tab-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
}

.empty-state {
  text-align: center;
  color: #999;
  padding: 50px;
  font-size: 16px;
}

/* 报名列表样式 */
.registration-list {
  display: grid;
  gap: 15px;
}

.registration-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 6px;
}

.student-info h4 {
  margin: 0 0 5px 0;
  color: #333;
}

.student-info p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.registration-time {
  color: #999;
  font-size: 14px;
}

/* 分组样式 */
.group-list {
  display: grid;
  gap: 20px;
}

.group-item {
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 20px;
}

.group-item h4 {
  margin: 0 0 15px 0;
  color: #333;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.group-members {
  display: grid;
  gap: 10px;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  background: #f9f9f9;
  border-radius: 4px;
}

.seed {
  background: #1976d2;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.name {
  color: #333;
}

/* 对阵表样式 */
.match-list {
  display: grid;
  gap: 15px;
}

.match-item {
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 20px;
  transition: all 0.2s;
}

.match-item.completed {
  background: #f8f9fa;
  border-color: #28a745;
}

.match-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.round {
  font-weight: bold;
  color: #333;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  background: #e9ecef;
  color: #495057;
}

.match-players {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 15px;
}

.player {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  min-width: 120px;
}

.player .name {
  font-weight: bold;
  color: #333;
}

.player .score {
  font-size: 24px;
  font-weight: bold;
  color: #1976d2;
}

.vs {
  font-weight: bold;
  color: #666;
  font-size: 18px;
}

.match-time {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-bottom: 15px;
}

.match-actions {
  text-align: center;
}

/* 按钮样式 */
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
  text-decoration: none;
  display: inline-block;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #1976d2;
  color: white;
}

.btn-primary:hover:not(:disabled) {
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

.match-info {
  text-align: center;
  margin-bottom: 20px;
}

.match-info h3 {
  margin: 0;
  color: #333;
}

.score-input {
  display: grid;
  gap: 15px;
  margin-bottom: 20px;
}

.player-score label {
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
}
</style>