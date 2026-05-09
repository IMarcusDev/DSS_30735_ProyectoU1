<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const title       = ref('')
const description = ref('')
const privacy     = ref('publico')
const loading     = ref(false)
const errors      = ref({ title: '', description: '' })

const titleLen = computed(() => title.value.length)
const descLen  = computed(() => description.value.length)

const titleProgress = computed(() => Math.min((titleLen.value / 100) * 100, 100))
const descProgress  = computed(() => Math.min((descLen.value / 500) * 100, 100))

function validate() {
  errors.value = { title: '', description: '' }
  let valid = true
  if (!title.value.trim()) {
    errors.value.title = 'El título es requerido'
    valid = false
  } else if (titleLen.value > 100) {
    errors.value.title = 'Máximo 100 caracteres'
    valid = false
  }
  if (!description.value.trim()) {
    errors.value.description = 'La descripción es requerida'
    valid = false
  } else if (descLen.value > 500) {
    errors.value.description = 'Máximo 500 caracteres'
    valid = false
  }
  return valid
}

async function handleSubmit() {
  if (!validate()) return
  loading.value = true
  // TODO: conectar al backend (POST /albums/request)
  await new Promise(r => setTimeout(r, 900))
  loading.value = false
  router.push({ path: '/user/albums', query: { toast: 'created' } })
}
</script>

<template>
  <div class="page">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <RouterLink to="/user/albums" class="bc-link">Mis Álbumes</RouterLink>
      <span class="bc-sep">/</span>
      <span class="bc-current">Solicitar álbum</span>
    </nav>

    <div class="form-layout">
      <div class="form-card">
        <div class="form-card-header">
          <h2 class="form-title">Solicitar nuevo álbum</h2>
          <p class="form-sub">
            Tu solicitud será revisada por un Supervisor antes de activarse.
          </p>
        </div>

        <form class="form-body" @submit.prevent="handleSubmit" novalidate>

          <div class="field" :class="{ 'field--error': errors.title }">
            <div class="field-label-row">
              <label class="field__label" for="album-title">
                Título <span class="required">*</span>
              </label>
              <span class="char-count" :class="{ 'char-count--warn': titleLen > 80 }">
                {{ titleLen }}/100
              </span>
            </div>
            <input
              id="album-title"
              v-model="title"
              type="text"
              placeholder="Ej. Viaje a Galápagos 2026"
              maxlength="100"
              class="field__input"
            />
            <div class="progress-bar">
              <div class="progress-bar__fill" :style="{ width: titleProgress + '%', background: titleLen > 80 ? '#F59E0B' : '#2E75B6' }"></div>
            </div>
            <p v-if="errors.title" class="field__error">⚠ {{ errors.title }}</p>
          </div>

          <div class="field" :class="{ 'field--error': errors.description }">
            <div class="field-label-row">
              <label class="field__label" for="album-desc">
                Descripción <span class="required">*</span>
              </label>
              <span class="char-count" :class="{ 'char-count--warn': descLen > 400 }">
                {{ descLen }}/500
              </span>
            </div>
            <textarea
              id="album-desc"
              v-model="description"
              placeholder="Describe el contenido del álbum..."
              maxlength="500"
              rows="4"
              class="field__input field__textarea"
            ></textarea>
            <div class="progress-bar">
              <div class="progress-bar__fill" :style="{ width: descProgress + '%', background: descLen > 400 ? '#F59E0B' : '#2E75B6' }"></div>
            </div>
            <p v-if="errors.description" class="field__error"> {{ errors.description }}</p>
          </div>

          <div class="field">
            <label class="field__label" for="album-privacy">Privacidad</label>
            <div class="privacy-options">
              <label class="privacy-option" :class="{ 'privacy-option--active': privacy === 'publico' }">
                <input v-model="privacy" type="radio" value="publico" class="sr-only" />
                <div class="privacy-option__icon">🌐</div>
                <div>
                  <p class="privacy-option__title">Público</p>
                  <p class="privacy-option__sub">Visible para todos los visitantes</p>
                </div>
              </label>
              <label class="privacy-option" :class="{ 'privacy-option--active': privacy === 'privado' }">
                <input v-model="privacy" type="radio" value="privado" class="sr-only" />
                <div class="privacy-option__icon">🔒</div>
                <div>
                  <p class="privacy-option__title">Privado</p>
                  <p class="privacy-option__sub">Solo visible para ti y supervisores</p>
                </div>
              </label>
            </div>
          </div>

          <div class="submit-row">
            <RouterLink to="/user/albums" class="btn-cancel">Cancelar</RouterLink>
            <button type="submit" class="btn-submit" :disabled="loading">
              <span v-if="loading" class="spinner"></span>
              <span v-else>Enviar solicitud →</span>
            </button>
          </div>

        </form>
      </div>

      <aside class="info-panel">
        <div class="info-card">
          <h4 class="info-title">¿Cómo funciona?</h4>
          <ol class="info-steps">
            <li>
              <span class="info-step-num">1</span>
              <div>
                <p class="info-step-title">Envías la solicitud</p>
                <p class="info-step-sub">Con título, descripción y privacidad.</p>
              </div>
            </li>
            <li>
              <span class="info-step-num">2</span>
              <div>
                <p class="info-step-title">Revisión del Supervisor</p>
                <p class="info-step-sub">Puede tardar hasta 24h hábiles.</p>
              </div>
            </li>
            <li>
              <span class="info-step-num">3</span>
              <div>
                <p class="info-step-title">Álbum activado</p>
                <p class="info-step-sub">Ya puedes subir imágenes para análisis.</p>
              </div>
            </li>
          </ol>
        </div>

        <div class="security-note">
          <p class="security-note__title">🛡 Nota de seguridad</p>
          <p class="security-note__body">
            Las descripciones son sanitizadas automáticamente para prevenir
            ataques <strong>Stored XSS</strong> antes de almacenarse.
          </p>
        </div>
      </aside>

    </div>
  </div>
</template>

<style scoped>
.page { display: flex; flex-direction: column; gap: 1.25rem; }

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
}

.bc-link { color: #2E75B6; text-decoration: none; font-weight: 500; }
.bc-link:hover { text-decoration: underline; }
.bc-sep { color: #D1D5DB; }
.bc-current { color: #6B7280; }

.form-layout {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 1.25rem;
  align-items: start;
}

.form-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  overflow: hidden;
}

.form-card-header {
  padding: 1.5rem 1.75rem 1.25rem;
  border-bottom: 1px solid #F3F4F6;
}

.form-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: #111827;
  margin: 0;
}

.form-sub {
  font-size: 0.82rem;
  color: #6B7280;
  margin: 0.3rem 0 0;
}

.form-body {
  padding: 1.5rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.field { display: flex; flex-direction: column; gap: 0.4rem; }

.field-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.field__label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #374151;
}

.required { color: #EF4444; }

.char-count {
  font-size: 0.72rem;
  color: #9CA3AF;
  font-weight: 500;
}

.char-count--warn { color: #F59E0B; }

.field__input {
  padding: 0.65rem 0.85rem;
  border: 1.5px solid #E5E7EB;
  border-radius: 7px;
  font-family: inherit;
  font-size: 0.88rem;
  color: #111827;
  background: white;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
  box-sizing: border-box;
}

.field__input:focus {
  border-color: #2E75B6;
  box-shadow: 0 0 0 3px rgba(46,117,182,0.12);
}

.field--error .field__input { border-color: #EF4444; }
.field--error .field__input:focus { box-shadow: 0 0 0 3px rgba(239,68,68,0.12); }

.field__textarea {
  resize: vertical;
  min-height: 100px;
  line-height: 1.55;
}

.field__error {
  font-size: 0.78rem;
  color: #EF4444;
  margin: 0;
}

.progress-bar {
  height: 3px;
  background: #F3F4F6;
  border-radius: 99px;
  overflow: hidden;
}

.progress-bar__fill {
  height: 100%;
  border-radius: 99px;
  transition: width 0.2s ease, background 0.2s ease;
}

.privacy-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.privacy-option {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.85rem 1rem;
  border: 1.5px solid #E5E7EB;
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}

.privacy-option:hover { border-color: #2E75B6; background: #F0F7FF; }

.privacy-option--active {
  border-color: #2E75B6;
  background: #EFF6FF;
}

.privacy-option__icon { font-size: 1.3rem; }

.privacy-option__title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.privacy-option__sub {
  font-size: 0.72rem;
  color: #6B7280;
  margin: 0.15rem 0 0;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0,0,0,0);
  white-space: nowrap;
  border: 0;
}

.submit-row {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 0.5rem;
  border-top: 1px solid #F3F4F6;
}

.btn-cancel {
  font-size: 0.88rem;
  color: #6B7280;
  text-decoration: none;
  font-weight: 500;
  padding: 0.6rem 1rem;
  border-radius: 7px;
  transition: background 0.15s;
}

.btn-cancel:hover { background: #F3F4F6; color: #374151; }

.btn-submit {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: #2E75B6;
  color: white;
  border: none;
  font-family: inherit;
  font-size: 0.9rem;
  font-weight: 600;
  padding: 0.65rem 1.5rem;
  border-radius: 7px;
  cursor: pointer;
  transition: background 0.15s;
  min-width: 160px;
}

.btn-submit:hover:not(:disabled) { background: #1E4D7B; }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.35);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.info-panel { display: flex; flex-direction: column; gap: 0.75rem; }

.info-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  padding: 1.25rem;
}

.info-title {
  font-size: 0.88rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 1rem;
}

.info-steps {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.info-steps li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.info-step-num {
  width: 22px;
  height: 22px;
  background: #2E75B6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  flex-shrink: 0;
  margin-top: 1px;
}

.info-step-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.info-step-sub {
  font-size: 0.75rem;
  color: #9CA3AF;
  margin: 0.15rem 0 0;
}

.security-note {
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  border-radius: 8px;
  padding: 1rem;
}

.security-note__title {
  font-size: 0.8rem;
  font-weight: 700;
  color: #1E4D7B;
  margin: 0 0 0.4rem;
}

.security-note__body {
  font-size: 0.75rem;
  color: #374151;
  margin: 0;
  line-height: 1.55;
}

@media (max-width: 900px) {
  .form-layout { grid-template-columns: 1fr; }
  .info-panel { display: none; }
}

@media (max-width: 600px) {
  .privacy-options { grid-template-columns: 1fr; }
}
</style>
