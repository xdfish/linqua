import Vue from 'vue'
import VueRouter from 'vue-router'

import Main from '../views/Main.vue'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Profile from '../views/Profile.vue'
import Tasks from '../views/Tasks.vue'
import Task from '../views/Task.vue'
import Words from '../views/Words.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', component: Login},
  { path: '/login', component: Login},
  {
      path: '/main',
      component: Main,
      children: [
        { 
          path: '/home', component: Home, name: 'home'
        },
        { 
          path: '/tasks', component: Tasks, name: 'tasks'
        },
        { 
          path: '/task', component: Task, props: true, name: 'task'
        },
        { 
          path: '/profile', component: Profile, name: 'profile'
        },
        { 
          path: '/words', component: Words, name: 'words'
        },
      ],
  },
];


const router = new VueRouter({
  routes
})

export default router
