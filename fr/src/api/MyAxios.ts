import axios from "axios";

const headers = {};

axios.defaults.headers.post["Content-Type"] = "application/json";
axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";
axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL ?? '/chitchat/api'
axios.defaults.timeout = 30000

export const my_get = async (url: string, data: object): Promise<any> => {
  try {
    return await axios.get(url, { params: data, headers });
  } catch (err) {
    return err;
  }
};

export const my_post = async (url: string, data: object): Promise<any> => {
  return await axios
    .post(url, data, { headers })
    .then((res) => res)
    .catch((err) => err);
};

//添加请求拦截器
axios.interceptors.request.use(
  (config) => {

    config.headers.Authorization = `Bearer ${localStorage.getItem("user_id")}`

    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// 添加响应拦截器
axios.interceptors.response.use(
  (response) => {

    return response.data;
  },
  (error) => {
    return Promise.reject(error.response.data);
  },
);
