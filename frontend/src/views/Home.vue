<template>
  <div class="home">
    <div class="hero">
      <h1>发现理想工作</h1>
      <p>连接优秀人才与优质企业</p>
      <button class="btn-primary" @click="$router.push('/jobs')">浏览职位</button>
    </div>
    <div class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">💼</div>
          <div class="stat-value">{{ stats.total_jobs }}</div>
          <div class="stat-label">总职位数</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🔥</div>
          <div class="stat-value">{{ stats.active_jobs }}</div>
          <div class="stat-label">招聘中</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📋</div>
          <div class="stat-value">{{ stats.total_applications }}</div>
          <div class="stat-label">投递记录</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-value">{{ stats.interviewing_applications }}</div>
          <div class="stat-label">面试中</div>
        </div>
      </div>
    </div>
    <div class="quick-actions">
      <h2>快捷入口</h2>
      <div class="action-grid">
        <div class="action-card" @click="$router.push('/jobs')">
          <div class="action-icon">🔍</div>
          <div class="action-title">搜索职位</div>
          <div class="action-desc">按岗位、城市筛选</div>
        </div>
        <div class="action-card" @click="$router.push('/jobs/create')">
          <div class="action-icon">📝</div>
          <div class="action-title">发布职位</div>
          <div class="action-desc">招聘方发布新职位</div>
        </div>
        <div class="action-card" @click="$router.push('/applications')">
          <div class="action-icon">📊</div>
          <div class="action-title">投递管理</div>
          <div class="action-desc">查看投递记录与状态</div>
        </div>
        <div class="action-card" @click="$router.push('/profile')">
          <div class="action-icon">👤</div>
          <div class="action-title">个人中心</div>
          <div class="action-desc">管理个人信息与简历</div>
        </div>
      </div>
    </div>
    <div class="recent-jobs">
      <div class="section-header">
        <h2>最新职位</h2>
        <button class="btn-link" @click="$router.push('/jobs')">查看全部</button>
      </div>
      <div class="job-list">
        <div class="job-card" v-for="job in recentJobs" :key="job.id" @click="$router.push(`/jobs/${job.id}`)">
          <div class="job-header">
            <div class="job-title">{{ job.title }}</div>
            <div class="job-status" :class="job.status">{{ job.status === 'active' ? '招聘中' : '已关闭' }}</div>
          </div>
          <div class="job-company">{{ job.company }}</div>
          <div class="job-info">
            <span class="job-city">{{ job.city }}</span>
            <span class="job-salary">{{ job.salary_min }}-{{ job.salary_max }}K</span>
          </div>
          <div class="job-tags">
            <span v-for="tag in job.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { statsApi, jobsApi } from '../api'

const stats = ref({
  total_jobs: 0,
  active_jobs: 0,
  total_applications: 0,
  interviewing_applications: 0
})
const recentJobs = ref([])

onMounted(async () => {
  try {
    const [statsRes, jobsRes] = await Promise.all([
      statsApi.getStats(),
      jobsApi.getJobs({ status: 'active' })
    ])
    stats.value = statsRes.data
    recentJobs.value = jobsRes.data.slice(0, 4)
  } catch (error) {
    console.error('Failed to load data:', error)
  }
})
</script>

<style scoped>
.home {
  padding: 20px 0;
}
.hero {
  text-align: center;
  padding: 80px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 16px;
  margin-bottom: 32px;
}
.hero h1 {
  font-size: 48px;
  margin-bottom: 16px;
}
.hero p {
  font-size: 20px;
  opacity: 0.9;
  margin-bottom: 32px;
}
.btn-primary {
  background: white;
  color: #667eea;
  border: none;
  padding: 14px 32px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}
.btn-primary:hover {
  transform: translateY(-2px);
}
.stats-section {
  margin-bottom: 32px;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
.stat-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.stat-icon {
  font-size: 32px;
  margin-bottom: 12px;
}
.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}
.stat-label {
  font-size: 14px;
  color: #999;
}
.quick-actions {
  margin-bottom: 32px;
}
.quick-actions h2 {
  font-size: 24px;
  margin-bottom: 20px;
}
.action-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
.action-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
.action-icon {
  font-size: 36px;
  margin-bottom: 12px;
}
.action-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
}
.action-desc {
  font-size: 14px;
  color: #999;
}
.recent-jobs {
  margin-bottom: 32px;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.section-header h2 {
  font-size: 24px;
}
.btn-link {
  background: none;
  border: none;
  color: #667eea;
  font-size: 14px;
  cursor: pointer;
  text-decoration: underline;
}
.job-list {
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
.job-city, .job-salary {
  font-size: 14px;
  color: #888;
}
.job-salary {
  color: #ff6b6b;
  font-weight: 600;
}
.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.tag {
  font-size: 12px;
  padding: 4px 10px;
  background: #f0f0f0;
  border-radius: 4px;
  color: #666;
}
</style>