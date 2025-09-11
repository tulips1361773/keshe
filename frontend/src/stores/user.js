import { defineStore } from 'pinia'
import axios from '../utils/axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isLoading: false
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userInfo: (state) => state.user,
    isStudent: (state) => state.user?.user_type === 'student',
    isCoach: (state) => state.user?.user_type === 'coach',
    isAdmin: (state) => state.user?.user_type === 'admin'
  },

  actions: {
    // 设置认证token
    setToken(token) {
      this.token = token
      if (token) {
        localStorage.setItem('token', token)
        axios.defaults.headers.common['Authorization'] = `Token ${token}`
      } else {
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
      }
    },

    // 设置用户信息
    setUser(user) {
      this.user = user
    },

    // 用户登录
    async login(credentials) {
      this.isLoading = true
      try {
        const response = await axios.post('/accounts/api/login/', credentials)
        const { token, user } = response.data
        
        this.setToken(token)
        this.setUser(user)
        
        return { success: true, data: response.data }
      } catch (error) {
        const message = error.response?.data?.message || '登录失败'
        return { success: false, message }
      } finally {
        this.isLoading = false
      }
    },

    // 用户注册
    async register(userData) {
      this.isLoading = true
      try {
        const response = await axios.post('/accounts/api/register/', userData)
        return { success: true, data: response.data }
      } catch (error) {
        console.log('注册API错误:', error)
        console.log('错误响应数据:', error.response?.data)
        
        let message = '注册失败'
        
        if (error.response?.data) {
          const errorData = error.response.data
          
          // 处理字段级别的错误
          if (typeof errorData === 'object' && !errorData.message) {
            const fieldErrors = []
            for (const [field, errors] of Object.entries(errorData)) {
              if (Array.isArray(errors)) {
                fieldErrors.push(`${this.getFieldName(field)}: ${errors[0]}`)
              } else if (typeof errors === 'string') {
                fieldErrors.push(`${this.getFieldName(field)}: ${errors}`)
              }
            }
            if (fieldErrors.length > 0) {
              message = fieldErrors.join('; ')
            }
          } else if (errorData.message) {
            message = errorData.message
          } else if (typeof errorData === 'string') {
            message = errorData
          }
        }
        
        console.log('最终错误信息:', message)
        return { success: false, message }
      } finally {
        this.isLoading = false
      }
    },
    
    // 获取字段中文名称
    getFieldName(field) {
      const fieldNames = {
        'username': '用户名',
        'real_name': '真实姓名',
        'phone': '手机号',
        'email': '邮箱',
        'password': '密码',
        'user_type': '用户类型'
      }
      return fieldNames[field] || field
    },

    // 用户登出
    async logout() {
      try {
        if (this.token) {
          await axios.post('/accounts/api/logout/')
        }
      } catch (error) {
        console.error('登出请求失败:', error)
      } finally {
        this.setToken(null)
        this.setUser(null)
      }
    },

    // 获取用户资料
    async fetchProfile() {
      if (!this.token) return
      
      try {
        const response = await axios.get('/accounts/api/profile/')
        this.setUser(response.data.user)
        return { success: true, data: response.data }
      } catch (error) {
        const message = error.response?.data?.message || '获取用户信息失败'
        return { success: false, message }
      }
    },

    // 更新用户资料
    async updateProfile(profileData) {
      this.isLoading = true
      try {
        const response = await axios.put('/accounts/api/profile/', profileData)
        this.setUser(response.data.user)
        return { success: true, data: response.data }
      } catch (error) {
        const message = error.response?.data?.message || '更新资料失败'
        return { success: false, message }
      } finally {
        this.isLoading = false
      }
    },

    // 初始化用户状态
    async initializeAuth() {
      // 从localStorage恢复token
      const storedToken = localStorage.getItem('token')
      if (storedToken) {
        this.token = storedToken
        axios.defaults.headers.common['Authorization'] = `Token ${storedToken}`
        await this.fetchProfile()
      }
    }
  }
})