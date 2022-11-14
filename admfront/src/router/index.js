import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/LoginView.vue'
import Home from '../views/HomeView.vue'
import Welcome from '../views/WelcomeView.vue'
import User from '../views/user/UserView'
import Perm from '../views/user/PermView'
import Role from '../views/user/RoleView'

Vue.use(VueRouter)

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch((err) => err)
}

const routes = [
    {path: '/', redirect: '/login'},
    {path: '/login', component: Login},
    {
        path: '/home',
        component: Home,
        redirect: '/welcome', // 访问/home重定向到/welcome，进入子路由
        children: [
            {path: '/welcome', component: Welcome},
            {path: '/users', component: User},
            {path: '/users/perms', component: Perm},
            {path: '/users/roles', component: Role},
        ]
    }
]

const router = new VueRouter({
    routes
})

// 挂载全局导航守卫
router.beforeEach((to, from, next) => {
    // from从哪里来，to去哪里，next函数跳转
    // 只要不是登录页，都要查看token
    if (to.path === '/login') {
        const token = window.localStorage.getItem('token')
        if (!token) {
            next()
        }else {
            next('/home')
        }
    } else {
        // 读取token
        const token = window.localStorage.getItem('token')
        if (!token) {
            next('/login')
        } else {
            next()
        }
    }
})

export default router
