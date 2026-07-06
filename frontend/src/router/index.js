import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import JobList from '../views/JobList.vue'
import JobDetail from '../views/JobDetail.vue'
import JobCreate from '../views/JobCreate.vue'
import JobManage from '../views/JobManage.vue'
import Applications from '../views/Applications.vue'
import ApplicationDetail from '../views/ApplicationDetail.vue'
import CandidateList from '../views/CandidateList.vue'
import CandidateDetail from '../views/CandidateDetail.vue'
import InterviewList from '../views/InterviewList.vue'
import InterviewDetail from '../views/InterviewDetail.vue'
import Profile from '../views/Profile.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/jobs', name: 'JobList', component: JobList },
  { path: '/jobs/:id', name: 'JobDetail', component: JobDetail },
  { path: '/jobs/create', name: 'JobCreate', component: JobCreate },
  { path: '/jobs/manage', name: 'JobManage', component: JobManage },
  { path: '/applications', name: 'Applications', component: Applications },
  { path: '/applications/:id', name: 'ApplicationDetail', component: ApplicationDetail },
  { path: '/candidates', name: 'CandidateList', component: CandidateList },
  { path: '/candidates/:id', name: 'CandidateDetail', component: CandidateDetail },
  { path: '/interviews', name: 'InterviewList', component: InterviewList },
  { path: '/interviews/:id', name: 'InterviewDetail', component: InterviewDetail },
  { path: '/profile', name: 'Profile', component: Profile }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router