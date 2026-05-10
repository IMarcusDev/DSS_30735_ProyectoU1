<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import AuthBrandPanel from '../components/AuthBrandPanel.vue'
import { api, ApiError } from '../services/api'
import { useAuth } from '../composables/useAuth'

const router = useRouter()
const { setToken, isAdmin } = useAuth()

const email        = ref('')
const password     = ref('')
const rememberMe   = ref(false)
const showPassword = ref(false)
const loading      = ref(false)
const globalError  = ref('')
const fieldErrors  = ref({ email: '', password: '' })

function validate() {
  fieldErrors.value = { email: '', password: '' }
  let valid = true
  if (!email.value) {
    fieldErrors.value.email = 'El email es requerido'
    valid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    fieldErrors.value.email = 'Ingresa un email válido'
    valid = false
  }
  if (!password.value) {
    fieldErrors.value.password = 'La contraseña es requerida'
    valid = false
  }
  return valid
}

async function handleLogin() {
  globalError.value = ''
  if (!validate()) return
  loading.value = true
  try {
    const res = await api.post<{ access_token: string; token_type: string }>(
      '/auth/login',
      { email: email.value, password: password.value }
    )
    setToken(res.access_token)
    router.push(isAdmin.value ? '/supervisor/dashboard' : '/user/dashboard')
  } catch (err) {
    if (err instanceof ApiError && err.status === 401) {
      globalError.value = 'Email o contraseña incorrectos'
      fieldErrors.value.password = 'Contraseña incorrecta'
    } else if (err instanceof ApiError && err.status === 429) {
      globalError.value = 'Demasiados intentos. Espera un momento.'
    } else {
      globalError.value = 'Error de conexión. Intenta de nuevo.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <AuthBrandPanel class="auth-page__brand" />

    <div class="auth-page__form-panel">
      <form class="auth-form" @submit.prevent="handleLogin" novalidate>

        <p class="form-tag">BIENVENIDO DE NUEVO</p>
        <h2 class="form-heading">Iniciar Sesión</h2>
        <p class="form-sub">Accede a tu galería y a tus álbumes aprobados</p>

        <div v-if="globalError" class="alert alert--error" role="alert">
          <span class="alert__icon">⚠</span>
          {{ globalError }}
        </div>

        <div class="field" :class="{ 'field--error': fieldErrors.email, 'field--valid': !fieldErrors.email && email }">
          <label class="field__label" for="login-email">
            Email <span class="required">*</span>
          </label>
          <div class="field__input-wrap">
            <input
              id="login-email"
              v-model="email"
              type="email"
              placeholder="tu@correo.com"
              autocomplete="email"
              class="field__input"
            />
            <span v-if="!fieldErrors.email && email" class="field__icon field__icon--valid">✓</span>
          </div>
          <p v-if="fieldErrors.email" class="field__error">⚠ {{ fieldErrors.email }}</p>
        </div>

        <div class="field" :class="{ 'field--error': fieldErrors.password }">
          <label class="field__label" for="login-password">
            Contraseña <span class="required">*</span>
          </label>
          <div class="field__input-wrap">
            <input
              id="login-password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="••••••••"
              autocomplete="current-password"
              class="field__input"
            />
            <button
              type="button"
              class="field__icon field__icon--toggle"
              @click="showPassword = !showPassword"
              :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
            >
              {{ showPassword ? '🙈' : '👁' }}
            </button>
          </div>
          <p v-if="fieldErrors.password" class="field__error">{{ fieldErrors.password }}</p>
        </div>

        <div class="form-row">
          <label class="checkbox-label">
            <input v-model="rememberMe" type="checkbox" class="checkbox" />
            Recordarme
          </label>
          <span class="link-muted link-muted--disabled">¿Olvidaste tu contraseña?</span>
        </div>

        <button type="submit" class="btn btn--primary" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          <span v-else>Iniciar Sesión &nbsp;→</span>
        </button>

        <div class="divider"><span>o</span></div>

        <button type="button" class="btn btn--outline" disabled title="Próximamente">
          &nbsp;Continuar con Google
        </button>

        <p class="form-footer">
          ¿No tienes cuenta?
          <RouterLink to="/register" class="link-primary">Regístrate gratis</RouterLink>
        </p>

        <div class="demo-section">
          <p class="demo-label">Acceso demo por rol</p>
          <div class="demo-btns">
            <RouterLink to="/galeria" class="demo-btn demo-btn--visitor">
              <span class="demo-dot demo-dot--visitor"></span>
              Visitante
            </RouterLink>
          </div>
        </div>

      </form>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.auth-page {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
  font-family: 'Inter', system-ui, sans-serif;
}

.auth-page__form-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F9FAFB;
  padding: 2rem 1.5rem;
}

.auth-form {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.form-tag {
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #2E75B6;
  margin: 0;
}

.form-heading {
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
  margin: 0;
  line-height: 1.15;
}

.form-sub {
  font-size: 0.875rem;
  color: #6B7280;
  margin: 0 0 0.5rem;
}

.alert {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.7rem 1rem;
  border-radius: 6px;
  font-size: 0.85rem;
}

.alert--error {
  background: #FEF2F2;
  border: 1px solid #FECACA;
  color: #B91C1C;
}

.alert__icon { font-size: 0.9rem; }

.alert__link {
  color: #B91C1C;
  font-weight: 600;
  text-decoration: underline;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.field__label {
  font-size: 0.85rem;
  font-weight: 500;
  color: #374151;
}

.required { color: #EF4444; }

.field__input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.field__input {
  width: 100%;
  padding: 0.65rem 2.5rem 0.65rem 0.85rem;
  border: 1.5px solid #D1D5DB;
  border-radius: 7px;
  font-family: inherit;
  font-size: 0.9rem;
  color: #111827;
  background: white;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  box-sizing: border-box;
  outline: none;
}

.field__input:focus {
  border-color: #2E75B6;
  box-shadow: 0 0 0 3px rgba(46, 117, 182, 0.15);
}

.field--valid .field__input { border-color: #10B981; }
.field--error .field__input { border-color: #EF4444; }
.field--error .field__input:focus { box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15); }

.field__icon {
  position: absolute;
  right: 0.75rem;
  font-size: 0.85rem;
}

.field__icon--valid { color: #10B981; pointer-events: none; }

.field__icon--toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  font-size: 1rem;
}

.field__error {
  font-size: 0.78rem;
  color: #EF4444;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.form-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.85rem;
  color: #374151;
  cursor: pointer;
}

.checkbox {
  width: 15px;
  height: 15px;
  accent-color: #2E75B6;
  cursor: pointer;
}

.link-muted {
  font-size: 0.82rem;
  color: #2E75B6;
  text-decoration: none;
}

.link-muted:hover { text-decoration: underline; }
.link-muted--disabled { cursor: default; opacity: 0.5; pointer-events: none; }

.link-primary {
  color: #2E75B6;
  font-weight: 600;
  text-decoration: none;
}

.link-primary:hover { text-decoration: underline; }

.btn {
  width: 100%;
  padding: 0.8rem 1rem;
  border-radius: 7px;
  font-family: inherit;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.btn--primary {
  background: #2E75B6;
  color: white;
  border: none;
  box-shadow: 0 2px 8px rgba(46, 117, 182, 0.35);
}

.btn--primary:hover:not(:disabled) {
  background: #1E4D7B;
  box-shadow: 0 4px 14px rgba(30, 77, 123, 0.4);
}

.btn--primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn--outline {
  background: white;
  color: #374151;
  border: 1.5px solid #D1D5DB;
}

.btn--outline:hover:not(:disabled) {
  background: #F3F4F6;
  border-color: #9CA3AF;
}

.btn--outline:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2.5px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.divider {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #9CA3AF;
  font-size: 0.8rem;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #E5E7EB;
}

.form-footer {
  text-align: center;
  font-size: 0.85rem;
  color: #6B7280;
  margin: 0;
}

.demo-section {
  border-top: 1px dashed #E5E7EB;
  padding-top: 1rem;
}

.demo-label {
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #9CA3AF;
  text-align: center;
  margin: 0 0 0.65rem;
}

.demo-btns {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 0.5rem;
}

.demo-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.5rem 0.5rem;
  border-radius: 7px;
  font-family: inherit;
  font-size: 0.78rem;
  font-weight: 600;
  text-decoration: none;
  border: 1.5px solid #E5E7EB;
  background: white;
  color: #374151;
  transition: all 0.15s;
}

.demo-btn:hover { border-color: #9CA3AF; background: #F9FAFB; }

.demo-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.demo-dot--visitor    { background: #10B981; }
.demo-dot--user       { background: #2E75B6; }
.demo-dot--supervisor { background: #F59E0B; }

@media (max-width: 768px) {
  .auth-page {
    grid-template-columns: 1fr;
  }

  .auth-page__brand {
    display: none;
  }
}
</style>
