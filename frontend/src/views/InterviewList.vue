<template>
  <div class="interview-list-page">
    <div class="page-header">
      <h1>面试管理</h1>
      <p>查看和管理面试安排</p>
    </div>
    <div class="stats-bar">
      <div class="stat-item">
        <div class="stat-value">{{ stats.total || 0 }}</div>
        <div class="stat-label">总面试</div>
      </div>
      <div class="stat-item">
        <div class="stat-value pending">{{ stats.pending || 0 }}</div>
        <div class="stat-label">待安排</div>
      </div>
      <div class="stat-item">
        <div class="stat-value scheduled">{{ stats.scheduled || 0 }}</div>
        <div class="stat-label">已安排</div>
      </div>
      <div class="stat-item">
        <div class="stat-value completed">{{ stats.completed || 0 }}</div>
        <div class="stat-label">已完成</div>
      </div>
    </div>
    <div class="filters">
      <div class="filter-item">
        <label>状态</label>
        <select v-model="filters.status" @change="loadInterviews">
          <option value="">全部状态</option>
          <option value="pending">待安排</option>
          <option value="scheduled">已安排</option>
          <option value="completed">已完成</option>
          <option value="cancelled">已取消</option>
        </select>
      </div>
    </div>
    <div class="results-info">
      共 {{ interviews.length }} 场面试
    </div>
    <div class="interview-list">
      <div v-for="interview in interviews" :key="interview.id" class="interview-card" @click="$router.push(`/interviews/${interview.id}`)">
        <div class="card-header">
          <div class="interview-info">
            <div class="interview-title">
              <span class="round-badge">{{ interview.round }}</span>
              <span class="job-title">{{ getJobTitle(interview.application_id) }}</span>
            </div>
            <div class="interview-meta">
              <span class="method">📹 {{ getMethodText(interview.method) }}</span>
              <span class="time">🕐 {{ formatDateTime(interview.time) }}</span>
            </div>
          </div>
          <span class="status-badge" :class="interview.status">{{ getStatusText(interview.status) }}</span>
        </div>
        <div class="card-body">
          <div class="participants">
            <span>👤 {{ getCandidateName(interview.application_id) }}</span>
            <span>🧑‍💼 {{ interview.interviewer }}</span>
          </div>
          <div class="location">📍 {{ interview.location }}</div>
          <div class="notes" v-if="interview.notes">{{ interview.notes }}</div>
        </div>
        <div class="card-footer">
          <span class="created-time">创建于 {{ formatDate(interview.created_at) }}</span>
          <span class="arrow">→</span>
        </div>
      </div>
    </div>
    <div class="empty-state" v-if="interviews.length === 0">
      <div class="empty-icon">📅</div>
      <div class="empty-text">暂无面试安排</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { interviewsApi, applicationsApi, jobsApi, candidatesApi, statsApi } from '../api'

const interviews = ref([])
const applications = ref({})
const jobs = ref({})
const candidates = ref({})
const filters = ref({
  status: ''
})

const stats = computed(() => {
  return {
    total: interviews.value.length,
    pending: interviews.value.filter(i => i.status === 'pending').length,
    scheduled: interviews.value.filter(i => i.status === 'scheduled').length,
    completed: interviews.value.filter(i => i.status === 'completed').length
  }
})

const getJobTitle = (appId) => {
  return jobs.value[appId] || appId
}

const getCandidateName = (appId) => {
  return candidates.value[appId] || appId
}

const getMethodText = (method) => {
  const map = {
    '视频面试': '视频面试',
    '现场面试': '现场面试',
    '电话面试': '电话面试'
  }
  return map[method] || method
}

const getStatusText = (status) => {
  const map = {
    'pending': '待安排',
    'scheduled': '已安排',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return map[status] || status
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const loadInterviews = async () => {
  try {
    const params = {}
    if (filters.value.status) params.status = filters.value.status
    const res = await interviewsApi.getInterviews(params)
    interviews.value = res.data
    
    const appIds = [...new Set(interviews.value.map(i => i.application_id))]
    const appPromises = appIds.map(id => applicationsApi.getApplication(id))
    const appResults = await Promise.all(appPromises)
    appResults.forEach(res => {
      applications.value[res.data.id] = res.data
    })
    
    const jobIds = [...new Set(appResults.map(r => r.data.job_id))]
    const jobPromises = jobIds.map(id => jobsApi.getJob(id))
    const jobResults = await Promise.all(jobPromises)
    jobResults.forEach(res => {
      jobs.value[res.data.id] = res.data.title
    })
    
    const candidateIds = [...new Set(appResults.map(r => r.data.candidate_id))]
    const candidatePromises = candidateIds.map(id => candidatesApi.getCandidate(id))
    const candidateResults = await Promise.all(candidatePromises)
    candidateResults.forEach(res => {
      candidates.value[res.data.id] = res.data.name
    })
    
    appIds.forEach(appId => {
      const app = applications.value[appId]
      if (app) {
        jobs.value[appId] = jobs.value[app.job_id]
        candidates.value[appId] = candidates.value[app.candidate_id]
      }
    })
  } catch (error) {
    console.error('Failed to load interviews:', error)
  }
}

onMounted(() => {
  loadInterviews()
})
</script>

<style scoped>
.interview-list-page {
  padding: 20px 0;
}
.page-header {
  margin-bottom: 24px;
}
.page-header h1 {
  font-size: 32px;
  margin-bottom: 8px;
}
.page-header p {
  font-size: 16px;
  color: #999;
}
.stats-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.stat-item {
  background: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}
.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #333;
}
.stat-value.pending {
  color: #ff9800;
}
.stat-value.scheduled {
  color: #2196f3;
}
.stat-value.completed {
  color: #4caf50;
}
.stat-label {
  font-size: 14px;
  color: #999;
  margin-top: 4px;
}
.filters {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}
.filter-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.filter-item label {
  font-size: 13px;
  font-weight: 500;
}
.filter-item select {
  padding: 8px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 13px;
}
.results-info {
  font-size: 14px;
  color: #999;
  margin-bottom: 16px;
}
.interview-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.interview-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.interview-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}
.interview-title {
  display: flex;
  align-items: center;
  gap: 10px;
}
.round-badge {
  font-size: 12px;
  padding: 4px 10px;
  background: #f0f5ff;
  color: #667eea;
  border-radius: 4px;
}
.job-title {
  font-size: 18px;
  font-weight: 600;
}
.interview-meta {
  display: flex;
  gap: 20px;
  margin-top: 8px;
}
.interview-meta span {
  font-size: 14px;
  color: #666;
}
.status-badge {
  font-size: 12px;
  padding: 6px 14px;
  border-radius: 20px;
}
.status-badge.pending {
  background: #fff3e0;
  color: #ff9800;
}
.status-badge.scheduled {
  background: #e3f2fd;
  color: #2196f3;
}
.status-badge.completed {
  background: #e8f5e9;
  color: #4caf50;
}
.status-badge.cancelled {
  background: #f5f5f5;
  color: #999;
}
.card-body {
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}
.participants {
  display: flex;
  gap: 20px;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}
.location {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}
.notes {
  font-size: 13px;
  color: #666;
  padding: 10px 14px;
  background: #fafafa;
  border-radius: 6px;
  max-height: 60px;
  overflow-y: auto;
}
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}
.created-time {
  font-size: 12px;
  color: #999;
}
.arrow {
  font-size: 20px;
  color: #ccc;
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