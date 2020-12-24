import axios from 'axios'

import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import { getToken, getOperator } from '@/utils/auth'
const JSONBig = require('json-bigint')({ 'storeAsString': true })
// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000, // request timeout
  transformResponse: [function transformResponse(data) {
    /*eslint no-param-reassign:0*/
    return JSONBig.parse(data)
  }]
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent

    if (store.getters.token) {
      // 请求自动添加header的token
      config.headers['Authorization'] = 'Bearer ' + getToken()
    }
    if (store.getters.operator) {
      config.headers['operator'] = getOperator()
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
   */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const res = response.data
    // 请求成功都是200
    if (response.status !== 200) {
      Message({
        message: res.message || 'Error',
        type: 'error',
        duration: 5 * 1000
      })
      return Promise.reject(new Error(res.message || 'Error'))
    } else {
      return res
    }
  },
  error => {
    // console.log(JSON.stringify(error))
    // console.log('err' + error) // for debug
    if (error.response.status === 401) {
    // 401登陆超时
      MessageBox.confirm('登陆超时,请重新登陆', '您已登出', {
        confirmButtonText: '重新登陆',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        store.dispatch('user/resetToken').then(() => {
          location.reload()
        })
      })
      return Promise.resolve('登陆异常已处理')
    }
    // 406帐号密码错误或未激活
    if (error.response.status === 406) {
      Message({
        message: error.response.data.detail,
        type: 'error',
        duration: 5 * 1000
      })
      return Promise.reject('登陆异常已处理')
    }
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
