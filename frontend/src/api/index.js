import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const statsApi = {
  getStats: () => api.get('/stats')
}

export const jobsApi = {
  getJobs: (params) => api.get('/jobs', { params }),
  getJob: (id) => api.get(`/jobs/${id}`),
  createJob: (data) => api.post('/jobs', data),
  updateJob: (id, data) => api.put(`/jobs/${id}`, data),
  deleteJob: (id) => api.delete(`/jobs/${id}`)
}

export const candidatesApi = {
  getCandidates: (params) => api.get('/candidates', { params }),
  getCandidate: (id) => api.get(`/candidates/${id}`),
  createCandidate: (data) => api.post('/candidates', data)
}

export const applicationsApi = {
  getApplications: (params) => api.get('/applications', { params }),
  getApplication: (id) => api.get(`/applications/${id}`),
  createApplication: (data) => api.post('/applications', data),
  updateStatus: (id, status) => api.put(`/applications/${id}/status`, { status })
}

export const messagesApi = {
  getMessages: (params) => api.get('/messages', { params }),
  createMessage: (data) => api.post('/messages', data)
}

export const interviewsApi = {
  getInterviews: (params) => api.get('/interviews', { params }),
  getInterview: (id) => api.get(`/interviews/${id}`),
  createInterview: (data) => api.post('/interviews', data),
  updateInterview: (id, data) => api.put(`/interviews/${id}`, data),
  updateStatus: (id, status) => api.put(`/interviews/${id}/status`, { status })
}

export const optionsApi = {
  getCities: () => api.get('/cities'),
  getStatuses: () => api.get('/statuses')
}

export default api