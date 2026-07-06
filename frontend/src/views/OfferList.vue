<template>
  <div class="offer-list-page">
    <div class="page-header">
      <h1>Offer管理</h1>
      <p>查看和管理Offer发放情况</p>
    </div>
    <div class="stats-bar">
      <div class="stat-item">
        <div class="stat-value">{{ stats.total || 0 }}</div>
        <div class="stat-label">总Offer</div>
      </div>
      <div class="stat-item">
        <div class="stat-value pending">{{ stats.pending || 0 }}</div>
        <div class="stat-label">待确认</div>
      </div>
      <div class="stat-item">
        <div class="stat-value accepted">{{ stats.accepted || 0 }}</div>
        <div class="stat-label">已接受</div>
      </div>
      <div class="stat-item">
        <div class="stat-value rejected">{{ stats.rejected || 0 }}</div>
        <div class="stat-label">已拒绝</div>
      </div>
    </div>
    <div class="filters">
      <div class="filter-item">
        <label>状态</label>
        <select v-model="filters.status" @change="loadOffers">
          <option value="">全部状态</option>
          <option value="pending">待确认</option>
          <option value="accepted">已接受</option>
          <option value="rejected">已拒绝</option>
          <option value="withdrawn">已撤回</option>
          <option value="pending_onboarding">待入职</option>
        </select>
      </div>
      <div class="filter-item">
        <label>职位搜索</label>
        <input type="text" v-model="filters.keyword" placeholder="搜索职位名称" @keyup.enter="loadOffers" />
      </div>
      <button class="btn-search" @click="loadOffers">🔍 搜索</button>
      <button class="btn-reset" @click="resetFilters">重置</button>
    </div>
    <div class="results-info">
      共 {{ offers.length }} 份Offer
    </div>
    <div class="offer-list">
      <div v-for="offer in offers" :key="offer.id" class="offer-card" @click="$router.push(`/offers/${offer.id}`)">
        <div class="card-header">
          <div class="offer-info">
            <div class="offer-title">{{ offer.position_title }}</div>
            <div class="offer-meta">
              <span class="salary">💰 {{ offer.salary_min }}K-{{ offer.salary_max }}K</span>
              <span class="start-date">📅 {{ formatDate(offer.start_date) }}</span>
            </div>
          </div>
          <span class="status-badge" :class="offer.status">{{ getStatusText(offer.status) }}</span>
        </div>
        <div class="card-body">
          <div class="participants">
            <span>👤 {{ getCandidateName(offer.application_id) }}</span>
            <span>🏢 {{ getCompanyName(offer.application_id) }}</span>
          </div>
          <div class="notes" v-if="offer.notes">{{ offer.notes }}</div>
        </div>
        <div class="card-footer">
          <span class="created-time">创建于 {{ formatDate(offer.created_at) }}</span>
          <span class="arrow">→</span>
        </div>
      </div>
    </div>
    <div class="empty-state" v-if="offers.length === 0">
      <div class="empty-icon">📋</div>
      <div class="empty-text">暂无Offer记录</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { offersApi, applicationsApi, jobsApi, candidatesApi } from '../api'

const offers = ref([])
const applications = ref({})
const jobs = ref({})
const candidates = ref({})
const filters = ref({
  status: '',
  keyword: ''
})

const stats = computed(() => {
  return {
    total: offers.value.length,
    pending: offers.value.filter(o => o.status === 'pending').length,
    accepted: offers.value.filter(o => o.status === 'accepted').length,
    rejected: offers.value.filter(o => o.status === 'rejected').length
  }
})

const getCandidateName = (appId) => {
  return candidates.value[appId] || appId
}

const getCompanyName = (appId) => {
  return jobs.value[appId] || appId
}

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

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

const loadOffers = async () => {
  try {
    const params = {}
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.keyword) params.keyword = filters.value.keyword
    const res = await offersApi.getOffers(params)
    offers.value = res.data
    
    const appIds = [...new Set(offers.value.map(o => o.application_id))]
    const appPromises = appIds.map(id => applicationsApi.getApplication(id))
    const appResults = await Promise.all(appPromises)
    appResults.forEach(res => {
      applications.value[res.data.id] = res.data
    })
    
    const jobIds = [...new Set(appResults.map(r => r.data.job_id))]
    const jobPromises = jobIds.map(id => jobsApi.getJob(id))
    const jobResults = await Promise.all(jobPromises)
    jobResults.forEach(res => {
      jobs.value[res.data.id] = res.data.company
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
    console.error('Failed to load offers:', error)
  }
}

const resetFilters = () => {
  filters.value = { status: '', keyword: '' }
  loadOffers()
}

onMounted(() => {
  loadOffers()
})
</script>

<style scoped>
.offer-list-page {
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
.stat-value.accepted {
  color: #4caf50;
}
.stat-value.rejected {
  color: #d32f2f;
}
.stat-label {
  font-size: 14px;
  color: #999;
  margin-top: 4px;
}
.filters {
  display: flex;
  gap: 16px;
  align-items: flex-end;
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
.filter-item select, .filter-item input {
  padding: 8px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 13px;
  min-width: 150px;
}
.btn-search, .btn-reset {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
}
.btn-search {
  background: #667eea;
  color: white;
  border-color: #667eea;
}
.results-info {
  font-size: 14px;
  color: #999;
  margin-bottom: 16px;
}
.offer-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.offer-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.offer-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}
.offer-title {
  font-size: 18px;
  font-weight: 600;
}
.offer-meta {
  display: flex;
  gap: 20px;
  margin-top: 8px;
}
.offer-meta span {
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