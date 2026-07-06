<template>
  <div class="application-detail-page">
    <button class="btn-back" @click="$router.back()">← 返回列表</button>
    <div class="detail-container" v-if="application">
      <div class="left-panel">
        <div class="section-card">
          <div class="section-header">
            <h3>职位信息</h3>
            <span class="status-badge" :class="application.status">{{ getStatusText(application.status) }}</span>
          </div>
          <div class="job-info">
            <div class="job-title">{{ job?.title }}</div>
            <div class="job-meta">
              <span>🏢 {{ job?.company }}</span>
              <span>📍 {{ job?.city }}</span>
              <span>💰 {{ job?.salary_min }}-{{ job?.salary_max }}K</span>
            </div>
          </div>
        </div>
        <div class="section-card">
          <h3>候选人信息</h3>
          <div class="candidate-info">
            <div class="candidate-header">
              <span class="candidate-icon">👤</span>
              <span class="candidate-name">{{ candidate?.name }}</span>
            </div>
            <div class="candidate-details">
              <div>📧 {{ candidate?.email }}</div>
              <div>📱 {{ candidate?.phone }}</div>
              <div>🎓 {{ candidate?.education }}</div>
              <div>📅 {{ candidate?.experience }}经验</div>
            </div>
            <div class="resume-section">
              <h4>简历</h4>
              <pre>{{ candidate?.resume }}</pre>
            </div>
          </div>
        </div>
        <div class="section-card">
          <h3>状态变更</h3>
          <div class="status-selector">
            <button 
              v-for="status in statusOptions" 
              :key="status.value"
              :class="['status-btn', { active: application.status === status.value }]"
              @click="updateStatus(status.value)"
            >
              {{ status.label }}
            </button>
          </div>
        </div>
      </div>
      <div class="right-panel">
        <div class="section-card chat-card">
          <h3>沟通记录</h3>
          <div class="messages-container" ref="messagesContainer">
            <div 
              v-for="message in messages" 
              :key="message.id" 
              :class="['message', message.sender_type]"
            >
              <div class="message-header">
                <span class="sender-name">{{ getSenderName(message) }}</span>
                <span class="send-time">{{ formatTime(message.sent_at) }}</span>
              </div>
              <div class="message-content">{{ message.content }}</div>
            </div>
          </div>
          <div class="message-input-container">
            <textarea 
              v-model="newMessage" 
              rows="2" 
              placeholder="输入消息..."
              @keydown.enter.ctrl="sendMessage"
            ></textarea>
            <div class="input-actions">
              <span class="hint">Ctrl+Enter 发送</span>
              <button class="btn-send" @click="sendMessage">发送</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { applicationsApi, jobsApi, candidatesApi, messagesApi } from '../api'

const route = useRoute()
const application = ref(null)
const job = ref(null)
const candidate = ref(null)
const messages = ref([])
const newMessage = ref('')
const messagesContainer = ref(null)

const statusOptions = [
  { value: 'pending', label: '待处理' },
  { value: 'communicating', label: '已沟通' },
  { value: 'interviewing', label: '面试中' },
  { value: 'rejected', label: '已拒绝' },
  { value: 'hired', label: '已录用' }
]

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

const getSenderName = (message) => {
  if (message.sender_type === 'candidate') {
    return candidate.value?.name || '候选人'
  }
  return '招聘方'
}

const formatTime = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`
}

const loadData = async () => {
  try {
    const [appRes, jobRes, candidateRes, messagesRes] = await Promise.all([
      applicationsApi.getApplication(route.params.id),
      jobsApi.getJob(application.value?.job_id || ''),
      candidatesApi.getCandidate(application.value?.candidate_id || ''),
      messagesApi.getMessages({ application_id: route.params.id })
    ])
    application.value = appRes.data
    job.value = jobRes.data
    candidate.value = candidateRes.data
    messages.value = messagesRes.data
    scrollToBottom()
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

const updateStatus = async (status) => {
  try {
    await applicationsApi.updateStatus(route.params.id, status)
    application.value.status = status
    alert(`状态已更新为: ${getStatusText(status)}`)
  } catch (error) {
    console.error('Failed to update status:', error)
    alert('更新失败，请重试')
  }
}

const sendMessage = async () => {
  const content = newMessage.value.trim()
  if (!content) return
  
  try {
    const res = await messagesApi.createMessage({
      application_id: route.params.id,
      sender_id: 'company-test',
      sender_type: 'company',
      content: content
    })
    messages.value.push(res.data)
    newMessage.value = ''
    scrollToBottom()
  } catch (error) {
    console.error('Failed to send message:', error)
    alert('发送失败，请重试')
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.application-detail-page {
  padding: 20px 0;
}
.btn-back {
  background: none;
  border: none;
  color: #667eea;
  font-size: 16px;
  cursor: pointer;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 4px;
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
}
.status-badge {
  font-size: 12px;
  padding: 6px 14px;
  border-radius: 20px;
}
.status-badge.pending { background: #fff3e0; color: #ff9800; }
.status-badge.communicating { background: #e3f2fd; color: #2196f3; }
.status-badge.interviewing { background: #e8f5e9; color: #4caf50; }
.status-badge.rejected { background: #ffebee; color: #d32f2f; }
.status-badge.hired { background: #f3e5f5; color: #9c27b0; }
.job-title {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 12px;
}
.job-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.job-meta span {
  font-size: 14px;
  color: #666;
}
.candidate-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}
.candidate-icon {
  font-size: 32px;
}
.candidate-name {
  font-size: 18px;
  font-weight: 600;
}
.candidate-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-bottom: 20px;
  font-size: 14px;
  color: #666;
}
.resume-section {
  background: #fafafa;
  padding: 16px;
  border-radius: 8px;
}
.resume-section h4 {
  font-size: 14px;
  margin-bottom: 12px;
}
.resume-section pre {
  font-size: 13px;
  line-height: 1.6;
  color: #666;
  white-space: pre-wrap;
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
.chat-card {
  display: flex;
  flex-direction: column;
  height: 600px;
}
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  margin-bottom: 16px;
}
.message {
  margin-bottom: 16px;
}
.message.company {
  text-align: right;
}
.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  font-size: 12px;
}
.message.company .message-header {
  flex-direction: row-reverse;
}
.sender-name {
  font-weight: 500;
}
.send-time {
  color: #999;
}
.message-content {
  display: inline-block;
  padding: 10px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
  max-width: 80%;
}
.message.candidate .message-content {
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 12px 12px 12px 0;
}
.message.company .message-content {
  background: #667eea;
  color: white;
  border-radius: 12px 12px 0 12px;
}
.message-input-container {
  border-top: 1px solid #eee;
  padding-top: 16px;
}
.message-input-container textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  resize: vertical;
}
.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}
.hint {
  font-size: 12px;
  color: #999;
}
.btn-send {
  padding: 10px 24px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
</style>