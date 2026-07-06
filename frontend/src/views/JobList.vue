<template>
  <div class="job-list-page">
    <div class="page-header">
      <h1>职位列表</h1>
      <p>找到适合您的工作机会</p>
    </div>
    <div class="filters">
      <div class="filter-item">
        <label>城市</label>
        <select v-model="filters.city">
          <option value="">全部城市</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>
      <div class="filter-item">
        <label>状态</label>
        <select v-model="filters.status">
          <option value="">全部状态</option>
          <option value="active">招聘中</option>
          <option value="closed">已关闭</option>
        </select>
      </div>
      <div class="filter-item search">
        <input type="text" v-model="filters.keyword" placeholder="搜索职位名称或公司..." />
        <button class="btn-search" @click="loadJobs">🔍</button>
      </div>
      <button class="btn-reset" @click="resetFilters">重置筛选</button>
    </div>
    <div class="results-info">
      共 {{ jobs.length }} 个职位
    </div>
    <div class="job-grid">
      <div class="job-card" v-for="job in jobs" :key="job.id" @click="$router.push(`/jobs/${job.id}`)">
        <div class="job-header">
          <div class="job-title">{{ job.title }}</div>
          <div class="job-status" :class="job.status">{{ job.status === 'active' ? '招聘中' : '已关闭' }}</div>
        </div>
        <div class="job-company">{{ job.company }}</div>
        <div class="job-info">
          <span class="job-city">{{ job.city }}</span>
          <span class="job-experience">{{ job.experience }}</span>
          <span class="job-education">{{ job.education }}</span>
        </div>
        <div class="job-salary">{{ job.salary_min }}-{{ job.salary_max }}K</div>
        <div class="job-tags">
          <span v-for="tag in job.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
        <div class="job-desc">{{ job.description }}</div>
        <div class="job-footer">
          <span>更新于 {{ formatDate(job.updated_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { jobsApi, optionsApi } from '../api'

const jobs = ref([])
const cities = ref([])
const filters = ref({
  city: '',
  status: '',
  keyword: ''
})

const loadJobs = async () => {
  try {
    const params = {}
    if (filters.value.city) params.city = filters.value.city
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.keyword) params.keyword = filters.value.keyword
    const res = await jobsApi.getJobs(params)
    jobs.value = res.data
  } catch (error) {
    console.error('Failed to load jobs:', error)
  }
}

const loadCities = async () => {
  try {
    const res = await optionsApi.getCities()
    cities.value = res.data
  } catch (error) {
    console.error('Failed to load cities:', error)
  }
}

const resetFilters = () => {
  filters.value = { city: '', status: '', keyword: '' }
  loadJobs()
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()}`
}

onMounted(() => {
  loadJobs()
  loadCities()
})
</script>

<style scoped>
.job-list-page {
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
  gap: 20px;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.filter-item label {
  font-size: 14px;
  font-weight: 500;
}
.filter-item select, .filter-item input {
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  min-width: 150px;
}
.filter-item.search {
  flex-direction: row;
  flex: 1;
  max-width: 400px;
}
.filter-item.search input {
  flex: 1;
}
.btn-search {
  padding: 10px 16px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 0 8px 8px 0;
  cursor: pointer;
}
.btn-reset {
  padding: 10px 20px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.results-info {
  font-size: 14px;
  color: #999;
  margin-bottom: 20px;
}
.job-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}
.job-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.job-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.job-title {
  font-size: 18px;
  font-weight: 600;
}
.job-status {
  font-size: 12px;
  padding: 4px 12px;
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
.job-company {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}
.job-info {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}
.job-city, .job-experience, .job-education {
  font-size: 14px;
  color: #888;
}
.job-salary {
  font-size: 20px;
  font-weight: bold;
  color: #ff6b6b;
  margin-bottom: 12px;
}
.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}
.tag {
  font-size: 12px;
  padding: 4px 10px;
  background: #f0f0f0;
  border-radius: 4px;
  color: #666;
}
.job-desc {
  font-size: 14px;
  color: #888;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.job-footer {
  font-size: 12px;
  color: #bbb;
}
</style>