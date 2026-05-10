<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import AuthBrandPanel from '../components/AuthBrandPanel.vue'
import { api, ApiError } from '../services/api'

const name           = ref('')
const email          = ref('')
const password       = ref('')
const confirmPwd     = ref('')
const acceptTerms    = ref(false)
const showPassword   = ref(false)
const showConfirm    = ref(false)
const loading        = ref(false)
const success        = ref(false)
const fieldErrors    = ref({ name: '', email: '', password: '', confirmPwd: '', terms: '' })

const passwordStrength = computed(() => {
  const pwd = password.value
  if (!pwd) return null
  let score = 0
  if (pwd.length >= 8) score++
  if (pwd.length >= 12) score++
  if (/[A-Z]/.test(pwd)) score++
  if (/[0-9]/.test(pwd)) score++
  if (/[^A-Za-z0-9]/.test(pwd)) score++
  if (score <= 1) return { level: 'débil',  hint: 'agrega mayúsculas y números', color: '#EF4444', pct: '33%' }
  if (score <= 3) return { level: 'media',  hint: 'agrega un símbolo',           color: '#F59E0B', pct: '66%' }
  return              { level: 'fuerte', hint: 'excelente contraseña',        color: '#10B981', pct: '100%' }
})

function validate() {
  fieldErrors.value = { name: '', email: '', password: '', confirmPwd: '', terms: '' }
  let valid = true

  if (!name.value.trim()) {
    fieldErrors.value.name = 'El nombre es requerido'
    valid = false
  }
  if (!email.value) {
    fieldErrors.value.email = 'El email es requerido'
    valid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    fieldErrors.value.email = 'Ingresa un email válido'
    valid = false
  }
  if (password.value.length < 8) {
    fieldErrors.value.password = 'Mínimo 8 caracteres'
    valid = false
  } else if (!/[A-Z]/.test(password.value)) {
    fieldErrors.value.password = 'Debe contener al menos una mayúscula'
    valid = false
  } else if (!/[0-9]/.test(password.value)) {
    fieldErrors.value.password = 'Debe contener al menos un número'
    valid = false
  } else if (!/[^A-Za-z0-9]/.test(password.value)) {
    fieldErrors.value.password = 'Debe contener al menos un símbolo (!@#$%...)'
    valid = false
  }
  if (password.value !== confirmPwd.value) {
    fieldErrors.value.confirmPwd = 'Las contraseñas no coinciden'
    valid = false
  }
  if (!acceptTerms.value) {
    fieldErrors.value.terms = 'Debes aceptar los términos para continuar'
    valid = false
  }
  return valid
}

const registerError = ref('')

async function handleRegister() {
  if (!validate()) return
  loading.value = true
  registerError.value = ''
  try {
    const parts = name.value.trim().split(' ')
    await api.post('/auth/register', {
      name:      parts[0] ?? '',
      last_name: parts.slice(1).join(' ') || parts[0] || '',
      email:     email.value,
      password:  password.value,
    })
    success.value = true
  } catch (err) {
    if (err instanceof ApiError && err.status === 409) {
      fieldErrors.value.email = 'Este email ya está registrado'
    } else if (err instanceof ApiError && err.status === 422) {
      registerError.value = 'La contraseña no cumple los requisitos de seguridad'
    } else if (err instanceof ApiError && err.status === 429) {
      registerError.value = 'Demasiados registros. Espera un momento.'
    } else {
      registerError.value = 'Error de conexión. Intenta de nuevo.'
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
      <form v-if="!success" class="auth-form" @submit.prevent="handleRegister" novalidate>

        <p class="form-tag">CREA TU CUENTA · GRATIS</p>
        <h2 class="form-heading">Comienza a proteger</h2>
        <p class="form-sub">Toma 2 minutos · sin tarjeta de crédito</p>

        <div class="field" :class="{ 'field--error': fieldErrors.name }">
          <label class="field__label" for="reg-name">
            Nombre completo <span class="required">*</span>
          </label>
          <input
            id="reg-name"
            v-model="name"
            type="text"
            placeholder="Tu nombre"
            autocomplete="name"
            class="field__input"
          />
          <p v-if="fieldErrors.name" class="field__error">⚠ {{ fieldErrors.name }}</p>
        </div>

        <div class="field" :class="{ 'field--error': fieldErrors.email, 'field--valid': !fieldErrors.email && email }">
          <label class="field__label" for="reg-email">
            Email <span class="required">*</span>
          </label>
          <div class="field__input-wrap">
            <input
              id="reg-email"
              v-model="email"
              type="email"
              placeholder="tucorreo@empresa.com"
              autocomplete="email"
              class="field__input"
            />
            <span v-if="!fieldErrors.email && email" class="field__icon field__icon--valid">✓</span>
          </div>
          <p v-if="fieldErrors.email" class="field__error">⚠ {{ fieldErrors.email }}</p>
          <p v-else-if="email" class="field__hint">Te enviaremos un correo de confirmación</p>
        </div>

        <div class="field" :class="{ 'field--error': fieldErrors.password }">
          <label class="field__label" for="reg-password">
            Contraseña <span class="required">*</span>
          </label>
          <div class="field__input-wrap">
            <input
              id="reg-password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Mínimo 8 caracteres"
              autocomplete="new-password"
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
          <div v-if="passwordStrength" class="strength-bar">
            <div
              class="strength-bar__fill"
              :style="{ width: passwordStrength.pct, background: passwordStrength.color }"
            ></div>
          </div>
          <p v-if="passwordStrength" class="field__hint">
            Fortaleza: <strong :style="{ color: passwordStrength.color }">{{ passwordStrength.level }}</strong>
            · {{ passwordStrength.hint }}
          </p>
          <p v-if="fieldErrors.password" class="field__error">{{ fieldErrors.password }}</p>
        </div>

        <div class="field" :class="{ 'field--error': fieldErrors.confirmPwd }">
          <label class="field__label" for="reg-confirm">
            Confirmar contraseña <span class="required">*</span>
          </label>
          <div class="field__input-wrap">
            <input
              id="reg-confirm"
              v-model="confirmPwd"
              :type="showConfirm ? 'text' : 'password'"
              placeholder="Repite tu contraseña"
              autocomplete="new-password"
              class="field__input"
            />
            <button
              type="button"
              class="field__icon field__icon--toggle"
              @click="showConfirm = !showConfirm"
              aria-label="Mostrar confirmación"
            >
              {{ showConfirm ? '🙈' : '👁' }}
            </button>
          </div>
          <p v-if="fieldErrors.confirmPwd" class="field__error">{{ fieldErrors.confirmPwd }}</p>
        </div>

        <div>
          <label class="checkbox-label">
            <input v-model="acceptTerms" type="checkbox" class="checkbox" />
            Acepto los
            <a href="#" class="link-primary">términos</a>
            y la
            <a href="#" class="link-primary">política de privacidad</a>
          </label>
          <p v-if="fieldErrors.terms" class="field__error">{{ fieldErrors.terms }}</p>
        </div>

        <div v-if="registerError" class="alert alert--error" role="alert">
          <span>⚠</span> {{ registerError }}
        </div>

        <button type="submit" class="btn btn--primary" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          <span v-else>Crear Cuenta &nbsp;→</span>
        </button>

        <p class="form-footer">
          ¿Ya tienes cuenta?
          <RouterLink to="/login" class="link-primary">Inicia sesión</RouterLink>
        </p>

      </form>

      <div v-else class="success-panel">
        <div class="success-icon">✓</div>
        <h2>¡Cuenta creada!</h2>
        <p>Revisa tu correo para confirmar tu cuenta antes de ingresar.</p>
        <RouterLink to="/login" class="btn btn--primary">Ir a Iniciar Sesión</RouterLink>
      </div>
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
  padding: 2.5rem 1.5rem;
}

.auth-form {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
  margin: 0 0 0.25rem;
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
  transition: border-color 0.15s, box-shadow 0.15s;
  box-sizing: border-box;
  outline: none;
}

.field > .field__input {
  padding-right: 0.85rem;
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
  font-size: 1rem;
  line-height: 1;
}

.field__error {
  font-size: 0.78rem;
  color: #EF4444;
  margin: 0;
}

.field__hint {
  font-size: 0.78rem;
  color: #6B7280;
  margin: 0;
}

.strength-bar {
  height: 4px;
  background: #E5E7EB;
  border-radius: 99px;
  overflow: hidden;
}

.strength-bar__fill {
  height: 100%;
  border-radius: 99px;
  transition: width 0.3s ease, background 0.3s ease;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.85rem;
  color: #374151;
  flex-wrap: wrap;
  cursor: pointer;
}

.checkbox {
  width: 15px;
  height: 15px;
  accent-color: #2E75B6;
  flex-shrink: 0;
  cursor: pointer;
}

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
  text-decoration: none;
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

.spinner {
  width: 18px;
  height: 18px;
  border: 2.5px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.form-footer {
  text-align: center;
  font-size: 0.85rem;
  color: #6B7280;
  margin: 0;
}

.success-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
  max-width: 360px;
  font-family: 'Inter', system-ui, sans-serif;
}

.success-icon {
  width: 64px;
  height: 64px;
  background: #10B981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.75rem;
  font-weight: 700;
}

.success-panel h2 {
  font-size: 1.75rem;
  font-weight: 800;
  color: #111827;
  margin: 0;
}

.success-panel p {
  color: #6B7280;
  font-size: 0.9rem;
  margin: 0;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .auth-page {
    grid-template-columns: 1fr;
  }

  .auth-page__brand {
    display: none;
  }
}
</style>
