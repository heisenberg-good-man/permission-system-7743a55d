<template>
  <div class="offer-detail-page">
    <div v-if="toastMessage" class="toast" :class="toastType">{{ toastMessage }}</div>
    <button class="btn-back" @click="$router.back()">← 返回列表</button>
    
    <div class="role-switcher" v-if="currentMode === 'detail'">
      <span class="role-label">当前视角：</span>
      <button 
        :class="['role-btn', { active: currentRole === 'company' }]" 
        @click="switchRole('company')"
      >
        招聘方
      </button>
      <button 
        :class="['role-btn', { active: currentRole === 'candidate' }]" 
        @click="switchRole('candidate')"
      >
        候选人
      </button>
    </div>

    <div class="loading" v-if="loading">
      <div class="spinner"></div>
      <div class="loading-text">加载中...</div>
    </div>
    <div v-if="!loading">
      <div v-if="notFound" class="error-container">
        <div class="error-icon">❌</div>
        <div class="error-title">Offer不存在</div>
        <div class="error-message">该Offer记录已被删除或不存在</div>
        <div class="error-actions">
          <button class="btn-back-home" @click="router.push('/offers')">返回Offer列表</button>
          <button class="btn-back-home" @click="router.push('/applications')">重新选择关联投递</button>
        </div>
      </div>
      <div v-else-if="error" class="error-container">
        <div class="error-icon">⚠️</div>
        <div class="error-title">加载失败</div>
        <div class="error-message">{{ error }}</div>
        <div class="error-actions">
          <button class="btn-retry" @click="loadData()">重新加载</button>
          <button class="btn-back-home" @click="router.push('/offers')">返回Offer列表</button>
          <button v-if="currentMode === 'create'" class="btn-back-home" @click="router.push('/applications')">去投递列表</button>
        </div>
      </div>
      <div v-else>
        <div class="page-header">
          <h1>{{ pageTitle }}</h1>
          <p>{{ pageSubtitle }}</p>
        </div>
        <div class="related-error-banner" v-if="relatedDataError">
          <span class="related-error-icon">⚠️</span>
          <span class="related-error-text">{{ relatedDataError }}</span>
          <button class="related-error-retry" @click="loadData()">重新加载</button>
          <button v-if="currentMode === 'create'" class="related-error-retry" @click="router.push('/applications')">去投递列表</button>
        </div>
        <div class="detail-container" v-if="currentMode === 'create' || offer">
        <div class="left-panel">
          <div class="section-card">
            <h3>Offer信息</h3>
            <div class="form-group">
              <label>职位名称</label>
              <input type="text" v-model="formData.position_title" :disabled="!canEdit" placeholder="请输入职位名称" />
            </div>
            <div class="form-group">
              <label>薪资范围（K）</label>
              <div class="salary-input">
                <input type="number" v-model="formData.salary_min" :disabled="!canEdit" placeholder="最低" />
                <span class="salary-separator">-</span>
                <input type="number" v-model="formData.salary_max" :disabled="!canEdit" placeholder="最高" />
                <span class="salary-unit">K</span>
              </div>
            </div>
            <div class="form-group">
              <label>入职时间</label>
              <input type="datetime-local" v-model="formData.start_date" :disabled="!canEdit" />
            </div>
            <div class="form-group">
              <label>备注</label>
              <textarea v-model="formData.notes" rows="4" :disabled="!canEdit" placeholder="请输入Offer备注，如福利、奖金等信息"></textarea>
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
            
            <div class="status-selector" v-if="currentMode !== 'create' && isCompany && !isEdit">
              <button 
                v-for="status in statusOptions" 
                :key="status.value"
                :class="['status-btn', { active: formData.status === status.value, disabled: !canChangeStatus(status.value) }]"
                :disabled="!canChangeStatus(status.value)"
                @click="updateStatus(status.value)"
              >
                {{ status.label }}
              </button>
            </div>
            
            <div class="candidate-actions" v-if="currentMode !== 'create' && isCandidate">
              <button 
                v-if="hasAction('accept')" 
                class="btn-accept" 
                @click="acceptOffer"
              >接受Offer</button>
              <button 
                v-if="hasAction('reject')" 
                class="btn-reject" 
                @click="rejectOffer"
              >拒绝Offer</button>
              <button 
                v-if="hasAction('adjustment_request')" 
                class="btn-adjust" 
                @click="showAdjustmentModal = true"
              >请求调整</button>
              <div v-if="!hasAction('accept') && !hasAction('reject') && !hasAction('adjustment_request')" class="disabled-hint">
                {{ getStatusHint() }}
              </div>
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
              <div class="timeline-item" v-if="offer.status === 'draft'">
                <div class="timeline-dot draft"></div>
                <div class="timeline-content">
                  <div class="timeline-title">Offer草稿（未发出）</div>
                  <div class="timeline-time">{{ formatDateTime(offer.updated_at) }}</div>
                </div>
              </div>
              <div class="timeline-item" v-if="offer.status !== 'draft' && (offer.status === 'pending' || offer.status === 'adjustment_requested' || offer.status === 'accepted' || offer.status === 'rejected' || offer.status === 'pending_onboarding')">
                <div class="timeline-dot pending"></div>
                <div class="timeline-content">
                  <div class="timeline-title">Offer已发出</div>
                  <div class="timeline-time">{{ formatDateTime(offer.updated_at) }}</div>
                </div>
              </div>
              <div class="timeline-item" v-if="offer.status === 'adjustment_requested'">
                <div class="timeline-dot adjustment"></div>
                <div class="timeline-content">
                  <div class="timeline-title">候选人请求调整</div>
                  <div class="timeline-time">{{ formatDateTime(offer.updated_at) }}</div>
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
          <div class="section-card" v-if="currentMode !== 'create'">
            <h3>操作</h3>
            <div class="action-buttons">
              <button v-if="isEdit || currentMode === 'create'" class="btn-save" @click="saveOffer">
                {{ currentMode === 'create' ? '创建Offer' : '保存修改' }}
              </button>
              <button v-if="currentMode !== 'create' && !isEdit && canEdit" class="btn-edit" @click="enterEditMode">
                编辑Offer
              </button>
              <button v-if="hasAction('send')" class="btn-send-offer" @click="sendOffer">
                发出Offer
              </button>
              <button v-if="hasAction('re_send')" class="btn-send-offer" @click="reSendOffer">
                修改并重新发出
              </button>
              <button v-if="hasAction('withdraw')" class="btn-withdraw" @click="withdrawOffer">
                撤回Offer
              </button>
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>

    <div class="modal-overlay" v-if="showAdjustmentModal" @click="showAdjustmentModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>请求调整Offer</h3>
          <button class="modal-close" @click="showAdjustmentModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>调整请求内容</label>
            <textarea v-model="adjustmentContent" rows="4" placeholder="请描述您希望调整的内容，例如：薪资、入职时间等"></textarea>
          </div>
          <div class="form-group">
            <label>期望薪资（K）</label>
            <div class="salary-input">
              <input type="number" v-model="adjustmentSalaryMin" placeholder="最低" />
              <span class="salary-separator">-</span>
              <input type="number" v-model="adjustmentSalaryMax" placeholder="最高" />
              <span class="salary-unit">K</span>
            </div>
          </div>
          <div class="form-group">
            <label>期望入职时间</label>
            <input type="datetime-local" v-model="adjustmentStartDate" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showAdjustmentModal = false">取消</button>
          <button class="btn-submit" @click="submitAdjustment">提交调整请求</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay" v-if="showWithdrawModal" @click="showWithdrawModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>确认撤回Offer</h3>
          <button class="modal-close" @click="showWithdrawModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="warning-icon">⚠️</div>
          <div class="warning-text">撤回后候选人将无法接受该Offer，此操作不可撤销。</div>
          <div class="form-group">
            <label>撤回原因（选填）</label>
            <textarea v-model="withdrawReason" rows="3" placeholder="请说明撤回原因，将发送给候选人"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showWithdrawModal = false">取消</button>
          <button class="btn-withdraw-modal" @click="confirmWithdraw">确认撤回</button>
        </div>
      </div>
    </div>

    <div class="communication-section" v-if="currentMode === 'detail'">
      <div class="section-card">
        <h3>沟通记录</h3>
        <div class="messages-container">
          <div 
            v-for="msg in messages" 
            :key="msg.id" 
            :class="['message-item', msg.sender_type]"
          >
            <div class="message-header">
              <span class="message-sender">{{ msg.sender_type === 'company' ? '招聘方' : '候选人' }}</span>
              <span class="message-time">{{ formatDateTime(msg.sent_at) }}</span>
              <span v-if="msg.message_type === 'adjustment_request'" class="message-tag adjustment">调整请求</span>
              <span v-if="msg.message_type === 'counter_offer'" class="message-tag counter">重新发出</span>
              <span v-if="msg.message_type === 'system'" class="message-tag system">系统通知</span>
            </div>
            <div class="message-content">{{ msg.content }}</div>
          </div>
          <div class="empty-state" v-if="!messages.length">
            <div class="empty-icon">💬</div>
            <div class="empty-text">暂无沟通记录</div>
          </div>
        </div>
        <div class="message-input-container" v-if="hasAction('send_message')">
          <textarea v-model="newMessageContent" rows="2" placeholder="输入消息内容..." @keydown.enter.ctrl="sendMessage"></textarea>
          <button class="btn-send" @click="sendMessage">发送</button>
        </div>
        <div v-if="!hasAction('send_message') && formData.status === 'withdrawn' && isCandidate" class="disabled-hint">
          Offer已撤回，无法发送消息
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import { offersApi, applicationsApi, jobsApi, candidatesApi, interviewsApi, offerMessagesApi } from '../api'

const route = useRoute()
const router = useRouter()
const offer = ref(null)
const application = ref(null)
const job = ref(null)
const candidate = ref(null)
const interviews = ref([])
const latestInterview = ref(null)
const messages = ref([])
const availableActions = ref([])
const loading = ref(true)
const error = ref(null)
const notFound = ref(false)
const currentMode = ref('create')
const currentRole = ref('company')
const isEdit = ref(false)
const relatedDataError = ref(null)
const toastMessage = ref('')
const toastType = ref('success')
const showAdjustmentModal = ref(false)
const showWithdrawModal = ref(false)
const adjustmentContent = ref('')
const adjustmentSalaryMin = ref('')
const adjustmentSalaryMax = ref('')
const adjustmentStartDate = ref('')
const withdrawReason = ref('')
const newMessageContent = ref('')
let loadRequestId = 0

const showToast = (message, type = 'success') => {
  toastMessage.value = message
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = ''
  }, 3000)
}

const isCompany = computed(() => currentRole.value === 'company')

const canEdit = computed(() => {
  if (currentMode.value === 'create') return true
  if (isEdit.value) return true
  return availableActions.value.includes('edit')
})

const canSendMessage = computed(() => {
  return availableActions.value.includes('send_message')
})

const hasAction = (action) => {
  return availableActions.value.includes(action)
}

const canChangeStatus = (status) => {
  if (!isCompany.value) return false
  const current = formData.value.status
  if (current === 'accepted' || current === 'rejected' || current === 'withdrawn') return false
  if (status === 'accepted' || status === 'rejected') return false
  if (current === 'draft' && status === 'pending') return true
  if (current === 'pending' && status === 'withdrawn') return true
  if (current === 'pending' && status === 'pending_onboarding') return true
  if (current === 'adjustment_requested' && status === 'pending') return true
  if (current === 'adjustment_requested' && status === 'withdrawn') return true
  return false
}

const getStatusHint = () => {
  const status = formData.value.status
  if (status === 'draft') return 'Offer尚未发出，请等待招聘方发出'
  if (status === 'adjustment_requested') return '您已提出调整请求，请等待招聘方回复'
  if (status === 'accepted') return '您已接受该Offer'
  if (status === 'rejected') return '您已拒绝该Offer'
  if (status === 'withdrawn') return 'Offer已被撤回，仅可查看历史记录'
  if (status === 'pending_onboarding') return 'Offer已接受，等待入职'
  return ''
}

const pageTitle = computed(() => {
  if (isEdit.value) return '编辑Offer'
  if (currentMode.value === 'create') return '创建Offer'
  return offer.value ? `Offer详情 - ${offer.value.id}` : 'Offer详情'
})

const pageSubtitle = computed(() => {
  const jobTitle = job.value?.title || '未关联职位'
  const candidateName = candidate.value?.name || '未关联候选人'
  return `${jobTitle} - ${candidateName}`
})

const formData = ref({
  position_title: '',
  salary_min: '',
  salary_max: '',
  start_date: '',
  notes: '',
  status: 'draft'
})

const statusOptions = [
  { value: 'pending', label: '待确认' },
  { value: 'accepted', label: '候选人接受' },
  { value: 'rejected', label: '候选人拒绝' },
  { value: 'pending_onboarding', label: '待入职' }
]

const getStatusText = (status) => {
  const map = {
    'draft': '草稿（未发出）',
    'pending': '待确认',
    'adjustment_requested': '待调整',
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

const resetAllState = () => {
  offer.value = null
  application.value = null
  job.value = null
  candidate.value = null
  interviews.value = []
  latestInterview.value = null
  messages.value = []
  availableActions.value = []
  error.value = null
  notFound.value = false
  relatedDataError.value = null
  isEdit.value = false
  adjustmentContent.value = ''
  adjustmentSalaryMin.value = ''
  adjustmentSalaryMax.value = ''
  adjustmentStartDate.value = ''
  newMessageContent.value = ''
  formData.value = {
    position_title: '',
    salary_min: '',
    salary_max: '',
    start_date: '',
    notes: '',
    status: 'draft'
  }
}

const applyOfferDetail = (data) => {
  offer.value = data.offer
  application.value = data.application
  job.value = data.job
  candidate.value = data.candidate
  interviews.value = data.interviews || []
  latestInterview.value = data.latest_interview
  messages.value = data.messages || []
  availableActions.value = data.available_actions || []
  if (data.offer) {
    formData.value = {
      position_title: data.offer.position_title,
      salary_min: data.offer.salary_min,
      salary_max: data.offer.salary_max,
      start_date: data.offer.start_date,
      notes: data.offer.notes,
      status: data.offer.status
    }
  }
}

const loadApplicationData = async (appId) => {
  try {
    const appRes = await applicationsApi.getApplication(appId)
    if (!appRes.data) return null

    const [jobRes, candidateRes, interviewsRes] = await Promise.allSettled([
      jobsApi.getJob(appRes.data.job_id),
      candidatesApi.getCandidate(appRes.data.candidate_id),
      interviewsApi.getInterviews({ application_id: appId })
    ])

    let job = null
    if (jobRes.status === 'fulfilled' && jobRes.value?.data) {
      job = jobRes.value.data
    }

    let candidate = null
    if (candidateRes.status === 'fulfilled' && candidateRes.value?.data) {
      candidate = candidateRes.value.data
    }

    let interviews = []
    let latest = null
    if (interviewsRes.status === 'fulfilled' && interviewsRes.value?.data) {
      interviews = interviewsRes.value.data || []
      if (interviews.length > 0) {
        latest = interviews.reduce((l, c) => new Date(c.time) > new Date(l.time) ? c : l)
      }
    }

    return {
      application: appRes.data,
      job: job,
      candidate: candidate,
      interviews: interviews,
      latest_interview: latest
    }
  } catch (e) {
    console.error('Failed to load application data:', e)
    return null
  }
}

const loadData = async (targetId = null, targetQuery = null, targetRole = null) => {
  const requestId = ++loadRequestId
  try {
    loading.value = true
    resetAllState()

    const currentId = targetId || route.params.id
    const query = targetQuery || route.query
    const role = targetRole || currentRole.value
    currentRole.value = role
    const isCreate = currentId === 'create'
    currentMode.value = isCreate ? 'create' : 'detail'

    if (isCreate) {
      const appId = query.application_id
      if (appId) {
        const appData = await loadApplicationData(appId)
        if (requestId !== loadRequestId) return
        if (appData) {
          application.value = appData.application
          job.value = appData.job
          candidate.value = appData.candidate
          interviews.value = appData.interviews
          latestInterview.value = appData.latest_interview
          if (appData.job) {
            formData.value.position_title = appData.job.title
          }
        } else {
          error.value = '关联投递记录不存在或无法获取'
        }
      } else {
        relatedDataError.value = '请从候选人详情、投递详情或面试详情进入创建 Offer，以确保关联正确的投递记录'
      }
    } else {
      const detailRes = await offersApi.getOfferDetails(currentId, { role })
      if (requestId !== loadRequestId) return
      const data = detailRes.data
      if (!data?.offer) {
        notFound.value = true
        return
      }

      applyOfferDetail(data)

      if (!data.application) {
        relatedDataError.value = '该 Offer 未关联投递记录，无法显示候选人、职位等信息'
      } else if (!data.job || !data.candidate) {
        relatedDataError.value = '关联的职位或候选人信息加载失败，请稍后重试'
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

const switchRole = async (role) => {
  if (currentRole.value === role) return
  await loadData(null, null, role)
}

const enterEditMode = () => {
  isEdit.value = true
}

const saveOffer = async () => {
  try {
    if (!route.query.application_id && currentMode.value === 'create') {
      showToast('请先选择投递记录', 'error')
      return
    }
    if (!formData.value.position_title) {
      showToast('请输入职位名称', 'error')
      return
    }
    if (!formData.value.salary_min || !formData.value.salary_max) {
      showToast('请输入薪资范围（最低和最高）', 'error')
      return
    }
    if (Number(formData.value.salary_min) <= 0 || Number(formData.value.salary_max) <= 0) {
      showToast('薪资范围必须为正数', 'error')
      return
    }
    if (Number(formData.value.salary_min) >= Number(formData.value.salary_max)) {
      showToast('薪资下限不能大于等于上限', 'error')
      return
    }
    if (!formData.value.start_date) {
      showToast('请选择入职时间', 'error')
      return
    }
    const startDate = new Date(formData.value.start_date)
    if (startDate <= new Date()) {
      showToast('入职时间必须在未来', 'error')
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
        showToast('创建成功但返回数据异常，请返回列表查看', 'error')
        await router.push('/offers')
        return
      }
      showToast('Offer创建成功（草稿状态）')

      await router.replace({ path: `/offers/${newId}`, query: {} })
      await nextTick()
      await loadData(newId, {})
    } else {
      await offersApi.updateOffer(route.params.id, formData.value)
      showToast('Offer信息更新成功')
      isEdit.value = false
      await loadData()
    }
  } catch (errorResponse) {
    console.error('Failed to save offer:', errorResponse)
    const errorMsg = errorResponse.response?.data?.detail || '保存失败，请重试'
    showToast(errorMsg, 'error')
  }
}

const updateStatus = async (status) => {
  try {
    await offersApi.updateStatus(route.params.id, status)
    showToast(`状态已更新为: ${getStatusText(status)}`)
    
    let messageContent = ''
    let messageType = 'system'
    if (status === 'accepted') {
      messageContent = '候选人已接受Offer'
    } else if (status === 'rejected') {
      messageContent = '候选人已拒绝Offer'
    } else if (status === 'pending_onboarding') {
      messageContent = 'Offer状态更新为待入职'
    } else if (status === 'pending') {
      if (formData.value.status === 'draft') {
        messageContent = 'Offer已发出，请查收详细条款'
      } else if (formData.value.status === 'adjustment_requested') {
        messageContent = '招聘方修改条款后重新发出Offer'
        messageType = 'counter_offer'
      }
    } else if (status === 'withdrawn') {
      messageContent = 'Offer已被招聘方撤回'
    } else if (status === 'adjustment_requested') {
      messageContent = '候选人请求调整Offer条款'
      messageType = 'adjustment_request'
    }
    
    if (messageContent) {
      await offerMessagesApi.createMessage({
        offer_id: route.params.id,
        sender_id: isCompany.value ? 'company' : 'candidate',
        sender_type: isCompany.value ? 'company' : 'candidate',
        content: messageContent,
        message_type: messageType
      })
    }
    
    await loadData()
  } catch (errorResponse) {
    console.error('Failed to update status:', errorResponse)
    const errorMsg = errorResponse.response?.data?.detail || '更新失败，请重试'
    showToast(errorMsg, 'error')
  }
}

const sendOffer = async () => {
  if (formData.value.status !== 'draft') {
    showToast('只有草稿状态的Offer才能发出', 'error')
    return
  }
  await updateStatus('pending')
}

const reSendOffer = async () => {
  if (formData.value.status !== 'adjustment_requested') {
    showToast('只有待调整状态的Offer才能重新发出', 'error')
    return
  }
  await updateStatus('pending')
}

const acceptOffer = async () => {
  if (formData.value.status !== 'pending') {
    showToast('只有待确认状态的Offer才能接受', 'error')
    return
  }
  await updateStatus('accepted')
}

const rejectOffer = async () => {
  if (formData.value.status !== 'pending') {
    showToast('只有待确认状态的Offer才能拒绝', 'error')
    return
  }
  await updateStatus('rejected')
}

const submitAdjustment = async () => {
  try {
    if (!adjustmentContent.value.trim()) {
      showToast('请输入调整请求内容', 'error')
      return
    }

    let content = adjustmentContent.value
    if (adjustmentSalaryMin.value || adjustmentSalaryMax.value) {
      content += `\n期望薪资：${adjustmentSalaryMin.value || '-'}K-${adjustmentSalaryMax.value || '-'}K`
    }
    if (adjustmentStartDate.value) {
      content += `\n期望入职时间：${adjustmentStartDate.value}`
    }

    await offerMessagesApi.createMessage({
      offer_id: route.params.id,
      sender_id: 'candidate',
      sender_type: 'candidate',
      content: content,
      message_type: 'adjustment_request'
    })

    await offersApi.updateStatus(route.params.id, 'adjustment_requested')

    showToast('调整请求已发送，等待招聘方回复')
    showAdjustmentModal.value = false
    adjustmentContent.value = ''
    adjustmentSalaryMin.value = ''
    adjustmentSalaryMax.value = ''
    adjustmentStartDate.value = ''
    await loadData()
  } catch (errorResponse) {
    console.error('Failed to submit adjustment:', errorResponse)
    const errorMsg = errorResponse.response?.data?.detail || '发送失败，请重试'
    showToast(errorMsg, 'error')
  }
}

const withdrawOffer = () => {
  showWithdrawModal.value = true
}

const confirmWithdraw = async () => {
  try {
    await offersApi.updateStatus(route.params.id, 'withdrawn')
    
    let messageContent = 'Offer已被招聘方撤回'
    if (withdrawReason.value.trim()) {
      messageContent += `\n原因：${withdrawReason.value}`
    }
    
    await offerMessagesApi.createMessage({
      offer_id: route.params.id,
      sender_id: 'company',
      sender_type: 'company',
      content: messageContent,
      message_type: 'system'
    })
    
    showToast('Offer已撤回')
    showWithdrawModal.value = false
    withdrawReason.value = ''
    await loadData()
  } catch (errorResponse) {
    console.error('Failed to withdraw offer:', errorResponse)
    const errorMsg = errorResponse.response?.data?.detail || '撤回失败，请重试'
    showToast(errorMsg, 'error')
  }
}

const sendMessage = async () => {
  try {
    if (!newMessageContent.value.trim()) {
      showToast('请输入消息内容', 'error')
      return
    }

    await offerMessagesApi.createMessage({
      offer_id: route.params.id,
      sender_id: isCompany.value ? 'company' : 'candidate',
      sender_type: isCompany.value ? 'company' : 'candidate',
      content: newMessageContent.value.trim(),
      message_type: 'text'
    })

    newMessageContent.value = ''
    await loadData()
  } catch (errorResponse) {
    console.error('Failed to send message:', errorResponse)
    const errorMsg = errorResponse.response?.data?.detail || '发送失败，请重试'
    showToast(errorMsg, 'error')
  }
}

onMounted(() => {
  loadData()
})

onBeforeRouteUpdate(async (to, from) => {
  const newId = to.params.id
  const oldId = from.params.id
  const newAppId = to.query.application_id
  const oldAppId = from.query.application_id
  const newInterviewId = to.query.interview_id
  const oldInterviewId = from.query.interview_id
  
  if (newId !== oldId || newAppId !== oldAppId || newInterviewId !== oldInterviewId) {
    await loadData(newId, to.query)
  }
})

watch(() => [route.params.id, route.query.application_id, route.query.interview_id],
  ([newId, newAppId, newInterviewId], [oldId, oldAppId, oldInterviewId]) => {
    if (newId === oldId && newAppId === oldAppId && newInterviewId === oldInterviewId) return
    loadData(newId, route.query)
  },
  { immediate: false }
)
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
.role-switcher {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}
.role-label {
  font-size: 14px;
  color: #666;
}
.role-btn {
  padding: 8px 20px;
  background: white;
  border: 2px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}
.role-btn:hover {
  border-color: #667eea;
}
.role-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 24px;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  z-index: 9999;
  animation: slideIn 0.3s ease-out;
}
.toast.success {
  background: #52c41a;
}
.toast.error {
  background: #ff4d4f;
}
@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
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
.status-badge.draft {
  background: #f5f5f5;
  color: #999;
}
.status-badge.pending {
  background: #fff3e0;
  color: #ff9800;
}
.status-badge.adjustment_requested {
  background: #fff8e1;
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
.status-btn:hover:not(.disabled) {
  border-color: #667eea;
}
.status-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}
.status-btn.disabled,
.status-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.candidate-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.btn-accept {
  padding: 12px 24px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.btn-reject {
  padding: 12px 24px;
  background: #d32f2f;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.btn-adjust {
  padding: 12px 24px;
  background: #ff9800;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.btn-send-offer {
  padding: 12px 24px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.disabled-hint {
  padding: 12px;
  background: #f5f5f5;
  border-radius: 8px;
  font-size: 14px;
  color: #999;
  text-align: center;
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
.timeline-dot.pending {
  background: #ff9800;
}
.timeline-dot.adjustment {
  background: #ff9800;
}
.timeline-dot.rejected {
  background: #d32f2f;
}
.timeline-dot.withdrawn {
  background: #999;
}
.timeline-dot.draft {
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
.error-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
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
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}
.modal-header h3 {
  margin: 0;
}
.modal-close {
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
  color: #999;
}
.modal-body {
  padding: 24px;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #f0f0f0;
}
.btn-cancel {
  padding: 10px 24px;
  background: #f5f5f5;
  color: #666;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.btn-submit {
  padding: 10px 24px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.btn-withdraw-modal {
  padding: 10px 24px;
  background: #d32f2f;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.warning-icon {
  font-size: 48px;
  text-align: center;
  margin-bottom: 16px;
}
.warning-text {
  text-align: center;
  font-size: 14px;
  color: #d32f2f;
  margin-bottom: 20px;
}
.communication-section {
  margin-top: 24px;
}
.messages-container {
  max-height: 400px;
  overflow-y: auto;
  padding-right: 10px;
}
.message-item {
  margin-bottom: 16px;
  padding: 12px;
  border-radius: 8px;
}
.message-item.company {
  background: #f0f4ff;
}
.message-item.candidate {
  background: #fafafa;
}
.message-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
  font-size: 12px;
}
.message-sender {
  font-weight: 600;
  color: #667eea;
}
.message-item.candidate .message-sender {
  color: #ff9800;
}
.message-time {
  color: #999;
}
.message-tag {
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}
.message-tag.adjustment {
  background: #fff3e0;
  color: #ff9800;
}
.message-tag.counter {
  background: #e8f5e9;
  color: #4caf50;
}
.message-tag.system {
  background: #e3f2fd;
  color: #1976d2;
}
.message-content {
  font-size: 14px;
  line-height: 1.6;
}
.message-input-container {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}
.message-input-container textarea {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  resize: vertical;
}
.btn-send {
  padding: 10px 24px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  align-self: flex-end;
}
</style>