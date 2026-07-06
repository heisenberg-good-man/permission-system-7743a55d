<template>
  <div class="job-manage-page">
    <div class="page-header">
      <h1>职位管理</h1>
      <button class="btn-add" @click="$router.push('/jobs/create')">+ 发布新职位</button>
    </div>
    <div class="filter-bar">
      <select v-model="statusFilter">
        <option value="">全部状态</option>
        <option value="active">招聘中</option>
        <option value="closed">已关闭</option>
      </select>
    </div>
    <div class="job-table-container">
      <table class="job-table">
        <thead>
          <tr>
            <th>职位名称</th>
            <th>公司</th>
            <th>城市</th>
            <th>薪资</th>
            <th>状态</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in filteredJobs" :key="job.id">
            <td><a href="#" @click.prevent="$router.push(`/jobs/${job.id}`)">{{ job.title }}</a></td>
            <td>{{ job.company }}</td>
            <td>{{ job.city }}</td>
            <td>{{ job.salary_min }}-{{ job.salary_max }}K</td>
            <td>
              <span class="status-badge" :class="job.status">{{ job.status === 'active' ? '招聘中' : '已关闭' }}</span>
            </td>
            <td>{{ formatDate(job.created_at) }}</td>
            <td class="actions">
              <button class="btn-edit" @click="editJob(job)">编辑</button>
              <button class="btn-toggle" @click="toggleStatus(job)">
                {{ job.status === 'active' ? '关闭' : '开启' }}
              </button>
              <button class="btn-delete" @click="deleteJob(job)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="empty-state" v-if="filteredJobs.length === 0">
      <div class="empty-icon">📭</div>
      <div class="empty-text">暂无职位</div>
      <button class="btn-add" @click="$router.push('/jobs/create')">发布第一个职位</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { jobsApi } from '../api'

const jobs = ref([])
const statusFilter = ref('')

const filteredJobs = computed(() => {
  if (!statusFilter.value) return jobs.value
  return jobs.value.filter(job => job.status === statusFilter.value)
})

const loadJobs = async () => {
  try {
    const res = await jobsApi.getJobs()
    jobs.value = res.data
  } catch (error) {
    console.error('Failed to load jobs:', error)
  }
}

const editJob = (job) => {
  alert(`编辑职位: ${job.title}`)
}

const toggleStatus = async (job) => {
  const newStatus = job.status === 'active' ? 'closed' : 'active'
  try {
    await jobsApi.updateJob(job.id, { status: newStatus })
    job.status = newStatus
    alert(`职位已${newStatus === 'active' ? '开启' : '关闭'}`)
  } catch (error) {
    console.error('Failed to update job:', error)
    alert('操作失败，请重试')
  }
}

const deleteJob = async (job) => {
  if (!confirm(`确定要删除职位 "${job.title}" 吗？`)) return
  try {
    await jobsApi.deleteJob(job.id)
    jobs.value = jobs.value.filter(j => j.id !== job.id)
    alert('职位已删除')
  } catch (error) {
    console.error('Failed to delete job:', error)
    alert('删除失败，请重试')
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`
}

onMounted(() => {
  loadJobs()
})
</script>

<style scoped>
.job-manage-page {
  padding: 20px 0;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}
.page-header h1 {
  font-size: 32px;
}
.btn-add {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}
.filter-bar {
  margin-bottom: 20px;
}
.filter-bar select {
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}
.job-table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  overflow: hidden;
}
.job-table {
  width: 100%;
  border-collapse: collapse;
}
.job-table th, .job-table td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}
.job-table th {
  background: #fafafa;
  font-weight: 600;
  font-size: 14px;
  color: #666;
}
.job-table td a {
  color: #667eea;
  text-decoration: none;
}
.status-badge {
  font-size: 12px;
  padding: 4px 12px;
  border-radius: 20px;
}
.status-badge.active {
  background: #e8f5e9;
  color: #4caf50;
}
.status-badge.closed {
  background: #f5f5f5;
  color: #999;
}
.actions {
  display: flex;
  gap: 8px;
}
.btn-edit, .btn-toggle, .btn-delete {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}
.btn-edit {
  background: #f0f0f0;
  color: #666;
}
.btn-toggle {
  background: #e3f2fd;
  color: #1976d2;
}
.btn-delete {
  background: #ffebee;
  color: #d32f2f;
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
  margin-bottom: 24px;
}
</style>