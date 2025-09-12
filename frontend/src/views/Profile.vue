<template>
  <div class="profile-page">
    <!-- 顶部导航栏 -->
    <div class="profile-header">
      <div class="header-content">
        <div class="back-section">
          <el-button type="primary" link @click="$router.go(-1)">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
        </div>
        
        <h1 class="page-title">个人资料</h1>
        
        <div class="header-actions">
          <el-button type="primary" @click="handleSave" :loading="saving">
            <el-icon><Check /></el-icon>
            保存
          </el-button>
        </div>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="profile-main">
      <div class="profile-container">
        <!-- 头像区域 -->
        <div class="avatar-section custom-card">
          <div class="avatar-content">
            <el-avatar :size="120" :src="profileForm.avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <div class="avatar-actions">
              <el-button type="primary" size="small" @click="handleAvatarUpload">
                <el-icon><Camera /></el-icon>
                更换头像
              </el-button>
            </div>
          </div>
          
          <div class="user-basic-info">
            <h2 class="user-name">{{ profileForm.real_name || profileForm.username }}</h2>
            <p class="user-type">{{ getUserTypeText(profileForm.user_type) }}</p>
            <p class="join-date">加入时间：{{ formatDate(profileForm.date_joined) }}</p>
          </div>
        </div>

        <!-- 基本信息表单 -->
        <div class="form-section custom-card">
          <div class="section-header">
            <h3 class="section-title">基本信息</h3>
          </div>
          
          <el-form
            ref="profileFormRef"
            :model="profileForm"
            :rules="profileRules"
            label-width="100px"
            class="profile-form"
          >
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="用户名" prop="username">
                  <el-input
                    v-model="profileForm.username"
                    disabled
                    placeholder="用户名不可修改"
                  />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="真实姓名" prop="real_name">
                  <el-input
                    v-model="profileForm.real_name"
                    placeholder="请输入真实姓名"
                    clearable
                  />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="手机号码" prop="phone">
                  <el-input
                    v-model="profileForm.phone"
                    placeholder="请输入手机号码"
                    clearable
                  />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="邮箱地址" prop="email">
                  <el-input
                    v-model="profileForm.email"
                    placeholder="请输入邮箱地址"
                    clearable
                  />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="性别" prop="gender">
                  <el-select v-model="profileForm.gender" placeholder="请选择性别" style="width: 100%">
                    <el-option label="男" value="male" />
                    <el-option label="女" value="female" />
                    <el-option label="未知" value="unknown" />
                  </el-select>
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="用户类型">
                  <el-select v-model="profileForm.user_type" disabled style="width: 100%">
                    <el-option label="学员" value="student" />
                    <el-option label="教练" value="coach" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="地址" prop="address">
                  <el-input
                    v-model="profileForm.address"
                    placeholder="请输入地址"
                    clearable
                  />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="状态">
                  <el-tag :type="profileForm.is_active ? 'success' : 'danger'">
                    {{ profileForm.is_active ? '活跃' : '未激活' }}
                  </el-tag>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="紧急联系人" prop="emergency_contact">
                  <el-input
                    v-model="profileForm.emergency_contact"
                    placeholder="请输入紧急联系人"
                    clearable
                  />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="紧急联系电话" prop="emergency_phone">
                  <el-input
                    v-model="profileForm.emergency_phone"
                    placeholder="请输入紧急联系电话"
                    clearable
                  />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="技能" prop="skills">
                  <el-input
                    v-model="profileForm.skills"
                    placeholder="请输入技能"
                    clearable
                  />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="经验年数" prop="experience_years">
                  <el-input-number
                    v-model="profileForm.experience_years"
                    :min="0"
                    :max="50"
                    placeholder="请输入经验年数"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="个人简介" prop="bio">
              <el-input
                v-model="profileForm.bio"
                type="textarea"
                :rows="4"
                placeholder="介绍一下自己吧..."
                maxlength="500"
                show-word-limit
              />
            </el-form-item>
          </el-form>
        </div>

        <!-- 安全设置 -->
        <div class="security-section custom-card">
          <div class="section-header">
            <h3 class="section-title">安全设置</h3>
          </div>
          
          <div class="security-items">
            <div class="security-item">
              <div class="security-info">
                <h4 class="security-title">登录密码</h4>
                <p class="security-desc">定期更换密码可以提高账户安全性</p>
              </div>
              <el-button type="primary" link @click="showChangePassword = true">
                修改密码
              </el-button>
            </div>
            
            <div class="security-item">
              <div class="security-info">
                <h4 class="security-title">手机绑定</h4>
                <p class="security-desc">{{ profileForm.phone ? `已绑定：${profileForm.phone}` : '未绑定手机号' }}</p>
              </div>
              <el-button type="primary" link>
                {{ profileForm.phone ? '更换' : '绑定' }}
              </el-button>
            </div>
            
            <div class="security-item">
              <div class="security-info">
                <h4 class="security-title">邮箱绑定</h4>
                <p class="security-desc">{{ profileForm.email ? `已绑定：${profileForm.email}` : '未绑定邮箱' }}</p>
              </div>
              <el-button type="primary" link>
                {{ profileForm.email ? '更换' : '绑定' }}
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="showChangePassword"
      title="修改密码"
      width="400px"
      :before-close="handleClosePasswordDialog"
    >
      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="passwordRules"
        label-width="100px"
      >
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input
            v-model="passwordForm.currentPassword"
            type="password"
            placeholder="请输入当前密码"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="passwordForm.newPassword"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            placeholder="请确认新密码"
            show-password
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="handleClosePasswordDialog">取消</el-button>
        <el-button type="primary" @click="handleChangePassword" :loading="changingPassword">
          确认修改
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import {
  ArrowLeft,
  Check,
  User,
  Camera
} from '@element-plus/icons-vue'
import axios from '@/utils/axios'

export default {
  name: 'Profile',
  components: {
    ArrowLeft,
    Check,
    User,
    Camera
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const profileFormRef = ref()
    const passwordFormRef = ref()
    const saving = ref(false)
    const changingPassword = ref(false)
    const showChangePassword = ref(false)

    // 个人资料表单
    const profileForm = reactive({
      username: '',
      real_name: '',
      phone: '',
      email: '',
      gender: 'unknown',
      address: '',
      emergency_contact: '',
      emergency_phone: '',
      skills: '',
      experience_years: 0,
      user_type: 'student',
      is_active: true,
      date_joined: '',
      bio: '',
      avatar: ''
    })

    // 密码修改表单
    const passwordForm = reactive({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })

    // 表单验证规则
    const profileRules = {
      real_name: [
        { required: true, message: '请输入真实姓名', trigger: 'blur' },
        { min: 2, max: 10, message: '姓名长度在 2 到 10 个字符', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入手机号码', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
      ],
      email: [
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      emergency_phone: [
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
      ],
      address: [
        { max: 200, message: '地址长度不能超过200个字符', trigger: 'blur' }
      ],
      emergency_contact: [
        { max: 50, message: '紧急联系人姓名长度不能超过50个字符', trigger: 'blur' }
      ],
      skills: [
        { max: 200, message: '技能描述长度不能超过200个字符', trigger: 'blur' }
      ]
    }

    const validateConfirmPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请确认新密码'))
      } else if (value !== passwordForm.newPassword) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }

    const passwordRules = {
      currentPassword: [
        { required: true, message: '请输入当前密码', trigger: 'blur' }
      ],
      newPassword: [
        { required: true, message: '请输入新密码', trigger: 'blur' },
        { min: 8, max: 16, message: '密码长度必须为8-16位', trigger: 'blur' },
        { pattern: /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>_~`\-+=\[\]\\;/]).*$/, message: '密码必须包含字母、数字和特殊字符', trigger: 'blur' }
      ],
      confirmPassword: [
        { validator: validateConfirmPassword, trigger: 'blur' }
      ]
    }

    // 方法
    const getUserTypeText = (userType) => {
      const typeMap = {
        'student': '学员',
        'coach': '教练',
        'admin': '管理员'
      }
      return typeMap[userType] || '用户'
    }

    const formatDate = (dateString) => {
      if (!dateString) return '未知'
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    const loadProfile = async () => {
      try {
        const response = await axios.get('/accounts/api/profile/')
        const user = response.data
        if (user) {
          Object.assign(profileForm, {
            username: user.username || '',
            real_name: user.real_name || '',
            phone: user.phone || '',
            email: user.email || '',
            gender: user.gender || 'unknown',
            address: user.address || '',
            emergency_contact: user.emergency_contact || '',
            emergency_phone: user.emergency_phone || '',
            skills: user.skills || '',
            experience_years: user.experience_years || 0,
            user_type: user.user_type || 'student',
            is_active: user.is_active !== false,
            date_joined: user.date_joined || '',
            bio: user.bio || '',
            avatar: user.avatar || ''
          })
        }
      } catch (error) {
        console.error('加载个人资料失败:', error)
        ElMessage.error('加载个人资料失败')
      }
    }

    const handleSave = async () => {
      if (!profileFormRef.value) return
      
      try {
        const valid = await profileFormRef.value.validate()
        if (!valid) return

        saving.value = true
        
        const updateData = {
          real_name: profileForm.real_name,
          phone: profileForm.phone,
          email: profileForm.email,
          gender: profileForm.gender,
          address: profileForm.address,
          emergency_contact: profileForm.emergency_contact,
          emergency_phone: profileForm.emergency_phone,
          skills: profileForm.skills,
          experience_years: profileForm.experience_years,
          bio: profileForm.bio
        }

        await axios.put('/accounts/api/profile/update/', updateData)
        
        ElMessage.success('个人资料保存成功')
        // 重新加载资料以获取最新数据
        await loadProfile()
      } catch (error) {
        console.error('保存个人资料失败:', error)
        ElMessage.error('保存过程中发生错误')
      } finally {
        saving.value = false
      }
    }

    const handleAvatarUpload = () => {
      ElMessage.info('头像上传功能开发中...')
    }

    const handleChangePassword = async () => {
      if (!passwordFormRef.value) return
      
      try {
        const valid = await passwordFormRef.value.validate()
        if (!valid) return

        changingPassword.value = true
        
        const passwordData = {
          old_password: passwordForm.currentPassword,
          new_password: passwordForm.newPassword,
          confirm_password: passwordForm.confirmPassword
        }
        
        await axios.post('/accounts/api/change-password/', passwordData)
        
        ElMessage.success('密码修改成功')
        handleClosePasswordDialog()
      } catch (error) {
        console.error('修改密码失败:', error)
        ElMessage.error('修改密码失败')
      } finally {
        changingPassword.value = false
      }
    }

    const handleClosePasswordDialog = () => {
      showChangePassword.value = false
      Object.assign(passwordForm, {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      })
      if (passwordFormRef.value) {
        passwordFormRef.value.resetFields()
      }
    }

    // 初始化
    onMounted(() => {
      if (!userStore.isAuthenticated) {
        router.push('/login')
        return
      }
      loadProfile()
    })

    return {
      profileFormRef,
      passwordFormRef,
      profileForm,
      passwordForm,
      profileRules,
      passwordRules,
      saving,
      changingPassword,
      showChangePassword,
      getUserTypeText,
      formatDate,
      handleSave,
      handleAvatarUpload,
      handleChangePassword,
      handleClosePasswordDialog
    }
  }
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f7fa;
}

/* 顶部导航栏 */
.profile-header {
  background: white;
  border-bottom: 1px solid #e4e7ed;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

/* 主要内容 */
.profile-main {
  padding: 24px;
}

.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 头像区域 */
.avatar-section {
  display: flex;
  align-items: center;
  gap: 32px;
  padding: 32px;
}

.avatar-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.avatar-actions {
  display: flex;
  gap: 12px;
}

.user-basic-info {
  flex: 1;
}

.user-name {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin: 0 0 8px 0;
}

.user-type {
  font-size: 1rem;
  color: #667eea;
  font-weight: 500;
  margin: 0 0 8px 0;
}

.join-date {
  color: #666;
  margin: 0;
}

/* 表单区域 */
.form-section,
.security-section {
  padding: 32px;
}

.section-header {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.profile-form {
  max-width: 800px;
}

/* 安全设置 */
.security-items {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.security-info {
  flex: 1;
}

.security-title {
  font-size: 1rem;
  font-weight: 500;
  color: #333;
  margin: 0 0 4px 0;
}

.security-desc {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-main {
    padding: 16px;
  }
  
  .avatar-section {
    flex-direction: column;
    text-align: center;
    gap: 24px;
    padding: 24px;
  }
  
  .form-section,
  .security-section {
    padding: 24px;
  }
  
  .header-content {
    padding: 0 16px;
  }
  
  .page-title {
    font-size: 1.3rem;
  }
}

@media (max-width: 480px) {
  .security-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .avatar-section {
    padding: 20px;
  }
  
  .form-section,
  .security-section {
    padding: 20px;
  }
}
</style>