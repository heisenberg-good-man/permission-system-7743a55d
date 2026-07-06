<template>
  <div class="job-detail-page">
    <button class="btn-back" @click="$router.back()">← 返回列表</button>
    <div class="job-detail" v-if="job">
      <div class="job-header">
        <div class="job-title">{{ job.title }}</div>
        <div class="job-status" :class="job.status">{{ job.status === 'active' ? '招聘中' : '已关闭' }}</div>
      </div>
      <div class="job-meta">
        <span class="meta-item">🏢 {{ job.company }}</span>
        <span class="meta-item">📍 {{ job.city }}</span>
        <span class="meta-item">💰 {{ job.salary_min }}-{{ job.salary_max }}K</span>
        <span class="meta-item">📅 {{ job.experience }}</span>
        <span class="meta-item">🎓 {{ job.education }}</span>
      </div>
      <div class="job-tags">
        <span v-for="tag in job.tags" :key="tag" class="tag">{{ tag }}</span>
      </div>
      <div class="job-section">
        <h3>职位描述</h3>
        <p>{{ job.description }}</p>
      </div>
      <div class="job-section">
        <h3>任职要求</h3>
        <pre>{{ job.requirements }}</pre>
      </div>
      <div class="job-section">
        <h3>联系方式</h3>
        <p>📧 {{ job.contact_email }}</p>
      </div>
      <div class="apply-section">
        <button class="btn-apply" :disabled="job.status !== 'active'" @click="showApplyModal = true">
          {{ job.status === 'active' ? '立即投递' : '职位已关闭' }}
        </button>
      </div>
    </div>
    <div class="modal-overlay" v-if="showApplyModal" @click="showApplyModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>投递简历</h3>
          <button class="btn-close" @click="showApplyModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>选择候选人</label>
            <select v-model="applyForm.candidate_id">
              <option value="">请选择候选人</option>
              <option v-for="candidate in candidates" :key="candidate.id" :value="candidate.id">
                {{ candidate.name }} - {{ candidate.email }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>自荐信</label>
            <textarea v-model="applyForm.cover_letter" rows="4" placeholder="请输入您的自荐信..."></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showApplyModal = false">取消</button>
          <button class="btn-submit" @click="submitApplication">确认投递</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { jobsApi, candidatesApi, applicationsApi } from '../api'

const route = useRoute()
const job = ref(null)
const candidates = ref([])
const showApplyModal = ref(false)
const applyForm = ref({
  candidate_id: '',
  cover_letter: ''
})

const loadJob = async () => {
  try {
    const res = await jobsApi.getJob(route.params.id)
    job.value = res.data
  } catch (error) {
    console.error('Failed to load job:', error)
  }
}

const loadCandidates = async () => {
  try {
    const res = await candidatesApi.getCandidates()
    candidates.value = res.data
  } catch (error) {
    console.error('Failed to load candidates:', error)
  }
}

const submitApplication = async () => {
  if (!applyForm.value.candidate_id) {
    alert('请选择候选人')
    return
  }
  try {
    await applicationsApi.createApplication({
      job_id: route.params.id,
      candidate_id: applyForm.value.candidate_id,
      cover_letter: applyForm.value.cover_letter
    })
    alert('投递成功！')
    showApplyModal.value = false
    applyForm.value = { candidate_id: '', cover_letter: '' }
  } catch (error) {
    console.error('Failed to submit application:', error)
    alert('投递失败，请重试')
  }
}

onMounted(() => {
  loadJob()
  loadCandidates()
})
</script>

<style scoped>
.job-detail-page {
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
.job-detail {
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.job-title {
  font-size: 32px;
  font-weight: bold;
}
.job-status {
  font-size: 14px;
  padding: 6px 16px;
  border-radius: 20px;
}
.job-status.active {
  background: #e8f5e9;
  color: #4caf50;
}
.job-status.closed {
  background: #f5f5f5;
  color: #999;
}
.job-meta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}
.meta-item {
  font-size: 14px;
  color: #666;
}
.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 32px;
}
.tag {
  font-size: 14px;
  padding: 6px 14px;
  background: #f0f5ff;
  border-radius: 6px;
  color: #667eea;
}
.job-section {
  margin-bottom: 32px;
}
.job-section h3 {
  font-size: 18px;
  margin-bottom: 12px;
  color: #333;
}
.job-section p, .job-section pre {
  font-size: 15px;
  line-height: 1.8;
  color: #666;
}
.job-section pre {
  white-space: pre-wrap;
  background: #fafafa;
  padding: 16px;
  border-radius: 8px;
}
.apply-section {
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid #eee;
}
.btn-apply {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}
.btn-apply:hover:not(:disabled) {
  transform: translateY(-2px);
}
.btn-apply:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  background: white;
  width: 90%;
  max-width: 500px;
  border-radius: 12px;
  overflow: hidden;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #eee;
}
.modal-header h3 {
  font-size: 18px;
}
.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}
.modal-body {
  padding: 24px;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
}
.form-group select, .form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}
.form-group textarea {
  resize: vertical;
}
.modal-footer {
  display: flex;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #eee;
}
.btn-cancel {
  flex: 1;
  padding: 12px;
  background: #f5f5f5;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.btn-submit {
  flex: 1;
  padding: 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
</style>