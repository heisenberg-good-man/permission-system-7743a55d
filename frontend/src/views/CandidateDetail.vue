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
                <span>投递时间：{{ formatDate(app.applied_at) }}</span>
              </div>
              <div class="app-arrow">→</div>
            </div>
          </div>
          <div class="empty-apps" v-else>
            <div class="empty-icon">📭</div>
            <div class="empty-text">暂无投递记录</div>
          </div>
        </div>
        <div class="card">
          <h2>📅 面试记录</h2>
          <div class="interviews-list" v-if="interviews.length > 0">
            <div v-for="interview in interviews" :key="interview.id" class="interview-item" @click="$router.push(`/interviews/${interview.id}`)">
              <div class="interview-header">
                <span class="interview-round">{{ interview.round }}</span>
                <span class="interview-status" :class="interview.status">{{ getInterviewStatusText(interview.status) }}</span>
              </div>
              <div class="interview-meta">
                <span>👤 {{ interview.interviewer }}</span>
                <span>🕐 {{ formatDateTime(interview.time) }}</span>
              </div>
              <div class="interview-method">📹 {{ getMethodText(interview.method) }}</div>
              <div class="interview-arrow">→</div>
            </div>
          </div>
          <div class="empty-interviews" v-else>
            <div class="empty-icon">📅</div>
            <div class="empty-text">暂无面试记录</div>
          </div>
        </div>
        <div class="card">
          <div class="card-header">
            <h2>📋 Offer记录</h2>
            <button 
              v-if="applications.length > 0" 
              class="btn-create-offer" 
              @click="$router.push(`/offers/create?application_id=${applications[0].id}`)"
            >
              + 发放Offer
            </button>
          </div>
          <div class="offers-list" v-if="offers.length > 0">
            <div v-for="offer in offers" :key="offer.id" class="offer-item" @click="$router.push(`/offers/${offer.id}`)">
              <div class="offer-header">
                <span class="offer-title">{{ offer.position_title }}</span>
                <span class="offer-status" :class="offer.status">{{ getOfferStatusText(offer.status) }}</span>
              </div>
              <div class="offer-meta">
                <span>💰 {{ offer.salary_min }}K-{{ offer.salary_max }}K</span>
                <span>📅 {{ formatDate(offer.start_date) }}</span>
              </div>
              <div class="offer-arrow">→</div>
            </div>
          </div>
          <div class="empty-offers" v-else>
            <div class="empty-icon">📋</div>
            <div class="empty-text">暂无Offer记录</div>
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
import { candidatesApi, applicationsApi, jobsApi, interviewsApi, offersApi } from '../api'

const route = useRoute()
const candidate = ref(null)
const applications = ref([])
const jobs = ref({})
const interviews = ref([])
const offers = ref([])
const loading = ref(true)

const getJobTitle = (jobId) => {
  return jobs.value[jobId]?.title || jobId
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': '待处理',
    'communicating': '已沟通',
    'interviewing': '面试中',
    'rejected': '已拒绝',
    'hired': '已录用'
  }
  return statusMap[status] || status
}

const getInterviewStatusText = (status) => {
  const map = {
    'pending': '待安排',
    'scheduled': '已安排',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return map[status] || status
}

const getOfferStatusText = (status) => {
  const map = {
    'pending': '待确认',
    'accepted': '已接受',
    'rejected': '已拒绝',
    'withdrawn': '已撤回',
    'pending_onboarding': '待入职'
  }
  return map[status] || status
}

const getMethodText = (method) => {
  const map = {
    '视频面试': '视频面试',
    '现场面试': '现场面试',
    '电话面试': '电话面试'
  }
  return map[method] || method
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

const loadData = async () => {
  try {
    loading.value = true
    const [candidateRes, appsRes, interviewsRes, offersRes] = await Promise.all([
      candidatesApi.getCandidate(route.params.id),
      applicationsApi.getApplications({ candidate_id: route.params.id }),
      interviewsApi.getInterviews({ candidate_id: route.params.id }),
      offersApi.getOffers({ candidate_id: route.params.id })
    ])
    candidate.value = candidateRes.data
    applications.value = appsRes.data
    interviews.value = interviewsRes.data
    offers.value = offersRes.data
    
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
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}
.card-header h2 {
  font-size: 18px;
  margin: 0;
}
.btn-create-offer {
  padding: 8px 16px;
  background: #ff9800;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.2s;
}
.btn-create-offer:hover {
  background: #f57c00;
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
.app-status.communicating {
  background: #e3f2fd;
  color: #2196f3;
}
.app-status.interviewing {
  background: #e8f5e9;
  color: #4caf50;
}
.app-status.hired {
  background: #f3e5f5;
  color: #9c27b0;
}
.app-status.rejected {
  background: #ffebee;
  color: #d32f2f;
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
.interviews-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.interview-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.interview-item:hover {
  background: #f0f5ff;
}
.interview-header {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.interview-round {
  font-size: 12px;
  padding: 4px 10px;
  background: #f0f5ff;
  color: #667eea;
  border-radius: 4px;
}
.interview-status {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 12px;
}
.interview-status.pending {
  background: #fff3e0;
  color: #ff9800;
}
.interview-status.scheduled {
  background: #e3f2fd;
  color: #2196f3;
}
.interview-status.completed {
  background: #e8f5e9;
  color: #4caf50;
}
.interview-status.cancelled {
  background: #f5f5f5;
  color: #999;
}
.interview-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #666;
  margin-bottom: 4px;
}
.interview-method {
  font-size: 12px;
  color: #999;
}
.interview-arrow {
  font-size: 20px;
  color: #ccc;
  margin-left: 12px;
}
.empty-interviews {
  text-align: center;
  padding: 40px 20px;
}
.offers-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.offer-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.offer-item:hover {
  background: #fff8e1;
}
.offer-header {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.offer-title {
  font-size: 15px;
  font-weight: 600;
}
.offer-status {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 12px;
}
.offer-status.pending {
  background: #fff3e0;
  color: #ff9800;
}
.offer-status.accepted {
  background: #e8f5e9;
  color: #4caf50;
}
.offer-status.rejected {
  background: #ffebee;
  color: #d32f2f;
}
.offer-status.withdrawn {
  background: #f5f5f5;
  color: #999;
}
.offer-status.pending_onboarding {
  background: #f3e5f5;
  color: #9c27b0;
}
.offer-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #666;
}
.offer-arrow {
  font-size: 20px;
  color: #ccc;
  margin-left: 12px;
}
.empty-offers {
  text-align: center;
  padding: 40px 20px;
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