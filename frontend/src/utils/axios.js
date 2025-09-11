import axios from 'axios'

// 获取CSRF token的函数
function getCSRFToken() {
  // 从cookie中获取CSRF token
  const name = 'csrftoken'
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// 配置axios默认设置
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

// 存储CSRF token
let csrfToken = null
let csrfTokenPromise = null

// 获取CSRF token的异步函数（使用原生 fetch，避免进入 axios 拦截器的递归）
async function fetchCSRFToken() {
  try {
    const response = await fetch('/accounts/api/csrf-token/', {
      credentials: 'same-origin',
      headers: { 'Accept': 'application/json' }
    })
    if (!response.ok) {
      throw new Error(`获取CSRF token失败，状态码: ${response.status}`)
    }
    const data = await response.json()
    csrfToken = data.csrfToken || getCSRFToken()
    return csrfToken
  } catch (error) {
    console.error('获取CSRF token失败:', error)
    return null
  }
}

// 初始化时尝试获取CSRF token（使用 fetch，不会触发 axios 拦截器）
fetchCSRFToken()

// 请求拦截器 - 自动添加CSRF token
axios.interceptors.request.use(
  async (config) => {
    // 保障 headers 存在
    config.headers = config.headers || {}

    // 如果没有CSRF token，尝试获取（使用单例Promise防抖）
    if (!csrfToken) {
      csrfTokenPromise = csrfTokenPromise || fetchCSRFToken()
      await csrfTokenPromise
      csrfTokenPromise = null
    }
    
    // 添加CSRF token到请求头
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken
    }
    
    // 从cookie中获取CSRF token作为备选
    const cookieToken = getCSRFToken()
    if (cookieToken && !config.headers['X-CSRFToken']) {
      config.headers['X-CSRFToken'] = cookieToken
    }
    
    // 确保POST/PUT/PATCH请求包含Content-Type
    const method = (config.method || '').toLowerCase()
    if (['post', 'put', 'patch'].includes(method)) {
      config.headers['Content-Type'] = config.headers['Content-Type'] || 'application/json'
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
axios.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 处理401未授权错误
    if (error.response?.status === 401) {
      // 清除本地存储的token
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
      // 可以在这里重定向到登录页
      // window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default axios