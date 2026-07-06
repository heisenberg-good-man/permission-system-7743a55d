<template>
  <div class="candidate-list-page">
    <div class="page-header">
      <h1>候选人管理</h1>
      <p>查看和筛选候选人信息</p>
    </div>
    <div class="filters">
      <div class="filter-item">
        <label>期望城市</label>
        <select v-model="filters.desired_city">
          <option value="">全部城市</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>
      <div class="filter-item">
        <label>工作经验</label>
        <select v-model="filters.experience">
          <option value="">全部经验</option>
          <option value="应届生">应届生</option>
          <option value="1年">1年</option>
          <option value="2年">2年</option>
          <option value="3年">3年</option>
          <option value="4年">4年</option>
          <option value="5年">5年</option>
        </select>
      </div>
      <div class="filter-item">
        <label>期望岗位</label>
        <select v-model="filters.desired_job">
          <option value="">全部岗位</option>
          <option v-for="job in desiredJobs" :key="job" :value="job">{{ job }}</option>
        </select>
      </div>
      <div class="filter-item">
        <label>状态</label>
        <select v-model="filters.status">
          <option value="">全部状态</option>
          <option value="active">活跃</option>
          <option value="inactive">已停用</option>
        </select>
      </div>
      <div class="filter-item search">
        <input type="text" v-model="filters.keyword" placeholder="搜索姓名、技能..." />
        <button class="btn-search" @click="loadCandidates">🔍</button>
      </div>
      <button class="btn-reset" @click="resetFilters">重置筛选</button>
    </div>
    <div class="results-info">
      共 {{ candidates.length }} 位候选人
    </div>
    <div class="candidate-grid">
      <div class="candidate-card" v-for="candidate in candidates" :key="candidate.id" @click="$router.push(`/candidates/${candidate.id}`)">
        <div class="candidate-header">
          <div class="candidate-icon">👤</div>
          <div class="candidate-info">
            <div class="candidate-name">{{ candidate.name }}</div>
            <div class="candidate-meta">{{ candidate.email }} | {{ candidate.phone }}</div>
          </div>
          <div class="candidate-status" :class="candidate.status">{{ candidate.status === 'active' ? '活跃' : '已停用' }}</div>
        </div>
        <div class="candidate-detail">
          <div class="detail-row">
            <span>🎓 {{ candidate.education }}</span>
            <span>📅 {{ candidate.experience }}经验</span>
            <span>📍 {{ candidate.desired_city }}</span>
          </div>
          <div class="desired-job">
            <strong>期望岗位：</strong>{{ candidate.desired_job }}
          </div>
          <div class="skills">
            <span v-for="skill in candidate.skills.slice(0, 4)" :key="skill" class="skill-tag">{{ skill }}</span>
            <span v-if="candidate.skills.length > 4" class="skill-more">+{{ candidate.skills.length - 4 }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="empty-state" v-if="candidates.length === 0">
      <div class="empty-icon">👥</div>
      <div class="empty-text">暂无候选人</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { candidatesApi } from '../api'

const candidates = ref([])
const cities = ref(['北京', '上海', '杭州', '深圳'])
const desiredJobs = ref(['前端工程师', '后端开发工程师', '产品经理', 'UI设计师', '技术总监'])
const filters = ref({
  desired_city: '',
  experience: '',
  desired_job: '',
  status: '',
  keyword: ''
})

const loadCandidates = async () => {
  try {
    const params = {}
    if (filters.value.desired_city) params.desired_city = filters.value.desired_city
    if (filters.value.experience) params.experience = filters.value.experience
    if (filters.value.desired_job) params.desired_job = filters.value.desired_job
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.keyword) params.keyword = filters.value.keyword
    const res = await candidatesApi.getCandidates(params)
    candidates.value = res.data
  } catch (error) {
    console.error('Failed to load candidates:', error)
  }
}

const resetFilters = () => {
  filters.value = {
    desired_city: '',
    experience: '',
    desired_job: '',
    status: '',
    keyword: ''
  }
  loadCandidates()
}

onMounted(() => {
  loadCandidates()
})
</script>

<style scoped>
.candidate-list-page {
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
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
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
.filter-item select, .filter-item input {
  padding: 8px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 13px;
  min-width: 120px;
}
.filter-item.search {
  flex-direction: row;
  flex: 1;
  max-width: 300px;
}
.filter-item.search input {
  flex: 1;
}
.btn-search {
  padding: 8px 14px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 0 6px 6px 0;
  cursor: pointer;
}
.btn-reset {
  padding: 8px 16px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
}
.results-info {
  font-size: 14px;
  color: #999;
  margin-bottom: 16px;
}
.candidate-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.candidate-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.candidate-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
.candidate-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}
.candidate-icon {
  font-size: 40px;
}
.candidate-info {
  flex: 1;
}
.candidate-name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}
.candidate-meta {
  font-size: 13px;
  color: #999;
}
.candidate-status {
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 16px;
}
.candidate-status.active {
  background: #e8f5e9;
  color: #4caf50;
}
.candidate-status.inactive {
  background: #f5f5f5;
  color: #999;
}
.candidate-detail {
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}
.detail-row {
  display: flex;
  gap: 16px;
  margin-bottom: 10px;
  font-size: 13px;
  color: #666;
}
.desired-job {
  font-size: 14px;
  color: #333;
  margin-bottom: 12px;
}
.skills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.skill-tag {
  font-size: 12px;
  padding: 4px 10px;
  background: #f0f5ff;
  color: #667eea;
  border-radius: 4px;
}
.skill-more {
  font-size: 12px;
  color: #999;
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