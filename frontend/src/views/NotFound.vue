<template>
  <div class="not-found-page">
    <div class="not-found-container">
      <div class="not-found-content">
        <!-- 404图标 -->
        <div class="error-icon">
          <div class="ping-pong-animation">
            <div class="ball"></div>
            <div class="paddle paddle-left"></div>
            <div class="paddle paddle-right"></div>
          </div>
        </div>
        
        <!-- 错误信息 -->
        <div class="error-info">
          <h1 class="error-code">404</h1>
          <h2 class="error-title">页面未找到</h2>
          <p class="error-description">
            抱歉，您访问的页面不存在或已被移动。
            <br>
            就像乒乓球飞出了球台一样，这个页面也找不到了！
          </p>
        </div>
        
        <!-- 操作按钮 -->
        <div class="error-actions">
          <el-button 
            type="primary" 
            size="large" 
            class="gradient-button"
            @click="goHome"
          >
            <el-icon><House /></el-icon>
            返回首页
          </el-button>
          
          <el-button 
            size="large" 
            @click="goBack"
          >
            <el-icon><ArrowLeft /></el-icon>
            返回上页
          </el-button>
        </div>
        
        <!-- 建议链接 -->
        <div class="suggestions">
          <h3 class="suggestions-title">您可能想要：</h3>
          <div class="suggestions-list">
            <el-link 
              type="primary" 
              @click="$router.push('/')"
              :underline="false"
            >
              <el-icon><House /></el-icon>
              访问首页
            </el-link>
            
            <el-link 
              type="primary" 
              @click="$router.push('/login')"
              :underline="false"
            >
              <el-icon><User /></el-icon>
              用户登录
            </el-link>
            
            <el-link 
              type="primary" 
              @click="$router.push('/register')"
              :underline="false"
            >
              <el-icon><UserFilled /></el-icon>
              用户注册
            </el-link>
            
            <el-link 
              type="primary" 
              @click="contactSupport"
              :underline="false"
            >
              <el-icon><Service /></el-icon>
              联系客服
            </el-link>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="decoration-ball ball-1"></div>
      <div class="decoration-ball ball-2"></div>
      <div class="decoration-ball ball-3"></div>
      <div class="decoration-paddle paddle-bg-1"></div>
      <div class="decoration-paddle paddle-bg-2"></div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  House,
  ArrowLeft,
  User,
  UserFilled,
  Service
} from '@element-plus/icons-vue'

export default {
  name: 'NotFound',
  components: {
    House,
    ArrowLeft,
    User,
    UserFilled,
    Service
  },
  setup() {
    const router = useRouter()
    
    const goHome = () => {
      router.push('/')
    }
    
    const goBack = () => {
      if (window.history.length > 1) {
        router.go(-1)
      } else {
        router.push('/')
      }
    }
    
    const contactSupport = () => {
      ElMessage.info('客服功能开发中，请稍后再试...')
    }
    
    return {
      goHome,
      goBack,
      contactSupport
    }
  }
}
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.not-found-container {
  width: 100%;
  max-width: 600px;
  padding: 40px 20px;
  z-index: 10;
}

.not-found-content {
  text-align: center;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 60px 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

/* 错误图标动画 */
.error-icon {
  margin-bottom: 40px;
}

.ping-pong-animation {
  position: relative;
  width: 200px;
  height: 100px;
  margin: 0 auto;
}

.ball {
  width: 20px;
  height: 20px;
  background: #ff6b6b;
  border-radius: 50%;
  position: absolute;
  top: 40px;
  left: 20px;
  animation: ballBounce 2s ease-in-out infinite;
  box-shadow: 0 4px 8px rgba(255, 107, 107, 0.3);
}

.paddle {
  width: 15px;
  height: 60px;
  background: #4ecdc4;
  border-radius: 8px;
  position: absolute;
  top: 20px;
  box-shadow: 0 4px 8px rgba(78, 205, 196, 0.3);
}

.paddle-left {
  left: 0;
  animation: paddleLeft 2s ease-in-out infinite;
}

.paddle-right {
  right: 0;
  animation: paddleRight 2s ease-in-out infinite;
}

@keyframes ballBounce {
  0%, 100% {
    left: 20px;
    transform: translateY(0);
  }
  25% {
    left: 90px;
    transform: translateY(-20px);
  }
  50% {
    left: 160px;
    transform: translateY(0);
  }
  75% {
    left: 90px;
    transform: translateY(-20px);
  }
}

@keyframes paddleLeft {
  0%, 50%, 100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(15deg);
  }
}

@keyframes paddleRight {
  0%, 50%, 100% {
    transform: rotate(0deg);
  }
  75% {
    transform: rotate(-15deg);
  }
}

/* 错误信息 */
.error-code {
  font-size: 6rem;
  font-weight: bold;
  color: #667eea;
  margin: 0 0 20px 0;
  text-shadow: 2px 2px 4px rgba(102, 126, 234, 0.3);
}

.error-title {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 20px 0;
}

.error-description {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
  margin: 0 0 40px 0;
}

/* 操作按钮 */
.error-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.error-actions .el-button {
  min-width: 140px;
  height: 48px;
  font-size: 1rem;
}

/* 建议链接 */
.suggestions {
  border-top: 1px solid #e4e7ed;
  padding-top: 30px;
}

.suggestions-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 20px 0;
}

.suggestions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.suggestions-list .el-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(102, 126, 234, 0.1);
  transition: all 0.3s;
}

.suggestions-list .el-link:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: translateY(-2px);
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
  animation: float 8s ease-in-out infinite;
}

.ball-1 {
  width: 80px;
  height: 80px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.ball-2 {
  width: 60px;
  height: 60px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.ball-3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 5%;
  animation-delay: 4s;
}

.decoration-paddle {
  position: absolute;
  width: 60px;
  height: 80px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 30px 30px 8px 8px;
  animation: rotate 10s linear infinite;
}

.paddle-bg-1 {
  top: 20%;
  right: 10%;
  animation-delay: 1s;
}

.paddle-bg-2 {
  bottom: 25%;
  right: 25%;
  animation-delay: 3s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) rotate(180deg);
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
  .not-found-container {
    padding: 20px 15px;
  }
  
  .not-found-content {
    padding: 40px 30px;
  }
  
  .error-code {
    font-size: 4rem;
  }
  
  .error-title {
    font-size: 1.5rem;
  }
  
  .error-description {
    font-size: 1rem;
  }
  
  .ping-pong-animation {
    width: 150px;
    height: 80px;
  }
  
  .ball {
    width: 15px;
    height: 15px;
  }
  
  .paddle {
    width: 12px;
    height: 45px;
  }
}

@media (max-width: 480px) {
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .error-actions .el-button {
    width: 100%;
    max-width: 200px;
  }
  
  .suggestions-list {
    flex-direction: column;
    align-items: center;
  }
  
  .suggestions-list .el-link {
    width: 100%;
    max-width: 200px;
    justify-content: center;
  }
}
</style>