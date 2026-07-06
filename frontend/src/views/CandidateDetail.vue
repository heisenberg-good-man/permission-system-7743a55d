<template>
  <div class="candidate-detail-page">
    <button class="btn-back" @click="$router.go(-1)">← 返回</button>
    <div class="candidate-header" v-if="candidate">
      <div class="candidate-icon">👤</div>
      <div class="candidate-basic">
        <h1>{{ candidate.name }}</h1>
        <div class="candidate-meta">
          <span>{{ candidate.email }}</span>
          <span>{{ candidate.phone }}</span>
          <span>{{ candidate.status === 'active' ? '活跃' : '已停用' }}</span>
        </div>
      </div>
    </div>
    <div class="content-grid" v-if="candidate">
      <div class="left-panel">
        <div class="card">
          <h2>📋 个人信息</h2>
          <div class="info-grid">
            <div class="info-item">
              <label>学历</label>
              <span>{{ candidate.education }}</span>
            </div>
            <div class="info-item">
              <label>工作经验</label>
              <span>{{ candidate.experience }}</span>
            </div>
            <div class="info-item">
              <label>期望城市</label>
              <span>{{ candidate.desired_city }}</span>
            </div>
            <div class="info-item">
              <label>期望岗位</label>
              <span>{{ candidate.desired_job }}</span>
            </div>
          </div>
        </div>
        <div class="card">
          <h2>💼 技能标签</h2>
          <div class="skills">
            <span v-for="skill in candidate.skills" :key="skill" class="skill-tag">{{ skill }}</span>
          </div>
        </div>
        <div class="card">
          <h2>📄 简历摘要</h2>
          <div class="resume-content">
            <pre>{{ candidate.resume }}</pre>
          </div>
        </div>
      </div>
      <div class="right-panel">
        <div class="card">
          <h2>📝 投递记录</h2>
          <div class="applications-list" v-if="applications.length > 0">
            <div v-for="app in applications" :key="app.id" class="app-item" @click="$router.push(`/applications/${app.id}`)">
              <div class="app-header">
                <span class="app-job">{{ getJobTitle(app.job_id) }}</span>
                <span class="app-status" :class="app.status">{{ getStatusText(app.status) }}</span>
              </div>
              <div class="app-meta">
                <span>投递时间：{{ formatDate(app.created_at) }}</span>
              </div>
              <div class="app-arrow">→</div>
            </div>
          </div>
          <div class="empty-apps" v-else>
            <div class="empty-icon">📭</div>
            <div class="empty-text">暂无投递记录</div>
          </div>
        </div>
      </div>
    </div>
    <div class="loading" v-if="loading">
      <div class="spinner"></div>
      <div class="loading-text">加载中...</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { candidatesApi, applicationsApi, jobsApi } from '../api'

const route = useRoute()
const candidate = ref(null)
const applications = ref([])
const jobs = ref({})
const loading = ref(true)

const getJobTitle = (jobId) => {
  return jobs.value[jobId]?.title || jobId
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': '待处理',
    'reviewing': '审核中',
    'interview': '面试中',
    'offer': '已发Offer',
    'rejected': '已拒绝'
  }
  return statusMap[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const loadData = async () => {
  try {
    loading.value = true
    const [candidateRes, appsRes] = await Promise.all([
      candidatesApi.getCandidate(route.params.id),
      applicationsApi.getApplications({ candidate_id: route.params.id })
    ])
    candidate.value = candidateRes.data
    applications.value = appsRes.data
    
    const jobIds = [...new Set(applications.value.map(a => a.job_id))]
    const jobPromises = jobIds.map(id => jobsApi.getJob(id))
    const jobResults = await Promise.all(jobPromises)
    jobResults.forEach(res => {
      jobs.value[res.data.id] = res.data
    })
  } catch (error) {
    console.error('Failed to load data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.candidate-detail-page {
  padding: 20px 0;
}
.btn-back {
  padding: 10px 20px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  margin-bottom: 20px;
  transition: all 0.2s;
}
.btn-back:hover {
  background: #f5f5f5;
}
.candidate-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 32px;
  padding: 24px;
  background: white;
  border-radius: 12px;
}
.candidate-icon {
  font-size: 64px;
}
.candidate-basic h1 {
  font-size: 28px;
  margin-bottom: 8px;
}
.candidate-meta {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #666;
}
.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}
.card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 20px;
}
.card h2 {
  font-size: 18px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.info-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.info-item label {
  font-size: 13px;
  color: #999;
}
.info-item span {
  font-size: 14px;
  font-weight: 500;
}
.skills {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.skill-tag {
  font-size: 13px;
  padding: 6px 14px;
  background: #f0f5ff;
  color: #667eea;
  border-radius: 20px;
}
.resume-content {
  background: #fafafa;
  padding: 16px;
  border-radius: 8px;
  max-height: 400px;
  overflow-y: auto;
}
.resume-content pre {
  font-size: 14px;
  line-height: 1.8;
  color: #333;
  white-space: pre-wrap;
  font-family: inherit;
}
.applications-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.app-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.app-item:hover {
  background: #f0f5ff;
}
.app-header {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.app-job {
  font-size: 15px;
  font-weight: 600;
}
.app-status {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 12px;
}
.app-status.pending {
  background: #fff3e0;
  color: #ff9800;
}
.app-status.reviewing {
  background: #e3f2fd;
  color: #2196f3;
}
.app-status.interview {
  background: #e8f5e9;
  color: #4caf50;
}
.app-status.offer {
  background: #fce4ec;
  color: #e91e63;
}
.app-status.rejected {
  background: #f5f5f5;
  color: #999;
}
.app-meta {
  font-size: 12px;
  color: #999;
}
.app-arrow {
  font-size: 20px;
  color: #ccc;
  margin-left: 12px;
}
.empty-apps {
  text-align: center;
  padding: 40px 20px;
}
.empty-icon {
  font-size: 40px;
  margin-bottom: 12px;
}
.empty-text {
  font-size: 14px;
  color: #999;
}
.loading {
  text-align: center;
  padding: 80px 20px;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.loading-text {
  font-size: 14px;
  color: #999;
}
</style>