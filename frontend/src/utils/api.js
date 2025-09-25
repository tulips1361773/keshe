import axios from './axios'

// API接口封装
const api = {
  // GET请求
  get(url, config = {}) {
    return axios.get(url, config)
  },

  // POST请求
  post(url, data = {}, config = {}) {
    return axios.post(url, data, config)
  },

  // PUT请求
  put(url, data = {}, config = {}) {
    return axios.put(url, data, config)
  },

  // PATCH请求
  patch(url, data = {}, config = {}) {
    return axios.patch(url, data, config)
  },

  // DELETE请求
  delete(url, config = {}) {
    return axios.delete(url, config)
  },

  // 文件上传
  upload(url, formData, config = {}) {
    return axios.post(url, formData, {
      ...config,
      headers: {
        'Content-Type': 'multipart/form-data',
        ...config.headers
      }
    })
  }
}

export default api