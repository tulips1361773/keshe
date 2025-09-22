import axios from 'axios'

// 设置axios基础URL
axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.withCredentials = true

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

// 获取CSRF token的异步函数
async function fetchCSRFToken() {
  try {
    // 先尝试从cookie中获取
    const cookieToken = getCSRFToken()
    if (cookieToken) {
      csrfToken = cookieToken
      console.log('从cookie获取CSRF token成功')
      return csrfToken
    }
    
    // 如果cookie中没有，则从API获取
    const response = await fetch('http://127.0.0.1:8000/api/accounts/csrf-token/', {
      method: 'GET',
      credentials: 'include',
      mode: 'cors',
      headers: { 
        'Accept': 'application/json'
      }
    })
    if (!response.ok) {
      throw new Error(`获取CSRF token失败，状态码: ${response.status}`)
    }
    const data = await response.json()
    csrfToken = data.csrfToken
    console.log('从API获取CSRF token成功')
    return csrfToken
  } catch (error) {
    console.error('获取CSRF token失败:', error)
    // 使用一个默认的token作为最后的备选方案
    csrfToken = 'dummy-token'
    console.log('使用默认CSRF token')
    return csrfToken
  }
}

// 初始化时尝试获取CSRF token（使用 fetch，不会触发 axios 拦截器）
fetchCSRFToken()

// 请求拦截器 - 自动添加CSRF token和Authorization头
axios.interceptors.request.use(
  async (config) => {
    // 保障 headers 存在
    config.headers = config.headers || {}

    // 添加Authorization头（如果存在token）
    const token = localStorage.getItem('token')
    if (token && !config.headers['Authorization']) {
      config.headers['Authorization'] = `Token ${token}`
    }

    // 对于需要CSRF保护的请求，添加CSRF token
    if (['post', 'put', 'patch', 'delete'].includes(config.method?.toLowerCase())) {
      // 优先从cookie中获取CSRF token
      const cookieToken = getCSRFToken()
      if (cookieToken) {
        config.headers['X-CSRFToken'] = cookieToken
      } else {
        // 如果cookie中没有，从API获取
        if (!csrfToken) {
          csrfTokenPromise = csrfTokenPromise || fetchCSRFToken()
          await csrfTokenPromise
          csrfTokenPromise = null
        }
        if (csrfToken && csrfToken !== 'dummy-token') {
          config.headers['X-CSRFToken'] = csrfToken
        }
      }
      
      // 确保POST/PUT/PATCH请求包含Content-Type
      config.headers['Content-Type'] = config.headers['Content-Type'] || 'application/json'
    }
    
    console.log('请求配置:', {
      method: config.method,
      url: config.url,
      headers: {
        'Authorization': config.headers['Authorization'] ? 'Token ***' : 'None',
        'X-CSRFToken': config.headers['X-CSRFToken'] ? config.headers['X-CSRFToken'].substring(0, 10) + '...' : 'None'
      }
    })
    
    return config
  },
  (error) => {
    console.error('请求拦截器错误:', error)
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