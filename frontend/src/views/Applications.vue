<template>
  <div class="applications-page">
    <div class="page-header">
      <h1>投递记录</h1>
      <p>查看所有简历投递情况</p>
    </div>
    <div class="filters">
      <select v-model="statusFilter">
        <option value="">全部状态</option>
        <option value="pending">待处理</option>
        <option value="communicating">已沟通</option>
        <option value="interviewing">面试中</option>
        <option value="rejected">已拒绝</option>
        <option value="hired">已录用</option>
      </select>
    </div>
    <div class="stats-row">
      <div class="stat-item">
        <span class="stat-num">{{ applications.length }}</span>
        <span class="stat-label">总投递</span>
      </div>
      <div class="stat-item">
        <span class="stat-num pending">{{ getCount('pending') }}</span>
        <span class="stat-label">待处理</span>
      </div>
      <div class="stat-item">
        <span class="stat-num communicating">{{ getCount('communicating') }}</span>
        <span class="stat-label">已沟通</span>
      </div>
      <div class="stat-item">
        <span class="stat-num interviewing">{{ getCount('interviewing') }}</span>
        <span class="stat-label">面试中</span>
      </div>
    </div>
    <div class="application-list">
      <div class="application-card" v-for="app in filteredApplications" :key="app.id" @click="$router.push(`/applications/${app.id}`)">
        <div class="app-header">
          <div class="app-info">
            <div class="job-title">{{ getJob(app.job_id)?.title || '未知职位' }}</div>
            <div class="company-name">{{ getJob(app.job_id)?.company || '未知公司' }}</div>
          </div>
          <div class="app-status" :class="app.status">{{ getStatusText(app.status) }}</div>
        </div>
        <div class="app-candidate">
          <span class="candidate-icon">👤</span>
          <span>{{ getCandidate(app.candidate_id)?.name || '未知候选人' }}</span>
          <span class="candidate-email">{{ getCandidate(app.candidate_id)?.email }}</span>
        </div>
        <div class="app-meta">
          <span>投递于 {{ formatDate(app.applied_at) }}</span>
          <span>更新于 {{ formatDate(app.updated_at) }}</span>
        </div>
        <div class="app-cover">
          {{ app.cover_letter }}
        </div>
      </div>
    </div>
    <div class="empty-state" v-if="filteredApplications.length === 0">
      <div class="empty-icon">📋</div>
      <div class="empty-text">暂无投递记录</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { applicationsApi, jobsApi, candidatesApi } from '../api'

const applications = ref([])
const jobs = ref([])
const candidates = ref([])
const statusFilter = ref('')

const filteredApplications = computed(() => {
  if (!statusFilter.value) return applications.value
  return applications.value.filter(app => app.status === statusFilter.value)
})

const getCount = (status) => {
  return applications.value.filter(app => app.status === status).length
}

const getJob = (jobId) => {
  return jobs.value.find(j => j.id === jobId)
}

const getCandidate = (candidateId) => {
  return candidates.value.find(c => c.id === candidateId)
}

const getStatusText = (status) => {
  const map = {
    pending: '待处理',
    communicating: '已沟通',
    interviewing: '面试中',
    rejected: '已拒绝',
    hired: '已录用'
  }
  return map[status] || status
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`
}

const loadData = async () => {
  try {
    const [appsRes, jobsRes, candidatesRes] = await Promise.all([
      applicationsApi.getApplications(),
      jobsApi.getJobs(),
      candidatesApi.getCandidates()
    ])
    applications.value = appsRes.data
    jobs.value = jobsRes.data
    candidates.value = candidatesRes.data
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.applications-page {
  padding: 20px 0;
}
.page-header {
  margin-bottom: 32px;
}
.page-header h1 {
  font-size: 32px;
  margin-bottom: 8px;
}
.page-header p {
  font-size: 16px;
  color: #999;
}
.filters {
  margin-bottom: 20px;
}
.filters select {
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}
.stats-row {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}
.stat-item {
  background: white;
  padding: 16px 24px;
  border-radius: 10px;
  display: flex;
  align-items: baseline;
  gap: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.stat-num {
  font-size: 24px;
  font-weight: bold;
  color: #667eea;
}
.stat-num.pending { color: #ff9800; }
.stat-num.communicating { color: #2196f3; }
.stat-num.interviewing { color: #4caf50; }
.stat-label {
  font-size: 14px;
  color: #999;
}
.application-list {
  display: grid;
  gap: 20px;
}
.application-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.application-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}
.job-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}
.company-name {
  font-size: 14px;
  color: #666;
}
.app-status {
  font-size: 12px;
  padding: 6px 14px;
  border-radius: 20px;
}
.app-status.pending {
  background: #fff3e0;
  color: #ff9800;
}
.app-status.communicating {
  background: #e3f2fd;
  color: #2196f3;
}
.app-status.interviewing {
  background: #e8f5e9;
  color: #4caf50;
}
.app-status.rejected {
  background: #ffebee;
  color: #d32f2f;
}
.app-status.hired {
  background: #f3e5f5;
  color: #9c27b0;
}
.app-candidate {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  padding: 12px;
  background: #fafafa;
  border-radius: 8px;
}
.candidate-icon {
  font-size: 24px;
}
.app-candidate span:nth-child(2) {
  font-weight: 500;
}
.candidate-email {
  font-size: 14px;
  color: #999;
}
.app-meta {
  display: flex;
  gap: 20px;
  font-size: 12px;
  color: #bbb;
  margin-bottom: 12px;
}
.app-cover {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
}
.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}
.empty-text {
  font-size: 16px;
  color: #999;
}
</style>