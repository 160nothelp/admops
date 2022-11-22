import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import './assets/css/main.css'
import axios from 'axios'

// 全局请求拦截器，只要发起异步请求都要带上这个token
axios.interceptors.request.use(config => {
    config.headers.Authorization = 'Bearer ' +
        window.localStorage.getItem('token')
    return config
})
// 响应拦截器，只要有错误码小于100都和登录有关，要求重新登录
axios.interceptors.response.use(function (response) {
    // 对响应数据做点什么
    if (response.data.code && response.data.code < 100) {
        window.localStorage.removeItem('token')
        router.push('/login')
        return response
    } else {
        return response
    }
})
// axios全局设置，baseURL指向后台服务
axios.defaults.baseURL = '/api/v1/'
// 为Vue类增加全局属性$http，这样所有组件实例都可以使用该属性了
Vue.prototype.$http = axios
Vue.config.productionTip = false

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
