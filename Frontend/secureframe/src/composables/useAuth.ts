import { ref, computed } from 'vue'
import { api } from '../services/api'

export interface AuthUser {
  user_id:   string
  role:      string
  name?:     string
  last_name?: string
  email?:    string
}

const token = ref<string | null>(localStorage.getItem('access_token'))
const user  = ref<AuthUser | null>(null)

function decodeRole(t: string): string {
  try {
    const payload = JSON.parse(atob(t.split('.')[1]!))
    return payload.role ?? ''
  } catch {
    return ''
  }
}

if (token.value) {
  user.value = { user_id: '', role: decodeRole(token.value) }
}

export function useAuth() {
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'Administrator')

  function setToken(t: string) {
    token.value = t
    localStorage.setItem('access_token', t)
    user.value = { user_id: '', role: decodeRole(t) }
  }

  async function fetchMe() {
    if (!token.value) return
    try {
      const me = await api.get<AuthUser>('/auth/me')
      user.value = me
    } catch {
      // Token expired or invalid managed for api.ts
    }
  }

  function logout() {
    token.value = null
    user.value  = null
    localStorage.removeItem('access_token')
  }

  return { token, user, isAuthenticated, isAdmin, setToken, fetchMe, logout }
}
