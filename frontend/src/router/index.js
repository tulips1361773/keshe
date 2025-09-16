import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 路由组件
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Dashboard from '@/views/Dashboard.vue'
import Profile from '@/views/Profile.vue'
import Courses from '@/views/Courses.vue'
import CourseDetail from '@/views/CourseDetail.vue'
import Reservations from '@/views/Reservations.vue'
import Payments from '@/views/Payments.vue'
import Evaluations from '@/views/Evaluations.vue'
import Notifications from '@/views/Notifications.vue'
import Competitions from '@/views/Competitions.vue'
import CompetitionDetail from '@/views/CompetitionDetail.vue'
import Coaches from '@/views/Coaches.vue'
import CoachDetail from '@/views/CoachDetail.vue'
import CoachChange from '@/views/CoachChange.vue'
import TeachingManagement from '@/components/TeachingManagement.vue'
import CoachSchedule from '@/components/CoachSchedule.vue'
import RechargeApproval from '@/views/RechargeApproval.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: '首页 - 乒乓球培训管理系统'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: '登录 - 乒乓球培训管理系统',
      requiresGuest: true
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      title: '注册 - 乒乓球培训管理系统',
      requiresGuest: true
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      title: '仪表板 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      title: '个人资料 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/courses',
    name: 'Courses',
    component: Courses,
    meta: {
      title: '课程管理 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/courses/:id',
    name: 'CourseDetail',
    component: CourseDetail,
    meta: {
      title: '课程详情 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/reservations',
    name: 'Reservations',
    component: Reservations,
    meta: {
      title: '预约管理 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/payments',
    name: 'Payments',
    component: Payments,
    meta: {
      title: '支付管理 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/evaluations',
    name: 'Evaluations',
    component: Evaluations,
    meta: {
      title: '课程评价 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: Notifications,
    meta: {
      title: '消息通知 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/competitions',
    name: 'Competitions',
    component: Competitions,
    meta: {
      title: '比赛管理 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/competitions/:id',
    name: 'CompetitionDetail',
    component: CompetitionDetail,
    meta: {
      title: '比赛详情 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/coaches',
    name: 'Coaches',
    component: Coaches,
    meta: {
      title: '教练员中心 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/coaches/:id',
    name: 'CoachDetail',
    component: CoachDetail,
    meta: {
      title: '教练员详情 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/coach-change',
    name: 'CoachChange',
    component: CoachChange,
    meta: {
      title: '教练更换 - 乒乓球培训管理系统',
      requiresAuth: true
    }
  },
  {
    path: '/teaching-management',
    name: 'TeachingManagement',
    component: TeachingManagement,
    meta: {
      title: '教学管理 - 乒乓球培训管理系统',
      requiresAuth: true,
      requiresCoach: true
    }
  },
  {
    path: '/coach-schedule',
    name: 'CoachSchedule',
    component: CoachSchedule,
    meta: {
      title: '我的课表 - 乒乓球培训管理系统',
      requiresAuth: true,
      requiresCoach: true
    }
  },
  {
    path: '/recharge-approval',
    name: 'RechargeApproval',
    component: RechargeApproval,
    meta: {
      title: '充值审核 - 乒乓球培训管理系统',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      title: '页面未找到 - 乒乓球培训管理系统'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title || '乒乓球培训管理系统'
  
  const userStore = useUserStore()
  const isAuthenticated = userStore.isAuthenticated
  
  // 需要登录的页面
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }
  
  // 已登录用户访问登录/注册页面
  if (to.meta.requiresGuest && isAuthenticated) {
    next({ name: 'Dashboard' })
    return
  }
  
  // 需要教练权限的页面
  if (to.meta.requiresCoach && isAuthenticated) {
    const userType = userStore.user?.user_type
    if (!['coach', 'super_admin', 'campus_admin'].includes(userType)) {
      next({ name: 'Dashboard' })
      return
    }
  }
  
  // 需要管理员权限的页面
  if (to.meta.requiresAdmin && isAuthenticated) {
    const userType = userStore.user?.user_type
    if (!['super_admin', 'campus_admin'].includes(userType)) {
      next({ name: 'Dashboard' })
      return
    }
  }
  
  next()
})

export default router