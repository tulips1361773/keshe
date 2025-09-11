// 错误处理工具类

/**
 * 统一的错误处理函数
 * @param {Error} error - 错误对象
 * @param {string} context - 错误上下文
 * @param {boolean} showMessage - 是否显示用户提示
 */
export const handleError = (error, context = '', showMessage = true) => {
  // 记录错误日志
  console.error(`[${context}] 错误:`, error)
  
  // 错误上报（可以集成第三方错误监控服务）
  if (process.env.NODE_ENV === 'production') {
    // 这里可以集成 Sentry 等错误监控服务
    // Sentry.captureException(error, { tags: { context } })
  }
  
  if (!showMessage) return
  
  // 根据错误类型显示不同的用户提示
  const { ElMessage } = require('element-plus')
  
  if (error.name === 'NetworkError' || error.message?.includes('fetch')) {
    ElMessage.error('网络连接失败，请检查网络后重试')
  } else if (error.name === 'ValidationError') {
    ElMessage.warning('请检查输入信息是否正确')
  } else if (error.status === 401) {
    ElMessage.error('登录已过期，请重新登录')
  } else if (error.status === 403) {
    ElMessage.error('没有权限执行此操作')
  } else if (error.status === 404) {
    ElMessage.error('请求的资源不存在')
  } else if (error.status === 500) {
    ElMessage.error('服务器内部错误，请稍后重试')
  } else {
    ElMessage.error(error.message || '操作失败，请稍后重试')
  }
}

/**
 * API 响应错误处理
 * @param {Response} response - fetch 响应对象
 * @param {string} context - 错误上下文
 */
export const handleApiError = async (response, context = '') => {
  const { ElMessage } = require('element-plus')
  
  try {
    const error = await response.json()
    
    if (response.status === 400) {
      if (error.non_field_errors) {
        ElMessage.error(error.non_field_errors[0])
      } else if (error.detail) {
        ElMessage.error(error.detail)
      } else {
        // 处理字段级错误
        const fieldErrors = []
        Object.keys(error).forEach(field => {
          if (Array.isArray(error[field])) {
            fieldErrors.push(`${getFieldLabel(field)}: ${error[field][0]}`)
          }
        })
        
        if (fieldErrors.length > 0) {
          ElMessage.error(fieldErrors.join('; '))
        } else {
          ElMessage.error('请检查输入信息')
        }
      }
    } else if (response.status === 401) {
      ElMessage.error('登录已过期，请重新登录')
      // 可以在这里触发重新登录逻辑
    } else if (response.status === 403) {
      ElMessage.error('没有权限执行此操作')
    } else if (response.status === 404) {
      ElMessage.error('请求的资源不存在')
    } else if (response.status === 409) {
      ElMessage.error('操作冲突，请刷新页面后重试')
    } else if (response.status >= 500) {
      ElMessage.error('服务器错误，请稍后重试')
    } else {
      ElMessage.error(error.error || error.message || '操作失败')
    }
    
    console.error(`[${context}] API错误:`, {
      status: response.status,
      url: response.url,
      error
    })
  } catch (parseError) {
    console.error(`[${context}] 解析错误响应失败:`, parseError)
    ElMessage.error('服务器响应异常')
  }
}

/**
 * 获取字段标签的辅助函数
 * @param {string} field - 字段名
 */
const getFieldLabel = (field) => {
  const labelMap = {
    // 用户相关
    username: '用户名',
    password: '密码',
    email: '邮箱',
    phone: '手机号',
    real_name: '真实姓名',
    
    // 预约相关
    relation_id: '师生关系',
    campus_id: '校区',
    table_id: '球台',
    start_time: '开始时间',
    end_time: '结束时间',
    total_fee: '预约费用',
    notes: '备注',
    reason: '原因',
    
    // 通用
    name: '名称',
    description: '描述',
    status: '状态'
  }
  return labelMap[field] || field
}

/**
 * 日志记录工具
 */
export const logger = {
  info: (message, data = null) => {
    console.log(`[INFO] ${message}`, data)
  },
  
  warn: (message, data = null) => {
    console.warn(`[WARN] ${message}`, data)
  },
  
  error: (message, error = null) => {
    console.error(`[ERROR] ${message}`, error)
  },
  
  debug: (message, data = null) => {
    if (process.env.NODE_ENV === 'development') {
      console.debug(`[DEBUG] ${message}`, data)
    }
  }
}

/**
 * 性能监控工具
 */
export const performance = {
  start: (label) => {
    if (process.env.NODE_ENV === 'development') {
      console.time(label)
    }
  },
  
  end: (label) => {
    if (process.env.NODE_ENV === 'development') {
      console.timeEnd(label)
    }
  }
}