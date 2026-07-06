<template>
  <div class="job-create-page">
    <div class="page-header">
      <h1>发布新职位</h1>
      <p>填写职位信息，开始招聘</p>
    </div>
    <form class="job-form" @submit.prevent="submitJob">
      <div class="form-section">
        <h3>基本信息</h3>
        <div class="form-row">
          <div class="form-group">
            <label>职位名称 *</label>
            <input type="text" v-model="jobForm.title" required placeholder="例如：高级前端工程师" />
          </div>
          <div class="form-group">
            <label>公司名称 *</label>
            <input type="text" v-model="jobForm.company" required placeholder="例如：字节跳动" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>工作城市 *</label>
            <select v-model="jobForm.city" required>
              <option value="">请选择城市</option>
              <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>学历要求 *</label>
            <select v-model="jobForm.education" required>
              <option value="">请选择学历</option>
              <option value="大专">大专</option>
              <option value="本科">本科</option>
              <option value="硕士">硕士</option>
              <option value="博士">博士</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>经验要求 *</label>
            <select v-model="jobForm.experience" required>
              <option value="">请选择经验</option>
              <option value="应届生">应届生</option>
              <option value="1-3年">1-3年</option>
              <option value="3-5年">3-5年</option>
              <option value="5-10年">5-10年</option>
              <option value="10年以上">10年以上</option>
            </select>
          </div>
          <div class="form-group">
            <label>薪资范围 *</label>
            <div class="salary-input">
              <input type="number" v-model="jobForm.salary_min" required placeholder="最低" />
              <span>-</span>
              <input type="number" v-model="jobForm.salary_max" required placeholder="最高" />
              <span>K</span>
            </div>
          </div>
        </div>
      </div>
      <div class="form-section">
        <h3>职位详情</h3>
        <div class="form-group">
          <label>职位描述 *</label>
          <textarea v-model="jobForm.description" rows="4" required placeholder="请描述职位的主要职责和工作内容..."></textarea>
        </div>
        <div class="form-group">
          <label>任职要求 *</label>
          <textarea v-model="jobForm.requirements" rows="6" required placeholder="请列出主要的任职要求，每行一条..."></textarea>
        </div>
      </div>
      <div class="form-section">
        <h3>标签与联系</h3>
        <div class="form-group">
          <label>技能标签</label>
          <input type="text" v-model="tagsInput" placeholder="输入标签后按回车添加" @keydown.enter.prevent="addTag" />
          <div class="tags-list">
            <span v-for="(tag, index) in jobForm.tags" :key="index" class="tag">
              {{ tag }}
              <button type="button" @click="removeTag(index)">×</button>
            </span>
          </div>
        </div>
        <div class="form-group">
          <label>联系邮箱 *</label>
          <input type="email" v-model="jobForm.contact_email" required placeholder="hr@company.com" />
        </div>
      </div>
      <div class="form-actions">
        <button type="button" class="btn-cancel" @click="$router.push('/jobs/manage')">取消</button>
        <button type="submit" class="btn-submit">发布职位</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { jobsApi, optionsApi } from '../api'

const jobForm = ref({
  title: '',
  company: '',
  city: '',
  education: '',
  experience: '',
  salary_min: '',
  salary_max: '',
  description: '',
  requirements: '',
  tags: [],
  contact_email: ''
})

const tagsInput = ref('')
const cities = ref([])

const loadCities = async () => {
  try {
    const res = await optionsApi.getCities()
    cities.value = res.data
  } catch (error) {
    console.error('Failed to load cities:', error)
  }
}

const addTag = () => {
  const tag = tagsInput.value.trim()
  if (tag && !jobForm.value.tags.includes(tag)) {
    jobForm.value.tags.push(tag)
    tagsInput.value = ''
  }
}

const removeTag = (index) => {
  jobForm.value.tags.splice(index, 1)
}

const submitJob = async () => {
  if (!jobForm.value.title || !jobForm.value.company || !jobForm.value.city) {
    alert('请填写必填项')
    return
  }
  try {
    await jobsApi.createJob(jobForm.value)
    alert('职位发布成功！')
    $router.push('/jobs/manage')
  } catch (error) {
    console.error('Failed to create job:', error)
    alert('发布失败，请重试')
  }
}

onMounted(() => {
  loadCities()
})
</script>

<style scoped>
.job-create-page {
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
.job-form {
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.form-section {
  margin-bottom: 32px;
}
.form-section h3 {
  font-size: 18px;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
}
.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
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
.form-group input, .form-group select, .form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}
.form-group textarea {
  resize: vertical;
}
.salary-input {
  display: flex;
  align-items: center;
  gap: 10px;
}
.salary-input input {
  flex: 1;
  max-width: 100px;
}
.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
}
.tag {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  padding: 6px 12px;
  background: #f0f5ff;
  color: #667eea;
  border-radius: 6px;
}
.tag button {
  background: none;
  border: none;
  color: #667eea;
  font-size: 16px;
  cursor: pointer;
}
.form-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid #eee;
}
.btn-cancel {
  padding: 12px 32px;
  background: #f5f5f5;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
.btn-submit {
  padding: 12px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}
</style>