import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/Main.vue'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Tasks from '../views/Tasks.vue'
import Task from '../views/Task.vue'
import Profile from '../views/Profile.vue'
import Session from '../views/Session.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', component: Login},
  { path: '/login', component: Login},
  {
      path: '/main',
      component: Main,
      children: [
        { 
          path: '/home', component: Home
        },
        { 
          path: '/tasks', component: Tasks
        },
        { 
          path: '/task', component: Task
        },
        { 
          path: '/profile', component: Profile
        },
        { 
          path: '/session/:type', component: Session
        },
      ],
  },
];


const router = new VueRouter({
  routes
})

export default router
