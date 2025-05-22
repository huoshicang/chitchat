import axios from "axios";


const instance = axios.create({
  baseURL: import.meta.env.VITE_APP_API_URL ?? '/chitchat/api',
  timeout: 30000,
});


// 添加请求拦截器（关键修改）
instance.interceptors.request.use(async (config) => {
  config.headers.Authorization = `Bearer ${localStorage.getItem("user_id")}`
  return config;
}, (error) => {
  return Promise.reject(error);
});


// 响应拦截器
instance.interceptors.response.use(
  (response) => {
    // 成功响应处理（HTTP 200 系列）
    const {status_code, data, message} = response.data
    return {status_code, data, message}
  },
  (error) => {
    // 错误处理（网络错误或 HTTP 非 200 状态码）
    let errorMessage = '请求异常'

    if (error.response) {
      // 服务器返回了响应但状态码不在 2xx 范围
      const {status, data} = error.response
      errorMessage = data?.message || `服务器错误 (${status})`
    } else if (error.request) {
      // 请求已发出但没有收到响应
      errorMessage = '网络连接异常'
    }

    // 显示错误提示（可根据需要配置静默模式）
    if (!error.config?.silent) {
      window.$message.warning(errorMessage)
    }

    // 统一错误格式
    const formattedError: UnifiedResponse = {
      isError: true,
      message: errorMessage,
      result: error.response?.data
        ? {
          status_code: error.response.status,
          data: error.response.data,
          message: errorMessage
        }
        : undefined
    }

    // 保持错误拒绝状态，但携带统一格式
    return Promise.reject(formattedError)
  }
)


//export default instance;
//
