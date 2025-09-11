<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card custom-card">
        <div class="login-header">
          <div class="logo">
            <el-icon class="logo-icon"><Basketball /></el-icon>
            <h1 class="logo-text">乒乓球培训系统</h1>
          </div>
          <h2 class="login-title">用户登录</h2>
          <p class="login-subtitle">欢迎回来，请登录您的账户</p>
        </div>

        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              size="large"
              :prefix-icon="User"
              clearable
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              :prefix-icon="Lock"
              show-password
              clearable
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-form-item>
            <div class="login-options">
              <el-checkbox v-model="rememberMe">记住我</el-checkbox>
              <el-link type="primary" :underline="false">
                忘记密码？
              </el-link>
            </div>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="login-button gradient-button"
              :loading="userStore.isLoading"
              @click="handleLogin"
              native-type="submit"
            >
              <el-icon v-if="!userStore.isLoading"><Right /></el-icon>
              {{ userStore.isLoading ? '登录中...' : '立即登录' }}
            </el-button>
          </el-form-item>
        </el-form>

        <div class="login-footer">
          <p class="register-link">
            还没有账户？
            <el-link type="primary" @click="$router.push('/register')">
              立即注册
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
      <div class="decoration-paddle paddle-1"></div>
      <div class="decoration-paddle paddle-2"></div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import {
  Basketball,
  User,
  Lock,
  Right,
  House
} from '@element-plus/icons-vue'

export default {
  name: 'Login',
  components: {
    Basketball,
    User,
    Lock,
    Right,
    House
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const userStore = useUserStore()
    const loginFormRef = ref()
    const rememberMe = ref(false)

    const loginForm = reactive({
      username: '',
      password: ''
    })

    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
      ]
    }

    const handleLogin = async () => {
      if (!loginFormRef.value) return
      
      try {
        const valid = await loginFormRef.value.validate()
        if (!valid) return

        const result = await userStore.login(loginForm)
        
        if (result.success) {
          ElMessage.success('登录成功！')
          
          // 获取重定向路径
          const redirectPath = route.query.redirect || '/dashboard'
          router.push(redirectPath)
        } else {
          ElMessage.error(result.message || '登录失败')
        }
      } catch (error) {
        console.error('登录错误:', error)
        ElMessage.error('登录过程中发生错误')
      }
    }

    // 初始化时检查是否已登录
    onMounted(() => {
      if (userStore.isAuthenticated) {
        router.push('/dashboard')
      }
    })

    return {
      loginFormRef,
      loginForm,
      loginRules,
      rememberMe,
      userStore,
      handleLogin,
      User,
      Lock
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.login-container {
  width: 100%;
  max-width: 450px;
  padding: 20px;
  z-index: 10;
}

.login-card {
  padding: 40px;
  text-align: center;
  position: relative;
}

.login-header {
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

.login-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin: 0 0 10px 0;
}

.login-subtitle {
  color: #666;
  margin: 0;
  font-size: 0.95rem;
}

.login-form {
  text-align: left;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.login-button {
  width: 100%;
  height: 50px;
  font-size: 1.1rem;
  font-weight: 500;
}

.login-footer {
  margin-top: 30px;
  text-align: center;
}

.register-link {
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
  width: 60px;
  height: 60px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.ball-2 {
  width: 40px;
  height: 40px;
  top: 70%;
  right: 15%;
  animation-delay: 2s;
}

.ball-3 {
  width: 80px;
  height: 80px;
  bottom: 20%;
  left: 5%;
  animation-delay: 4s;
}

.decoration-paddle {
  position: absolute;
  width: 50px;
  height: 70px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 25px 25px 5px 5px;
  animation: rotate 8s linear infinite;
}

.paddle-1 {
  top: 15%;
  right: 10%;
  animation-delay: 1s;
}

.paddle-2 {
  bottom: 15%;
  right: 20%;
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
  .login-container {
    padding: 15px;
  }
  
  .login-card {
    padding: 30px 25px;
  }
  
  .logo-text {
    font-size: 1.5rem;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .login-options {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
}

/* 表单动画 */
.login-form .el-form-item {
  animation: slideInUp 0.6s ease-out;
  animation-fill-mode: both;
}

.login-form .el-form-item:nth-child(1) { animation-delay: 0.1s; }
.login-form .el-form-item:nth-child(2) { animation-delay: 0.2s; }
.login-form .el-form-item:nth-child(3) { animation-delay: 0.3s; }
.login-form .el-form-item:nth-child(4) { animation-delay: 0.4s; }

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