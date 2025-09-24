<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card custom-card">
        <div class="register-header">
          <div class="logo">
            <el-icon class="logo-icon"><Basketball /></el-icon>
            <h1 class="logo-text">乒乓球培训系统</h1>
          </div>
          <h2 class="register-title">用户注册</h2>
          <p class="register-subtitle">加入我们，开启您的乒乓球学习之旅</p>
        </div>

        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          class="register-form"
          @submit.prevent="handleRegister"
        >
          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="请输入用户名"
              size="large"
              :prefix-icon="User"
              clearable
            />
          </el-form-item>

          <el-form-item prop="real_name">
            <el-input
              v-model="registerForm.real_name"
              placeholder="请输入真实姓名"
              size="large"
              :prefix-icon="UserFilled"
              clearable
            />
          </el-form-item>

          <el-form-item prop="phone">
            <el-input
              v-model="registerForm.phone"
              placeholder="请输入手机号码"
              size="large"
              :prefix-icon="Phone"
              clearable
            />
          </el-form-item>

          <el-form-item prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱地址（可选）"
              size="large"
              :prefix-icon="Message"
              clearable
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              :prefix-icon="Lock"
              show-password
              clearable
            />
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请确认密码"
              size="large"
              :prefix-icon="Lock"
              show-password
              clearable
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <el-form-item prop="user_type">
            <el-select
              v-model="registerForm.user_type"
              placeholder="请选择用户类型"
              size="large"
              style="width: 100%"
            >
              <el-option
                label="学员"
                value="student"
              >
                <div class="user-type-option">
                  <el-icon><User /></el-icon>
                  <span>学员 - 参加培训课程</span>
                </div>
              </el-option>
              <el-option
                label="教练"
                value="coach"
              >
                <div class="user-type-option">
                  <el-icon><Star /></el-icon>
                  <span>教练 - 教授培训课程</span>
                </div>
              </el-option>
            </el-select>
          </el-form-item>

          <!-- 教练员专用字段 -->
          <el-form-item 
            v-if="registerForm.user_type === 'coach'"
            prop="avatar"
            label="头像照片"
          >
            <div class="avatar-upload-container">
              <el-upload
                class="avatar-uploader"
                :show-file-list="false"
                :before-upload="beforeAvatarUpload"
                :on-success="handleAvatarSuccess"
                :on-error="handleAvatarError"
                action="#"
                :http-request="uploadAvatar"
              >
                <img v-if="registerForm.avatar" :src="registerForm.avatar" class="avatar-preview" />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
              </el-upload>
              <div class="upload-tips">
                <p>点击上传头像照片（教练员必填）</p>
                <p class="tips-text">支持 JPG、PNG 格式，文件大小不超过 2MB</p>
              </div>
            </div>
          </el-form-item>

          <!-- 校区选择 (仅教练员) -->
          <el-form-item 
            v-if="registerForm.user_type === 'coach'" 
            label="所属校区" 
            prop="campus_id"
            class="form-item"
          >
            <el-select 
              v-model="registerForm.campus_id" 
              placeholder="请选择所属校区"
              style="width: 100%"
              :loading="campusLoading"
            >
              <el-option
                v-for="campus in campusList"
                :key="campus.id"
                :label="campus.name"
                :value="campus.id"
              />
            </el-select>
          </el-form-item>

          <!-- 成绩描述 (仅教练员) -->
          <!-- 校区选择 (仅教练员) -->
          <el-form-item 
            v-if="registerForm.user_type === 'coach'" 
            label="所属校区" 
            prop="campus_id"
            class="form-item"
          >
            <el-select 
              v-model="registerForm.campus_id" 
              placeholder="请选择所属校区"
              style="width: 100%"
              :loading="campusLoading"
            >
              <el-option
                v-for="campus in campusList"
                :key="campus.id"
                :label="campus.name"
                :value="campus.id"
              />
            </el-select>
          </el-form-item>

          <!-- 成绩描述 (仅教练员) -->
          <el-form-item 
            v-if="registerForm.user_type === 'coach'"
            prop="achievements"
          >
            <el-input
              v-model="registerForm.achievements"
              type="textarea"
              :rows="3"
              placeholder="请填写您的比赛成绩描述（教练员必填）"
              size="large"
              clearable
            />
          </el-form-item>

          <el-form-item prop="agreement">
            <el-checkbox v-model="registerForm.agreement">
              我已阅读并同意
              <el-link type="primary" :underline="false">
                《用户协议》
              </el-link>
              和
              <el-link type="primary" :underline="false">
                《隐私政策》
              </el-link>
            </el-checkbox>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="register-button gradient-button"
              :loading="userStore.isLoading"
              @click="handleRegister"
              native-type="submit"
            >
              <el-icon v-if="!userStore.isLoading"><Right /></el-icon>
              {{ userStore.isLoading ? '注册中...' : '立即注册' }}
            </el-button>
          </el-form-item>
        </el-form>

        <div class="register-footer">
          <p class="login-link">
            已有账户？
            <el-link type="primary" @click="$router.push('/login')">
              立即登录
            </el-link>
          </p>
          <el-divider>或</el-divider>
          <el-button
            class="back-home-button"
            @click="$router.push('/')"
          >
            <el-icon><House /></el-icon>
            返回首页
          </el-button>
        </div>
      </div>
    </div>

    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="decoration-ball ball-1"></div>
      <div class="decoration-ball ball-2"></div>
      <div class="decoration-ball ball-3"></div>
      <div class="decoration-ball ball-4"></div>
      <div class="decoration-paddle paddle-1"></div>
      <div class="decoration-paddle paddle-2"></div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import axios from 'axios'
import {
  Basketball,
  User,
  UserFilled,
  Phone,
  Message,
  Lock,
  Right,
  House,
  Star,
  Plus
} from '@element-plus/icons-vue'

export default {
  name: 'Register',
  components: {
    Basketball,
    User,
    UserFilled,
    Phone,
    Message,
    Lock,
    Right,
    House,
    Star,
    Plus
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const registerFormRef = ref()
    
    // 校区相关数据
    const campusList = ref([])
    const campusLoading = ref(false)
    
    // 校区相关数据
    const campusList = ref([])
    const campusLoading = ref(false)

    const registerForm = reactive({
      username: '',
      real_name: '',
      phone: '',
      email: '',
      password: '',
      confirmPassword: '',
      user_type: 'student',
      avatar: null,
      avatar: null,
      achievements: '',
      campus_id: null,
      campus_id: null,
      agreement: false
    })

    // 自定义验证规则
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入手机号码'))
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号码'))
      } else {
        callback()
      }
    }

    const validateEmail = (rule, value, callback) => {
      if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        callback(new Error('请输入正确的邮箱地址'))
      } else {
        callback()
      }
    }

    const validateConfirmPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请确认密码'))
      } else if (value !== registerForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }

    const validateAgreement = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请阅读并同意用户协议和隐私政策'))
      } else {
        callback()
      }
    }

    const registerRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
        { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
      ],
      agreement: [
        { validator: validateAgreement, trigger: 'change' }
      ],
      agreement: [
        { validator: validateAgreement, trigger: 'change' }
      ],
      real_name: [
        { required: true, message: '请输入真实姓名', trigger: 'blur' },
        { min: 2, max: 10, message: '姓名长度在 2 到 10 个字符', trigger: 'blur' }
      ],
      phone: [
        { validator: validatePhone, trigger: 'blur' }
      ],
      email: [
        { validator: validateEmail, trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 8, max: 16, message: '密码长度必须为8-16位', trigger: 'blur' },
        { pattern: /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>_~`\-+=\[\]\\;/]).*$/, message: '密码必须包含字母、数字和特殊字符', trigger: 'blur' }
      ],
      confirmPassword: [
        { validator: validateConfirmPassword, trigger: 'blur' }
      ],
      user_type: [
        { required: true, message: '请选择用户类型', trigger: 'change' }
      ],
      avatar: [
        { 
          validator: (rule, value, callback) => {
            if (registerForm.user_type === 'coach') {
              if (!value || value.trim() === '') {
                callback(new Error('教练员必须上传头像照片'))
              } else {
                callback()
              }
            } else {
              callback()
            }
          }, 
          trigger: 'change' 
        }
      ],
      achievements: [
        { 
          validator: (rule, value, callback) => {
            if (registerForm.user_type === 'coach') {
              if (!value || value.trim() === '') {
                callback(new Error('教练员必须填写比赛成绩描述'))
              } else if (value.trim().length < 10) {
                callback(new Error('成绩描述至少需要10个字符'))
              } else {
                callback()
              }
            } else {
              callback()
            }
          }, 
          trigger: 'blur' 
        }
      ],
      campus_id: [
        { 
          validator: (rule, value, callback) => {
            if (registerForm.user_type === 'coach' && !value) {
              callback(new Error('请选择所属校区'))
            } else {
              callback()
            }
          }, 
          trigger: 'change' 
        }
      ],
      campus_id: [
        { 
          validator: (rule, value, callback) => {
            if (registerForm.user_type === 'coach' && !value) {
              callback(new Error('请选择所属校区'))
            } else {
              callback()
            }
          }, 
          trigger: 'change' 
        }
      ],
    }

    // 头像上传相关方法
    const beforeAvatarUpload = (file) => {
      const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG) {
        ElMessage.error('头像图片只能是 JPG 或 PNG 格式!')
        return false
      }
      if (!isLt2M) {
        ElMessage.error('头像图片大小不能超过 2MB!')
        return false
      }
      return true
    }

    const uploadAvatar = (options) => {
      const { file } = options
      const reader = new FileReader()
      reader.onload = (e) => {
        registerForm.avatar = e.target.result
        ElMessage.success('头像上传成功!')
      }
      reader.readAsDataURL(file)
    }

    const handleAvatarSuccess = (response, file) => {
      // 处理上传成功
    }

    const handleAvatarError = (error) => {
      ElMessage.error('头像上传失败，请重试!')
    }

    const handleRegister = async () => {
      if (!registerFormRef.value) return
      
      try {
        const valid = await registerFormRef.value.validate()
        if (!valid) return

        // 构建注册数据
        const registerData = {
          username: registerForm.username,
          real_name: registerForm.real_name,
          phone: registerForm.phone,
          email: registerForm.email || undefined,
          password: registerForm.password,
          password_confirm: registerForm.confirmPassword,
          user_type: registerForm.user_type
        }

        // 如果是教练员，添加成绩描述、头像和校区
        // 如果是教练员，添加成绩描述、头像和校区
        if (registerForm.user_type === 'coach') {
          registerData.achievements = registerForm.achievements
          registerData.avatar = registerForm.avatar
          registerData.campus_id = registerForm.campus_id
          registerData.campus_id = registerForm.campus_id
        }

        const result = await userStore.register(registerData)
        
        console.log('注册结果:', result)
        
        if (result.success) {
          ElMessage.success('注册成功！正在跳转到登录页面...')
          setTimeout(() => {
            router.push('/login')
          }, 1500)
        } else {
          console.log('注册失败，错误信息:', result.message)
          ElMessage.error(result.message || '注册失败')
        }
      } catch (error) {
        console.error('注册错误:', error)
        ElMessage.error('注册过程中发生错误')
      }
    }

    // 获取校区列表
    const fetchCampusList = async () => {
      try {
        campusLoading.value = true
        const response = await axios.get('/api/campus/api/list/')
        console.log('校区列表API响应:', response.data)
        // API返回格式: {success: true, data: [...], count: 24}
        campusList.value = response.data.data || []
      } catch (error) {
        console.error('获取校区列表失败:', error)
        ElMessage.error('获取校区列表失败')
      } finally {
        campusLoading.value = false
      }
    }

    // 初始化时检查是否已登录并获取校区列表
    onMounted(() => {
      if (userStore.isAuthenticated) {
        router.push('/dashboard')
      }
      fetchCampusList()
      fetchCampusList()
    })

    return {
      registerFormRef,
      registerForm,
      registerRules,
      userStore,
      handleRegister,
      beforeAvatarUpload,
      uploadAvatar,
      handleAvatarSuccess,
      handleAvatarError,
      campusList,
      campusLoading
      handleAvatarError,
      campusList,
      campusLoading
    }
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 20px 0;
}

.register-container {
  width: 100%;
  max-width: 500px;
  padding: 20px;
  z-index: 10;
}

.register-card {
  padding: 40px;
  text-align: center;
  position: relative;
}

.register-header {
  margin-bottom: 40px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 20px;
}

.logo-icon {
  font-size: 2.5rem;
  color: #667eea;
}

.logo-text {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.register-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin: 0 0 10px 0;
}

.register-subtitle {
  color: #666;
  margin: 0;
  font-size: 0.95rem;
}

.register-form {
  text-align: left;
}

.user-type-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.register-button {
  width: 100%;
  height: 50px;
  font-size: 1.1rem;
  font-weight: 500;
}

.register-footer {
  margin-top: 30px;
  text-align: center;
}

.login-link {
  margin: 0 0 20px 0;
  color: #666;
}

.back-home-button {
  width: 100%;
  height: 45px;
}

/* 背景装饰 */
.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.decoration-ball {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.ball-1 {
  width: 50px;
  height: 50px;
  top: 8%;
  left: 8%;
  animation-delay: 0s;
}

.ball-2 {
  width: 35px;
  height: 35px;
  top: 25%;
  right: 12%;
  animation-delay: 1.5s;
}

.ball-3 {
  width: 70px;
  height: 70px;
  bottom: 25%;
  left: 3%;
  animation-delay: 3s;
}

.ball-4 {
  width: 45px;
  height: 45px;
  bottom: 8%;
  right: 8%;
  animation-delay: 4.5s;
}

.decoration-paddle {
  position: absolute;
  width: 45px;
  height: 65px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 22px 22px 5px 5px;
  animation: rotate 8s linear infinite;
}

.paddle-1 {
  top: 12%;
  right: 8%;
  animation-delay: 1s;
}

.paddle-2 {
  bottom: 12%;
  right: 25%;
  animation-delay: 3s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .register-container {
    padding: 15px;
  }
  
  .register-card {
    padding: 30px 25px;
  }
  
  .logo-text {
    font-size: 1.5rem;
  }
  
  .register-title {
    font-size: 1.5rem;
  }
}

/* 头像上传样式 */
.avatar-upload-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar-uploader {
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-uploader:hover {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-preview {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 6px;
}

.upload-tips {
  flex: 1;
}

.upload-tips p {
  margin: 0 0 5px 0;
  color: #606266;
  font-size: 14px;
}

.tips-text {
  color: #909399;
  font-size: 12px;
}

@media (max-width: 768px) {
  .avatar-upload-container {
    flex-direction: column;
    gap: 10px;
  }
  
  .upload-tips {
    text-align: center;
  }
}

@media (max-width: 480px) {
  .register-page {
    padding: 10px 0;
  }
  
  .register-card {
    padding: 25px 20px;
  }
}

/* 表单动画 */
.register-form .el-form-item {
  animation: slideInUp 0.6s ease-out;
  animation-fill-mode: both;
}

.register-form .el-form-item:nth-child(1) { animation-delay: 0.1s; }
.register-form .el-form-item:nth-child(2) { animation-delay: 0.15s; }
.register-form .el-form-item:nth-child(3) { animation-delay: 0.2s; }
.register-form .el-form-item:nth-child(4) { animation-delay: 0.25s; }
.register-form .el-form-item:nth-child(5) { animation-delay: 0.3s; }
.register-form .el-form-item:nth-child(6) { animation-delay: 0.35s; }
.register-form .el-form-item:nth-child(7) { animation-delay: 0.4s; }
.register-form .el-form-item:nth-child(8) { animation-delay: 0.45s; }
.register-form .el-form-item:nth-child(9) { animation-delay: 0.5s; }

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>