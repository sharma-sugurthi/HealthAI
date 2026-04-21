import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
})

export function setAuthToken(token) {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`
  } else {
    delete api.defaults.headers.common.Authorization
  }
}

export async function loginUser(username, password) {
  const { data } = await api.post('/auth/login', { username, password })
  return data
}

export async function registerUser(payload) {
  const { data } = await api.post('/auth/register', payload)
  return data
}

export async function getMe() {
  const { data } = await api.get('/auth/me')
  return data
}

export async function sendMessage(message) {
  const { data } = await api.post('/chat/message', { message })
  return data
}

export async function analyzeSymptoms(symptoms) {
  const { data } = await api.post('/chat/symptoms', { symptoms })
  return data
}

export async function generateTreatmentPlan(condition) {
  const { data } = await api.post('/chat/treatment-plan', { condition })
  return data
}

export async function getChatHistory(limit = 50) {
  const { data } = await api.get('/chat/history', { params: { limit } })
  return data
}

export async function getHealthMetrics(metric_type) {
  const { data } = await api.get('/health/metrics', { params: { metric_type } })
  return data
}

export async function recordHealthMetric(payload) {
  const { data } = await api.post('/health/metrics', payload)
  return data
}

export async function getHealthStats(metric_type) {
  const { data } = await api.get(`/health/statistics/${encodeURIComponent(metric_type)}`)
  return data
}

export async function getTreatmentPlans() {
  const { data } = await api.get('/treatment/plans')
  return data
}

export async function createTreatmentPlan(payload) {
  const { data } = await api.post('/treatment/plans', payload)
  return data
}

export async function getMedicalProfile() {
  const [conditions, medications, allergies, symptoms] = await Promise.all([
    api.get('/medical-history/conditions'),
    api.get('/medical-history/medications'),
    api.get('/medical-history/allergies'),
    api.get('/medical-history/symptoms'),
  ])
  return {
    conditions: conditions.data,
    medications: medications.data,
    allergies: allergies.data,
    symptoms: symptoms.data,
  }
}

export default api
