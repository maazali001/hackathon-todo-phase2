const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://electronic-bessy-mazzali001-d766a150.koyeb.app'

export interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

export interface User {
  id: string
  email: string
  name: string
  token?: string
}

// Helper to get token from cookies
function getToken(): string | null {
  if (typeof document === 'undefined') return null
  const cookies = document.cookie.split('; ')
  const tokenCookie = cookies.find(c => c.startsWith('token='))
  return tokenCookie ? tokenCookie.split('=')[1] : null
}

// Helper to set token
export function setToken(token: string) {
  if (typeof document !== 'undefined') {
    document.cookie = `token=${token}; path=/; max-age=${60*60*24*7}` // 7 days
  }
}

// Helper to get user_id from cookies
export function getUserId(): string | null {
  if (typeof document === 'undefined') return null
  const cookies = document.cookie.split('; ')
  const userCookie = cookies.find(c => c.startsWith('user_id='))
  return userCookie ? userCookie.split('=')[1] : null
}

// Helper to set user_id
export function setUserId(userId: string) {
  if (typeof document !== 'undefined') {
    document.cookie = `user_id=${userId}; path=/; max-age=${60*60*24*7}` // 7 days
  }
}

// Helper to clear auth
export function clearAuth() {
  if (typeof document !== 'undefined') {
    document.cookie = 'token=; path=/; max-age=0'
    document.cookie = 'user_id=; path=/; max-age=0'
  }
}

// Auth API calls
export async function signup(email: string, password: string, name: string): Promise<User> {
  const response = await fetch(`${API_URL}/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, name })
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Signup failed')
  }
  
  const user = await response.json()
  if (user.token) {
    setToken(user.token)
    setUserId(user.id)
  }
  return user
}

export async function signin(email: string, password: string): Promise<User> {
  const response = await fetch(`${API_URL}/auth/signin`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Login failed')
  }
  
  const user = await response.json()
  if (user.token) {
    setToken(user.token)
    setUserId(user.id)
  }
  return user
}

// Task API calls
export async function getTasks(status: string = 'all'): Promise<Task[]> {
  const token = getToken()
  const userId = getUserId()
  
  if (!token || !userId) throw new Error('Not authenticated')
  
  const response = await fetch(`${API_URL}/api/${userId}/tasks?status=${status}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  
  if (!response.ok) throw new Error('Failed to fetch tasks')
  return response.json()
}

export async function createTask(title: string, description?: string): Promise<Task> {
  const token = getToken()
  const userId = getUserId()
  
  if (!token || !userId) throw new Error('Not authenticated')
  
  const response = await fetch(`${API_URL}/api/${userId}/tasks`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title, description })
  })
  
  if (!response.ok) throw new Error('Failed to create task')
  return response.json()
}

export async function updateTask(taskId: number, title?: string, description?: string): Promise<Task> {
  const token = getToken()
  const userId = getUserId()
  
  if (!token || !userId) throw new Error('Not authenticated')
  
  const response = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title, description })
  })
  
  if (!response.ok) throw new Error('Failed to update task')
  return response.json()
}

export async function deleteTask(taskId: number): Promise<void> {
  const token = getToken()
  const userId = getUserId()
  
  if (!token || !userId) throw new Error('Not authenticated')
  
  const response = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  })
  
  if (!response.ok) throw new Error('Failed to delete task')
}

export async function toggleTaskComplete(taskId: number): Promise<Task> {
  const token = getToken()
  const userId = getUserId()
  
  if (!token || !userId) throw new Error('Not authenticated')
  
  const response = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}/complete`, {
    method: 'PATCH',
    headers: { 'Authorization': `Bearer ${token}` }
  })
  
  if (!response.ok) throw new Error('Failed to toggle task')
  return response.json()
}