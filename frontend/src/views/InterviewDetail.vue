<template>
  <div class="interview-detail-page">
    <button class="btn-back" @click="$router.back()">← 返回列表</button>
    <div class="loading" v-if="loading">
      <div class="spinner"></div>
      <div class="loading-text">加载中...</div>
    </div>
    <div v-if="!loading">
      <div class="page-header">
        <h1>{{ isEdit ? '编辑面试' : (isCreate ? '安排面试' : '面试详情') }}</h1>
        <p>{{ job?.title }} - {{ candidate?.name }}</p>
      </div>
      <div class="detail-container" v-if="interview || isCreate">
        <div class="left-panel">
          <div class="section-card">
            <h3>面试信息</h3>
            <div class="form-group">
              <label>面试轮次</label>
              <select v-model="formData.round" :disabled="!isEdit && !isCreate">
                <option value="初试">初试</option>
                <option value="复试">复试</option>
                <option value="终试">终试</option>
              </select>
            </div>
            <div class="form-group">
              <label>面试方式</label>
              <select v-model="formData.method" :disabled="!isEdit && !isCreate">
                <option value="视频面试">视频面试</option>
                <option value="现场面试">现场面试</option>
                <option value="电话面试">电话面试</option>
              </select>
            </div>
            <div class="form-group">
              <label>面试时间</label>
              <input type="datetime-local" v-model="formData.time" :disabled="!isEdit && !isCreate" />
            </div>
            <div class="form-group">
              <label>面试地点/会议链接</label>
              <textarea v-model="formData.location" rows="2" :disabled="!isEdit && !isCreate" placeholder="请输入面试地点或视频会议链接"></textarea>
            </div>
            <div class="form-group">
              <label>面试官</label>
              <input type="text" v-model="formData.interviewer" :disabled="!isEdit && !isCreate" placeholder="请输入面试官姓名" />
            </div>
            <div class="form-group">
              <label>备注</label>
              <textarea v-model="formData.notes" rows="4" :disabled="!isEdit && !isCreate" placeholder="请输入面试备注"></textarea>
            </div>
          </div>
          <div class="section-card">
            <h3>关联信息</h3>
            <div class="info-row">
              <span class="label">职位</span>
              <span class="value">{{ job?.title }}</span>
            </div>
            <div class="info-row">
              <span class="label">公司</span>
              <span class="value">{{ job?.company }}</span>
            </div>
            <div class="info-row">
              <span class="label">候选人</span>
              <span class="value">{{ candidate?.name }}</span>
            </div>
            <div class="info-row">
              <span class="label">投递状态</span>
              <span class="value">{{ getAppStatusText(application?.status) }}</span>
            </div>
            <div class="action-link" @click="$router.push(`/applications/${application?.id}`)">
              → 查看投递详情
            </div>
          </div>
        </div>
        <div class="right-panel">
          <div class="section-card">
            <div class="section-header">
              <h3>面试状态</h3>
              <span class="status-badge" :class="formData.status">{{ getStatusText(formData.status) }}</span>
            </div>
            <div class="status-selector" v-if="!isCreate">
              <button 
                v-for="status in statusOptions" 
                :key="status.value"
                :class="['status-btn', { active: formData.status === status.value }]"
                @click="updateStatus(status.value)"
              >
                {{ status.label }}
              </button>
            </div>
            <div class="status-selector" v-if="isCreate">
              <button 
                v-for="status in createStatusOptions" 
                :key="status.value"
                :class="['status-btn', { active: formData.status === status.value }]"
                @click="formData.status = status.value"
              >
                {{ status.label }}
              </button>
            </div>
          </div>
          <div class="section-card">
            <h3>操作</h3>
            <div class="action-buttons">
              <button v-if="!isCreate && !isEdit" class="btn-offer" @click="$router.push(`/offers/create?application_id=${application?.id}&interview_id=${route.params.id}`)">
                📋 发放Offer
              </button>
              <button v-if="isEdit || isCreate" class="btn-save" @click="saveInterview">
                {{ isCreate ? '创建面试' : '保存修改' }}
              </button>
              <button v-if="!isCreate && !isEdit" class="btn-edit" @click="enterEditMode">
                编辑面试
              </button>
              <button v-if="!isCreate" class="btn-cancel" @click="cancelInterview" v-show="formData.status !== 'cancelled'">
                取消面试
              </button>
            </div>
          </div>
          <div class="section-card" v-if="!isCreate">
            <h3>时间信息</h3>
            <div class="info-row">
              <span class="label">创建时间</span>
              <span class="value">{{ formatDateTime(interview?.created_at) }}</span>
            </div>
            <div class="info-row">
              <span class="label">更新时间</span>
              <span class="value">{{ formatDateTime(interview?.updated_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { interviewsApi, applicationsApi, jobsApi, candidatesApi } from '../api'

const route = useRoute()
const router = useRouter()
const interview = ref(null)
const application = ref(null)
const job = ref(null)
const candidate = ref(null)
const loading = ref(true)
const isCreate = computed(() => route.params.id === 'create')
const isEdit = ref(false)

const formData = ref({
  interviewer: '',
  round: '初试',
  method: '视频面试',
  time: '',
  location: '',
  status: 'pending',
  notes: ''
})

const statusOptions = [
  { value: 'pending', label: '待安排' },
  { value: 'scheduled', label: '已安排' },
  { value: 'completed', label: '已完成' },
  { value: 'cancelled', label: '已取消' }
]

const createStatusOptions = [
  { value: 'pending', label: '待安排' },
  { value: 'scheduled', label: '已安排' }
]

const getStatusText = (status) => {
  const map = {
    'pending': '待安排',
    'scheduled': '已安排',
    'completed': '已完成',
    'cancelled': '已取消'
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
  return map[status] || status
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

const loadData = async () => {
  try {
    loading.value = true
    if (!isCreate.value) {
      const res = await interviewsApi.getInterview(route.params.id)
      interview.value = res.data
      formData.value = {
        interviewer: res.data.interviewer,
        round: res.data.round,
        method: res.data.method,
        time: res.data.time,
        location: res.data.location,
        status: res.data.status,
        notes: res.data.notes
      }
    }
    
    const appId = isCreate.value ? route.query.application_id : interview.value?.application_id
    if (appId) {
      const [appRes, jobRes, candidateRes] = await Promise.all([
        applicationsApi.getApplication(appId),
        jobsApi.getJob(appId ? (await applicationsApi.getApplication(appId)).data.job_id : ''),
        candidatesApi.getCandidate(appId ? (await applicationsApi.getApplication(appId)).data.candidate_id : '')
      ])
      application.value = appRes.data
      job.value = jobRes.data
      candidate.value = candidateRes.data
    }
  } catch (error) {
    console.error('Failed to load data:', error)
  } finally {
    loading.value = false
  }
}

const enterEditMode = () => {
  isEdit.value = true
}

const saveInterview = async () => {
  try {
    if (!route.query.application_id && isCreate.value) {
      alert('请先选择投递记录')
      return
    }
    if (!formData.value.time) {
      alert('请选择面试时间')
      return
    }
    if (!formData.value.interviewer) {
      alert('请输入面试官姓名')
      return
    }
    if (!formData.value.method) {
      alert('请选择面试方式')
      return
    }
    
    if (isCreate.value) {
      const res = await interviewsApi.createInterview({
        ...formData.value,
        application_id: route.query.application_id
      })
      alert('面试安排创建成功')
      router.push(`/interviews/${res.data.id}`)
    } else {
      await interviewsApi.updateInterview(route.params.id, formData.value)
      alert('面试信息更新成功')
      isEdit.value = false
      await loadData()
    }
  } catch (error) {
    console.error('Failed to save interview:', error)
    const errorMsg = error.response?.data?.detail || '保存失败，请重试'
    alert(errorMsg)
  }
}

const updateStatus = async (status) => {
  try {
    await interviewsApi.updateStatus(route.params.id, status)
    formData.value.status = status
    alert(`状态已更新为: ${getStatusText(status)}`)
    await loadData()
  } catch (error) {
    console.error('Failed to update status:', error)
    alert('更新失败，请重试')
  }
}

const cancelInterview = () => {
  if (confirm('确定要取消这场面试吗？')) {
    updateStatus('cancelled')
  }
}

watch(() => route.params.id, () => {
  if (!isCreate.value) {
    loadData()
  }
})

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.interview-detail-page {
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
.form-group select,
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
.form-group select:disabled,
.form-group textarea:disabled {
  background: #fafafa;
  color: #666;
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
.btn-offer {
  padding: 12px 24px;
  background: #ff9800;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.btn-cancel {
  padding: 12px 24px;
  background: white;
  color: #d32f2f;
  border: 2px solid #d32f2f;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
</style>