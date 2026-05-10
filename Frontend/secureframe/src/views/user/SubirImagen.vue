<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { albumsService, type Album } from '../../services/albums'
import { imagesService, type GalleryImage } from '../../services/images'
import { ApiError } from '../../services/api'

const approvedAlbums = ref<Album[]>([])
const selectedAlbum  = ref('')
const file           = ref<File | null>(null)
const preview        = ref<string | null>(null)
const loading        = ref(false)
const loadingAlbums  = ref(true)
const error          = ref('')
const uploadResult   = ref<GalleryImage | null>(null)

const stateMap = {
  Limpio:     { label: 'Limpio — imagen aprobada',        color: '#10B981', bg: '#ECFDF5' },
  Sospechoso: { label: 'Sospechoso — en cuarentena',      color: '#F59E0B', bg: '#FFFBEB' },
  Positivo:   { label: 'Positivo — pendiente eliminación',color: '#EF4444', bg: '#FEF2F2' },
} as const

onMounted(async () => {
  try {
    const all = await albumsService.getMine()
    approvedAlbums.value = all.filter(a => a.state === 'Aprobado')
  } catch {
    error.value = 'No se pudieron cargar tus álbumes.'
  } finally {
    loadingAlbums.value = false
  }
})

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  const f = input.files?.[0] ?? null
  file.value = f
  preview.value = f ? URL.createObjectURL(f) : null
  uploadResult.value = null
  error.value = ''
}

function onDrop(e: DragEvent) {
  e.preventDefault()
  const f = e.dataTransfer?.files[0] ?? null
  if (f) {
    file.value = f
    preview.value = URL.createObjectURL(f)
    uploadResult.value = null
    error.value = ''
  }
}

async function handleUpload() {
  if (!file.value || !selectedAlbum.value) return
  loading.value = true
  error.value = ''
  uploadResult.value = null
  try {
    const result = await imagesService.upload(selectedAlbum.value, file.value)
    uploadResult.value = result
    file.value = null
    preview.value = null
  } catch (err) {
    if (err instanceof ApiError) {
      error.value = err.message
    } else {
      error.value = 'Error al subir la imagen.'
    }
  } finally {
    loading.value = false
  }
}

function formatSize(bytes: number): string {
  return bytes > 1_048_576
    ? `${(bytes / 1_048_576).toFixed(1)} MB`
    : `${(bytes / 1024).toFixed(0)} KB`
}
</script>

<template>
  <div class="page">
    <nav class="breadcrumb">
      <RouterLink to="/user/albums" class="bc-link">Mis Álbumes</RouterLink>
      <span class="bc-sep">/</span>
      <span class="bc-current">Subir imagen</span>
    </nav>

    <div class="layout">
      <div class="upload-card">
        <div class="card-header">
          <h2 class="card-title">Subir imagen</h2>
          <p class="card-sub">La imagen pasará análisis automático antes de publicarse</p>
        </div>

        <div class="card-body">
          <div class="field">
            <label class="field-label" for="album-select">
              Álbum destino <span class="required">*</span>
            </label>
            <div v-if="loadingAlbums" class="loading-inline">Cargando álbumes...</div>
            <select
              v-else
              id="album-select"
              v-model="selectedAlbum"
              class="field-select"
              :disabled="approvedAlbums.length === 0"
            >
              <option value="" disabled>Selecciona un álbum aprobado</option>
              <option v-for="a in approvedAlbums" :key="a.id" :value="a.id">
                {{ a.name }}
              </option>
            </select>
            <p v-if="approvedAlbums.length === 0 && !loadingAlbums" class="field-hint">
              No tienes álbumes aprobados.
              <RouterLink to="/user/albums/new" class="link">Solicita uno →</RouterLink>
            </p>
          </div>

          <div class="field">
            <label class="field-label">Archivo <span class="required">*</span></label>
            <div
              class="drop-zone"
              :class="{ 'drop-zone--has-file': !!file }"
              @dragover.prevent
              @drop="onDrop"
              @click="($refs.fileInput as HTMLInputElement).click()"
            >
              <input
                ref="fileInput"
                type="file"
                accept="image/jpeg,image/png,image/gif,image/webp,image/bmp"
                class="sr-only"
                @change="onFileChange"
              />
              <div v-if="!file" class="drop-placeholder">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" class="drop-icon">
                  <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
                </svg>
                <p class="drop-title">Arrastra tu imagen aquí</p>
                <p class="drop-sub">o haz clic para seleccionar · JPEG, PNG, GIF, WebP, BMP · máx. 10 MB</p>
              </div>
              <div v-else class="drop-selected">
                <img v-if="preview" :src="preview" class="preview-thumb" alt="Vista previa" />
                <div class="file-info">
                  <p class="file-name">{{ file.name }}</p>
                  <p class="file-size">{{ formatSize(file.size) }}</p>
                </div>
                <button type="button" class="file-remove" @click.stop="file = null; preview = null">✕</button>
              </div>
            </div>
          </div>

          <div v-if="error" class="alert alert--error">⚠ {{ error }}</div>

          <button
            type="button"
            class="btn-submit"
            :disabled="!file || !selectedAlbum || loading"
            @click="handleUpload"
          >
            <span v-if="loading" class="spinner"></span>
            <span v-else>Subir y analizar →</span>
          </button>
        </div>
      </div>

      <aside class="side-panel">
        <div v-if="uploadResult" class="result-card">
          <p class="result-tag">RESULTADO DEL ANÁLISIS</p>
          <div
            class="result-state"
            :style="{ color: stateMap[uploadResult.image_state].color, background: stateMap[uploadResult.image_state].bg }"
          >
            <span class="result-dot" :style="{ background: stateMap[uploadResult.image_state].color }"></span>
            {{ stateMap[uploadResult.image_state].label }}
          </div>
          <img :src="uploadResult.image_path" :alt="uploadResult.image_name" class="result-img" />
          <div class="result-meta">
            <div class="meta-row">
              <span>Nombre</span>
              <span>{{ uploadResult.image_name }}</span>
            </div>
            <div class="meta-row">
              <span>Tamaño</span>
              <span>{{ formatSize(uploadResult.image_size) }}</span>
            </div>
            <div class="meta-row">
              <span>MIME</span>
              <span>{{ uploadResult.image_mimetype }}</span>
            </div>
          </div>
          <p v-if="uploadResult.image_state !== 'Limpio'" class="quarantine-note">
            Esta imagen fue enviada a cuarentena para revisión del supervisor.
          </p>
        </div>

        <!-- Info card -->
        <div v-else class="info-card">
          <h4 class="info-title">¿Qué ocurre al subir?</h4>
          <ol class="info-steps">
            <li>
              <span class="step-num">1</span>
              <div>
                <p class="step-title">Validación MIME real</p>
                <p class="step-sub">Se verifica el tipo mediante file magic numbers.</p>
              </div>
            </li>
            <li>
              <span class="step-num">2</span>
              <div>
                <p class="step-title">Limpieza EXIF</p>
                <p class="step-sub">Se eliminan metadatos de geolocalización y otros.</p>
              </div>
            </li>
            <li>
              <span class="step-num">3</span>
              <div>
                <p class="step-title">Análisis LSB + EOF</p>
                <p class="step-sub">Detección de datos ocultos en píxeles y marcadores.</p>
              </div>
            </li>
            <li>
              <span class="step-num">4</span>
              <div>
                <p class="step-title">Publicación o cuarentena</p>
                <p class="step-sub">Limpio → galería. Sospechoso → revisión del supervisor.</p>
              </div>
            </li>
          </ol>
        </div>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.page { display: flex; flex-direction: column; gap: 1.25rem; }

.breadcrumb { display: flex; align-items: center; gap: 0.5rem; font-size: 0.82rem; }
.bc-link { color: #2E75B6; text-decoration: none; font-weight: 500; }
.bc-link:hover { text-decoration: underline; }
.bc-sep { color: #D1D5DB; }
.bc-current { color: #6B7280; }

.layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 1.25rem;
  align-items: start;
}

.upload-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  overflow: hidden;
  font-family: 'Inter', system-ui, sans-serif;
}

.card-header {
  padding: 1.5rem 1.75rem 1.25rem;
  border-bottom: 1px solid #F3F4F6;
}

.card-title { font-size: 1.1rem; font-weight: 800; color: #111827; margin: 0; }
.card-sub { font-size: 0.8rem; color: #6B7280; margin: 0.25rem 0 0; }

.card-body {
  padding: 1.5rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.field { display: flex; flex-direction: column; gap: 0.4rem; }
.field-label { font-size: 0.85rem; font-weight: 600; color: #374151; }
.required { color: #EF4444; }

.field-select {
  padding: 0.65rem 0.85rem;
  border: 1.5px solid #E5E7EB;
  border-radius: 7px;
  font-family: inherit;
  font-size: 0.88rem;
  color: #111827;
  background: white;
  outline: none;
  cursor: pointer;
  transition: border-color 0.15s;
}

.field-select:focus { border-color: #2E75B6; }
.field-select:disabled { opacity: 0.6; cursor: not-allowed; }

.field-hint { font-size: 0.78rem; color: #6B7280; margin: 0; }
.link { color: #2E75B6; text-decoration: none; font-weight: 600; }
.link:hover { text-decoration: underline; }

.loading-inline { font-size: 0.82rem; color: #9CA3AF; }

.drop-zone {
  border: 2px dashed #D1D5DB;
  border-radius: 10px;
  min-height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s;
  background: #FAFAFA;
}

.drop-zone:hover, .drop-zone--has-file { border-color: #2E75B6; background: #F0F7FF; }

.drop-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 2rem;
  text-align: center;
}

.drop-icon { width: 32px; height: 32px; color: #9CA3AF; }
.drop-title { font-size: 0.9rem; font-weight: 600; color: #374151; margin: 0; }
.drop-sub { font-size: 0.75rem; color: #9CA3AF; margin: 0; }

.drop-selected {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  width: 100%;
}

.preview-thumb {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 7px;
  flex-shrink: 0;
}

.file-info { flex: 1; }
.file-name { font-size: 0.85rem; font-weight: 600; color: #111827; margin: 0; word-break: break-all; }
.file-size { font-size: 0.75rem; color: #6B7280; margin: 0.2rem 0 0; }

.file-remove {
  background: none;
  border: 1.5px solid #E5E7EB;
  border-radius: 6px;
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
  color: #6B7280;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.15s;
}

.file-remove:hover { border-color: #EF4444; color: #EF4444; }

.alert { padding: 0.7rem 1rem; border-radius: 6px; font-size: 0.85rem; }
.alert--error { background: #FEF2F2; border: 1px solid #FECACA; color: #B91C1C; }

.btn-submit {
  width: 100%;
  padding: 0.8rem 1rem;
  border-radius: 7px;
  font-family: inherit;
  font-size: 0.95rem;
  font-weight: 600;
  background: #2E75B6;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: background 0.15s;
}

.btn-submit:hover:not(:disabled) { background: #1E4D7B; }
.btn-submit:disabled { opacity: 0.5; cursor: not-allowed; }

.spinner {
  width: 18px; height: 18px;
  border: 2.5px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.sr-only {
  position: absolute; width: 1px; height: 1px;
  padding: 0; overflow: hidden; clip: rect(0,0,0,0);
  white-space: nowrap; border: 0;
}

.side-panel { display: flex; flex-direction: column; gap: 0; }

.result-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  font-family: 'Inter', system-ui, sans-serif;
}

.result-tag { font-size: 0.62rem; font-weight: 700; letter-spacing: 0.1em; color: #9CA3AF; text-transform: uppercase; margin: 0; }

.result-state {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.75rem;
  border-radius: 99px;
  font-size: 0.78rem;
  font-weight: 600;
  width: fit-content;
}

.result-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }

.result-img {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-radius: 7px;
  border: 1px solid #E5E7EB;
}

.result-meta { display: flex; flex-direction: column; gap: 0.5rem; }

.meta-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: #374151;
}

.meta-row span:first-child { color: #9CA3AF; }
.meta-row span:last-child { font-weight: 600; word-break: break-all; text-align: right; max-width: 60%; }

.quarantine-note {
  font-size: 0.75rem;
  color: #B45309;
  background: #FFFBEB;
  border: 1px solid #FDE68A;
  padding: 0.55rem 0.7rem;
  border-radius: 6px;
  margin: 0;
}

.info-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  padding: 1.25rem;
  font-family: 'Inter', system-ui, sans-serif;
}

.info-title { font-size: 0.9rem; font-weight: 700; color: #111827; margin: 0 0 1rem; }

.info-steps { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.85rem; }

.info-steps li { display: flex; gap: 0.75rem; align-items: flex-start; }

.step-num {
  width: 22px; height: 22px;
  background: #2E75B6; color: white;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.7rem; font-weight: 700;
  flex-shrink: 0; margin-top: 1px;
}

.step-title { font-size: 0.82rem; font-weight: 600; color: #374151; margin: 0; }
.step-sub { font-size: 0.75rem; color: #9CA3AF; margin: 0.15rem 0 0; }

@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; }
  .side-panel { order: -1; }
}
</style>
