<template>
  <div class="offer-detail-page">
    <button class="btn-back" @click="$router.back()">← 返回列表</button>
    <div class="loading" v-if="loading">
      <div class="spinner"></div>
      <div class="loading-text">加载中...</div>
    </div>
    <div v-if="!loading">
      <div v-if="notFound" class="error-container">
        <div class="error-icon">❌</div>
        <div class="error-title">Offer不存在</div>
        <div class="error-message">该Offer记录已被删除或不存在</div>
        <button class="btn-back-home" @click="router.push('/offers')">返回Offer列表</button>
      </div>
      <div v-else-if="error" class="error-container">
        <div class="error-icon">⚠️</div>
        <div class="error-title">加载失败</div>
        <div class="error-message">{{ error }}</div>
        <button class="btn-retry" @click="loadData()">重新加载</button>
      </div>
      <div v-else>
        <div class="page-header">
          <h1>{{ isEdit ? '编辑Offer' : (currentMode === 'create' ? '创建Offer' : 'Offer详情') }}</h1>
          <p>{{ job?.title || '未关联职位' }} - {{ candidate?.name || '未关联候选人' }}</p>
        </div>
        <div class="related-error-banner" v-if="relatedDataError">
          <span class="related-error-icon">⚠️</span>
          <span class="related-error-text">{{ relatedDataError }}</span>
          <button class="related-error-retry" @click="loadData()">重新加载</button>
        </div>
        <div class="detail-container" v-if="currentMode === 'create' || offer">
        <div class="left-panel">
          <div class="section-card">
            <h3>Offer信息</h3>
            <div class="form-group">
              <label>职位名称</label>
              <input type="text" v-model="formData.position_title" :disabled="!isEdit && currentMode !== 'create'" placeholder="请输入职位名称" />
            </div>
            <div class="form-group">
              <label>薪资范围（K）</label>
              <div class="salary-input">
                <input type="number" v-model="formData.salary_min" :disabled="!isEdit && currentMode !== 'create'" placeholder="最低" />
                <span class="salary-separator">-</span>
                <input type="number" v-model="formData.salary_max" :disabled="!isEdit && currentMode !== 'create'" placeholder="最高" />
                <span class="salary-unit">K</span>
              </div>
            </div>
            <div class="form-group">
              <label>入职时间</label>
              <input type="datetime-local" v-model="formData.start_date" :disabled="!isEdit && currentMode !== 'create'" />
            </div>
            <div class="form-group">
              <label>备注</label>
              <textarea v-model="formData.notes" rows="4" :disabled="!isEdit && currentMode !== 'create'" placeholder="请输入Offer备注，如福利、奖金等信息"></textarea>
            </div>
          </div>
          <div class="section-card">
            <h3>关联信息</h3>
            <div class="info-row">
              <span class="label">职位</span>
              <span class="value">{{ job?.title || '未关联职位' }}</span>
            </div>
            <div class="info-row">
              <span class="label">公司</span>
              <span class="value">{{ job?.company || '未关联公司' }}</span>
            </div>
            <div class="info-row">
              <span class="label">候选人</span>
              <span class="value">{{ candidate?.name || '未关联候选人' }}</span>
            </div>
            <div class="info-row">
              <span class="label">投递状态</span>
              <span class="value">{{ getAppStatusText(application?.status) }}</span>
            </div>
            <div class="action-link" v-if="application?.id" @click="$router.push(`/applications/${application.id}`)">
              → 查看投递详情
            </div>
            <div class="action-link" v-if="offer?.interview_id" @click="$router.push(`/interviews/${offer.interview_id}`)">
              → 查看面试详情
            </div>
          </div>
          <div class="section-card" v-if="latestInterview">
            <h3>最近面试反馈</h3>
            <div class="interview-summary">
              <div class="summary-row">
                <span class="summary-label">面试轮次</span>
                <span class="summary-value">{{ latestInterview.round }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">面试官</span>
                <span class="summary-value">{{ latestInterview.interviewer }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">面试时间</span>
                <span class="summary-value">{{ formatDateTime(latestInterview.time) }}</span>
              </div>
              <div class="summary-row">
                <span class="summary-label">面试状态</span>
                <span class="summary-value">{{ getInterviewStatusText(latestInterview.status) }}</span>
              </div>
              <div class="summary-notes">
                <span class="summary-label">反馈摘要</span>
                <p>{{ latestInterview.notes || '暂无反馈内容' }}</p>
              </div>
            </div>
          </div>
          <div class="section-card" v-else-if="currentMode !== 'create' && application?.id">
            <h3>最近面试反馈</h3>
            <div class="empty-state">
              <div class="empty-icon">📝</div>
              <div class="empty-text">暂无面试反馈记录</div>
            </div>
          </div>
        </div>
        <div class="right-panel">
          <div class="section-card">
            <div class="section-header">
              <h3>Offer状态</h3>
              <span class="status-badge" :class="formData.status">{{ getStatusText(formData.status) }}</span>
            </div>
            <div class="status-selector" v-if="currentMode !== 'create'">
              <button 
                v-for="status in statusOptions" 
                :key="status.value"
                :class="['status-btn', { active: formData.status === status.value }]"
                @click="updateStatus(status.value)"
              >
                {{ status.label }}
              </button>
            </div>
          </div>
          <div class="section-card">
            <h3>状态时间线</h3>
            <div class="timeline" v-if="offer">
              <div class="timeline-item">
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                  <div class="timeline-title">创建Offer</div>
                  <div class="timeline-time">{{ formatDateTime(offer.created_at) }}</div>
                </div>
              </div>
              <div class="timeline-item" v-if="offer.status === 'accepted'">
                <div class="timeline-dot accepted"></div>
                <div class="timeline-content">
                  <div class="timeline-title">候选人已接受</div>
                  <div class="timeline-time">{{ formatDateTime(offer.updated_at) }}</div>
                </div>
              </div>
              <div class="timeline-item" v-if="offer.status === 'rejected'">
                <div class="timeline-dot rejected"></div>
                <div class="timeline-content">
                  <div class="timeline-title">候选人已拒绝</div>
                  <div class="timeline-time">{{ formatDateTime(offer.updated_at) }}</div>
                </div>
              </div>
              <div class="timeline-item" v-if="offer.status === 'withdrawn'">
                <div class="timeline-dot withdrawn"></div>
                <div class="timeline-content">
                  <div class="timeline-title">Offer已撤回</div>
                  <div class="timeline-time">{{ formatDateTime(offer.updated_at) }}</div>
                </div>
              </div>
              <div class="timeline-item" v-if="offer.status === 'pending_onboarding'">
                <div class="timeline-dot pending_onboarding"></div>
                <div class="timeline-content">
                  <div class="timeline-title">待入职</div>
                  <div class="timeline-time">{{ formatDateTime(offer.updated_at) }}</div>
                </div>
              </div>
            </div>
            <div class="empty-state" v-else>
              <div class="empty-icon">⏳</div>
              <div class="empty-text">创建Offer后将显示状态时间线</div>
            </div>
          </div>
          <div class="section-card">
            <h3>操作</h3>
            <div class="action-buttons">
              <button v-if="isEdit || currentMode === 'create'" class="btn-save" @click="saveOffer">
                {{ currentMode === 'create' ? '创建Offer' : '保存修改' }}
              </button>
              <button v-if="currentMode !== 'create' && !isEdit" class="btn-edit" @click="enterEditMode">
                编辑Offer
              </button>
              <button v-if="currentMode !== 'create' && formData.status !== 'withdrawn'" class="btn-withdraw" @click="withdrawOffer">
                撤回Offer
              </button>
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import { offersApi, applicationsApi, jobsApi, candidatesApi, interviewsApi } from '../api'

const route = useRoute()
const router = useRouter()
const offer = ref(null)
const application = ref(null)
const job = ref(null)
const candidate = ref(null)
const interviews = ref([])
const latestInterview = ref(null)
const loading = ref(true)
const error = ref(null)
const notFound = ref(false)
const currentMode = ref('create')
const isEdit = ref(false)
const relatedDataError = ref(null)
let loadRequestId = 0

const formData = ref({
  position_title: '',
  salary_min: '',
  salary_max: '',
  start_date: '',
  notes: '',
  status: 'pending'
})

const statusOptions = [
  { value: 'pending', label: '待确认' },
  { value: 'accepted', label: '候选人接受' },
  { value: 'rejected', label: '候选人拒绝' },
  { value: 'pending_onboarding', label: '待入职' }
]

const getStatusText = (status) => {
  const map = {
    'pending': '待确认',
    'accepted': '已接受',
    'rejected': '已拒绝',
    'withdrawn': '已撤回',
    'pending_onboarding': '待入职'
  }
  return map[status] || status
}

const getAppStatusText = (status) => {
  const map = {
    'pending': '待处理',
    'communicating': '已沟通',
    'interviewing': '面试中',
    'rejected': '已拒绝',
    'hired': '已录用'
  }
  return map[status] || (status ? status : '未知')
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

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

const clearAllData = () => {
  offer.value = null
  application.value = null
  job.value = null
  candidate.value = null
  interviews.value = []
  latestInterview.value = null
  error.value = null
  notFound.value = false
  relatedDataError.value = null
  isEdit.value = false
  formData.value = {
    position_title: '',
    salary_min: '',
    salary_max: '',
    start_date: '',
    notes: '',
    status: 'pending'
  }
}

const loadOfferDetail = async (offerId) => {
  try {
    const res = await offersApi.getOffer(offerId)
    return res.data || null
  } catch (e) {
    throw e
  }
}

const loadApplicationData = async (appId) => {
  try {
    const appRes = await applicationsApi.getApplication(appId)
    if (!appRes.data) {
      return null
    }
    
    const [jobRes, candidateRes, interviewsRes] = await Promise.all([
      jobsApi.getJob(appRes.data.job_id),
      candidatesApi.getCandidate(appRes.data.candidate_id),
      interviewsApi.getInterviews({ application_id: appId })
    ])
    
    return {
      application: appRes.data,
      job: jobRes.data,
      candidate: candidateRes.data,
      interviews: interviewsRes.data || []
    }
  } catch (e) {
    console.error('Failed to load application data:', e)
    return null
  }
}

const loadData = async (targetId = null, targetQuery = null) => {
  const requestId = ++loadRequestId
  try {
    loading.value = true
    error.value = null
    notFound.value = false
    relatedDataError.value = null
    clearAllData()

    const currentId = targetId || route.params.id
    const query = targetQuery || route.query

    currentMode.value = currentId === 'create' ? 'create' : 'detail'

    if (currentMode.value === 'create') {
      const appId = query.application_id
      if (appId) {
        const appData = await loadApplicationData(appId)
        if (requestId !== loadRequestId) return
        if (appData) {
          application.value = appData.application
          job.value = appData.job
          candidate.value = appData.candidate
          interviews.value = appData.interviews

          if (appData.interviews.length > 0) {
            latestInterview.value = appData.interviews.reduce((latest, current) => {
              return new Date(current.time) > new Date(latest.time) ? current : latest
            })
          }

          if (job.value) {
            formData.value.position_title = job.value.title
          }
        } else {
          error.value = '关联投递记录不存在或无法获取'
        }
      }
    } else {
      const offerData = await loadOfferDetail(currentId)
      if (requestId !== loadRequestId) return
      if (!offerData) {
        notFound.value = true
        return
      }

      offer.value = offerData
      formData.value = {
        position_title: offerData.position_title,
        salary_min: offerData.salary_min,
        salary_max: offerData.salary_max,
        start_date: offerData.start_date,
        notes: offerData.notes,
        status: offerData.status
      }

      const appId = offerData.application_id
      if (appId) {
        const appData = await loadApplicationData(appId)
        if (requestId !== loadRequestId) return
        if (appData) {
          application.value = appData.application
          job.value = appData.job
          candidate.value = appData.candidate
          interviews.value = appData.interviews

          if (appData.interviews.length > 0) {
            latestInterview.value = appData.interviews.reduce((latest, current) => {
              return new Date(current.time) > new Date(latest.time) ? current : latest
            })
          }
        } else {
          relatedDataError.value = '关联投递信息加载失败，请稍后重试或联系管理员'
        }
      } else {
        relatedDataError.value = '该 Offer 未关联投递记录，无法显示候选人、职位等信息'
      }
    }
  } catch (errorResponse) {
    if (requestId !== loadRequestId) return
    console.error('Failed to load data:', errorResponse)
    if (errorResponse.response?.status === 404) {
      notFound.value = true
    } else {
      error.value = errorResponse.response?.data?.detail || '加载失败，请刷新重试'
    }
  } finally {
    if (requestId === loadRequestId) {
      loading.value = false
    }
  }
}

const enterEditMode = () => {
  isEdit.value = true
}

const saveOffer = async () => {
  try {
    if (!route.query.application_id && currentMode.value === 'create') {
      alert('请先选择投递记录')
      return
    }
    if (!formData.value.position_title) {
      alert('请输入职位名称')
      return
    }
    if (!formData.value.salary_min || !formData.value.salary_max) {
      alert('请输入薪资范围（最低和最高）')
      return
    }
    if (Number(formData.value.salary_min) <= 0 || Number(formData.value.salary_max) <= 0) {
      alert('薪资范围必须为正数')
      return
    }
    if (Number(formData.value.salary_min) >= Number(formData.value.salary_max)) {
      alert('薪资下限不能大于等于上限')
      return
    }
    if (!formData.value.start_date) {
      alert('请选择入职时间')
      return
    }
    const startDate = new Date(formData.value.start_date)
    if (startDate <= new Date()) {
      alert('入职时间必须在未来')
      return
    }
    
    if (currentMode.value === 'create') {
      const res = await offersApi.createOffer({
        ...formData.value,
        application_id: route.query.application_id,
        interview_id: route.query.interview_id
      })
      const newId = res.data?.id
      if (!newId) {
        alert('创建成功但返回数据异常，请返回列表查看')
        await router.push('/offers')
        return
      }
      alert('Offer创建成功')
      await router.push(`/offers/${newId}`)
    } else {
      await offersApi.updateOffer(route.params.id, formData.value)
      alert('Offer信息更新成功')
      isEdit.value = false
      await loadData()
    }
  } catch (errorResponse) {
    console.error('Failed to save offer:', errorResponse)
    const errorMsg = errorResponse.response?.data?.detail || '保存失败，请重试'
    alert(errorMsg)
  }
}

const updateStatus = async (status) => {
  try {
    await offersApi.updateStatus(route.params.id, status)
    formData.value.status = status
    alert(`状态已更新为: ${getStatusText(status)}`)
    await loadData()
  } catch (errorResponse) {
    console.error('Failed to update status:', errorResponse)
    const errorMsg = errorResponse.response?.data?.detail || '更新失败，请重试'
    alert(errorMsg)
  }
}

const withdrawOffer = () => {
  if (confirm('确定要撤回这份Offer吗？')) {
    updateStatus('withdrawn')
  }
}

onMounted(() => {
  loadData()
})

onBeforeRouteUpdate(async (to, from) => {
  if (to.params.id !== from.params.id || to.query.application_id !== from.query.application_id) {
    await loadData(to.params.id, to.query)
  }
})

watch(() => route.params.id, async (newId, oldId) => {
  if (newId !== oldId) {
    await loadData(newId, route.query)
  }
})

watch(() => route.query.application_id, async (newAppId, oldAppId) => {
  if (newAppId !== oldAppId && currentMode.value === 'create') {
    await loadData('create', route.query)
  }
})
</script>

<style scoped>
.offer-detail-page {
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
.page-header {
  margin-bottom: 24px;
}
.page-header h1 {
  font-size: 28px;
  margin-bottom: 8px;
}
.page-header p {
  font-size: 16px;
  color: #666;
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
.detail-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}
.section-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin-bottom: 20px;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.section-card h3 {
  font-size: 18px;
  margin-bottom: 16px;
}
.form-group {
  margin-bottom: 16px;
}
.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 6px;
}
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}
.form-group textarea {
  resize: vertical;
}
.form-group input:disabled,
.form-group textarea:disabled {
  background: #fafafa;
  color: #666;
}
.salary-input {
  display: flex;
  align-items: center;
  gap: 8px;
}
.salary-input input {
  flex: 1;
  width: auto;
}
.salary-separator {
  font-size: 16px;
  color: #999;
}
.salary-unit {
  font-size: 14px;
  color: #999;
}
.info-row {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}
.info-row:last-of-type {
  border-bottom: none;
}
.info-row .label {
  font-size: 13px;
  color: #999;
}
.info-row .value {
  font-size: 14px;
  font-weight: 500;
}
.action-link {
  padding-top: 12px;
  color: #667eea;
  cursor: pointer;
  font-size: 14px;
}
.interview-summary {
  padding-top: 8px;
}
.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}
.summary-row:last-of-type {
  border-bottom: none;
}
.summary-label {
  font-size: 13px;
  color: #999;
}
.summary-value {
  font-size: 14px;
  font-weight: 500;
}
.summary-notes {
  margin-top: 12px;
}
.summary-notes .summary-label {
  display: block;
  margin-bottom: 8px;
}
.summary-notes p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  padding: 12px;
  background: #fafafa;
  border-radius: 6px;
  margin: 0;
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
.status-badge.accepted {
  background: #e8f5e9;
  color: #4caf50;
}
.status-badge.rejected {
  background: #ffebee;
  color: #d32f2f;
}
.status-badge.withdrawn {
  background: #f5f5f5;
  color: #999;
}
.status-badge.pending_onboarding {
  background: #f3e5f5;
  color: #9c27b0;
}
.status-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.status-btn {
  padding: 10px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}
.status-btn:hover {
  border-color: #667eea;
}
.status-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}
.timeline {
  position: relative;
  padding-left: 20px;
}
.timeline::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e0e0e0;
}
.timeline-item {
  position: relative;
  padding-bottom: 20px;
}
.timeline-item:last-child {
  padding-bottom: 0;
}
.timeline-dot {
  position: absolute;
  left: -17px;
  top: 4px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #667eea;
}
.timeline-dot.accepted {
  background: #4caf50;
}
.timeline-dot.rejected {
  background: #d32f2f;
}
.timeline-dot.withdrawn {
  background: #999;
}
.timeline-dot.pending_onboarding {
  background: #9c27b0;
}
.timeline-content {
  padding-left: 10px;
}
.timeline-title {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}
.timeline-time {
  font-size: 12px;
  color: #999;
}
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.btn-save {
  padding: 12px 24px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.btn-edit {
  padding: 12px 24px;
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.btn-withdraw {
  padding: 12px 24px;
  background: white;
  color: #ff9800;
  border: 2px solid #ff9800;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.error-container {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.error-icon {
  font-size: 64px;
  margin-bottom: 20px;
}
.error-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #333;
}
.error-message {
  font-size: 16px;
  color: #999;
  margin-bottom: 24px;
}
.btn-back-home,
.btn-retry {
  padding: 12px 32px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}
.btn-back-home:hover,
.btn-retry:hover {
  background: #5a6fd6;
}
.empty-state {
  text-align: center;
  padding: 30px 20px;
  background: #fafafa;
  border-radius: 8px;
}
.empty-icon {
  font-size: 32px;
  margin-bottom: 12px;
}
.empty-text {
  font-size: 14px;
  color: #999;
}
.related-error-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #fff8e1;
  border: 1px solid #ffe0b2;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 14px;
  color: #e65100;
}
.related-error-icon {
  font-size: 18px;
}
.related-error-text {
  flex: 1;
}
.related-error-retry {
  padding: 6px 14px;
  background: #ff9800;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: background 0.2s;
}
.related-error-retry:hover {
  background: #f57c00;
}
</style>
