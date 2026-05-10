<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import Header from '../../components/header.vue'
import { albumsService } from '../../services/albums'
import { imagesService } from '../../services/images'

const route   = useRoute()
const album   = ref(null)
const images  = ref([])
const loading = ref(true)
const error   = ref('')

const gradients = [
  { from: '#667eea', to: '#764ba2' }, { from: '#f093fb', to: '#f5576c' },
  { from: '#4facfe', to: '#00f2fe' }, { from: '#43e97b', to: '#38f9d7' },
  { from: '#fa709a', to: '#fee140' }, { from: '#a18cd1', to: '#fbc2eb' },
  { from: '#fccb90', to: '#d57eeb' }, { from: '#0fd850', to: '#f9f047' },
  { from: '#30cfd0', to: '#330867' }, { from: '#a1c4fd', to: '#c2e9fb' },
  { from: '#fd7043', to: '#ff8a65' }, { from: '#26a0da', to: '#314755' },
]

const albumPalette = ['#3B82F6','#2563EB','#60A5FA','#BFDBFE']

function initials(name) {
  return (name ?? '?').split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
}

function formatDate(iso) {
  return iso ? new Date(iso).toLocaleDateString('es-EC', { day:'2-digit', month:'short', year:'numeric' }) : ''
}

onMounted(async () => {
  const id = route.params.id
  try {
    const [albumData, imgData] = await Promise.all([
      albumsService.getById(id),
      imagesService.getByAlbum(id),
    ])
    album.value  = albumData
    images.value = imgData
  } catch {
    error.value = 'No se pudo cargar el álbum.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="album-page">
    <Header />

    <div v-if="loading" class="loading-state">
      <div class="spinner-large"></div>
      <p>Cargando álbum...</p>
    </div>

    <div v-else-if="error || !album" class="not-found">
      <p class="nf-icon">📂</p>
      <h2>Álbum no encontrado</h2>
      <p>{{ error || 'Este álbum no existe o no está disponible públicamente.' }}</p>
      <RouterLink to="/galeria" class="back-btn">← Volver a la galería</RouterLink>
    </div>

    <template v-else>
      <section class="album-banner" :style="{ background: `linear-gradient(135deg, ${albumPalette[0]}, ${albumPalette[1]})` }">
        <div class="album-banner__inner">
          <RouterLink to="/galeria" class="back-link">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            Galería pública
          </RouterLink>

          <div class="album-banner__body">
            <div class="banner-cover">
              <div v-for="(c, i) in albumPalette" :key="i" class="banner-swatch" :style="{ background: c, opacity: 0.4 + i * 0.15 }"></div>
            </div>

            <div class="album-banner__text">
              <h1 class="album-title">{{ album.name }}</h1>
              <p class="album-desc">{{ album.description }}</p>
              <div class="album-meta">
                <div class="author-chip">
                  <div class="author-avatar">{{ initials(album.author_name) }}</div>
                  <span>{{ album.author_name ?? 'Usuario' }}</span>
                </div>
                <span class="meta-sep">·</span>
                <span>{{ images.length }} imágenes</span>
                <span class="meta-sep">·</span>
                <span>{{ formatDate(album.date_created) }}</span>
              </div>
            </div>
          </div>

          <div class="verify-badge">
            <span class="verify-dot"></span>
            Álbum verificado · LSB + MIME + EXIF
          </div>
        </div>
      </section>

      <section class="images-section">
        <div v-if="images.length === 0" class="empty-images">
          <p>Este álbum aún no tiene imágenes.</p>
        </div>
        <div v-else class="images-grid">
          <div v-for="(img, idx) in images" :key="img.image_id" class="image-card">
            <div class="image-thumb">
              <img
                :src="img.image_path"
                :alt="img.image_name"
                class="real-image"
                loading="lazy"
                :style="{ background: `linear-gradient(135deg, ${gradients[idx % gradients.length].from}, ${gradients[idx % gradients.length].to})` }"
              />
              <div class="image-overlay">
                <svg class="expand-icon" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round">
                  <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>
                </svg>
              </div>
            </div>
            <div class="image-footer">
              <span class="image-name">{{ img.image_name }}</span>
              <span class="verified-tag">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" width="10" height="10">
                  <path d="M20 6L9 17l-5-5"/>
                </svg>
                Verificado
              </span>
            </div>
          </div>
        </div>
      </section>

      <div class="security-banner">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="security-icon">
          <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
        </svg>
        <span>
          Cada imagen ha pasado <strong>análisis LSB</strong>, <strong>validación MIME real</strong>
          y <strong>eliminación de metadatos EXIF</strong> antes de publicarse en esta galería.
        </span>
      </div>

      <section class="visitor-cta">
        <div class="visitor-cta__inner">
          <h2 class="cta-title">¿Quieres subir tus propias fotos?</h2>
          <p class="cta-sub">Regístrate gratis, solicita un álbum y comparte imágenes con análisis de seguridad automático.</p>
          <div class="cta-actions">
            <RouterLink to="/register" class="cta-btn cta-btn--primary">Crear cuenta gratis →</RouterLink>
            <RouterLink to="/galeria" class="cta-btn cta-btn--ghost">Ver más álbumes</RouterLink>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.album-page {
  min-height: 100vh;
  background: #F9FAFB;
  font-family: 'Inter', system-ui, sans-serif;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 6rem 2rem;
  color: #9CA3AF;
  font-size: 0.9rem;
}

.spinner-large {
  width: 40px; height: 40px;
  border: 3px solid #E5E7EB;
  border-top-color: #2E75B6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.real-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.empty-images {
  text-align: center;
  padding: 3rem;
  color: #9CA3AF;
  font-size: 0.9rem;
}

.not-found {
  text-align: center;
  padding: 6rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.nf-icon { font-size: 3rem; margin: 0; }

.not-found h2 { font-size: 1.5rem; font-weight: 700; color: #111827; margin: 0; }
.not-found p { color: #6B7280; margin: 0; }

.back-btn {
  display: inline-block;
  margin-top: 0.5rem;
  background: #2E75B6;
  color: white;
  padding: 0.6rem 1.25rem;
  border-radius: 7px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.88rem;
}

.album-banner {
  padding: 2.5rem 2rem;
  color: white;
}

.album-banner__inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  font-size: 0.82rem;
  font-weight: 500;
  transition: color 0.15s;
}

.back-link svg { width: 14px; height: 14px; }
.back-link:hover { color: white; }

.album-banner__body {
  display: flex;
  align-items: center;
  gap: 1.75rem;
}

.banner-cover {
  display: grid;
  grid-template-columns: 1fr 1fr;
  width: 100px;
  height: 100px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 4px 16px rgba(0,0,0,0.25);
}

.banner-swatch { transition: transform 0.3s; }

.album-banner__text { flex: 1; }

.album-title {
  font-size: clamp(1.25rem, 3vw, 2rem);
  font-weight: 800;
  margin: 0 0 0.5rem;
  line-height: 1.2;
}

.album-desc {
  font-size: 0.875rem;
  opacity: 0.82;
  margin: 0 0 1rem;
  line-height: 1.6;
  max-width: 560px;
}

.album-meta {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.82rem;
  opacity: 0.8;
  flex-wrap: wrap;
}

.author-chip {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.author-avatar {
  width: 24px;
  height: 24px;
  background: rgba(255,255,255,0.25);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.6rem;
  font-weight: 700;
}

.meta-sep { opacity: 0.5; }

.verify-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.2);
  padding: 0.3rem 0.8rem;
  border-radius: 99px;
  font-size: 0.72rem;
  font-weight: 500;
  width: fit-content;
}

.verify-dot {
  width: 7px;
  height: 7px;
  background: #10B981;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.images-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 2rem;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.85rem;
}

.image-card {
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #E5E7EB;
  background: white;
}

.image-thumb {
  position: relative;
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  cursor: pointer;
}

.photo-icon {
  width: 36px;
  height: 36px;
  opacity: 0.5;
  pointer-events: none;
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.image-card:hover .image-overlay { opacity: 1; }

.expand-icon { width: 22px; height: 22px; }

.image-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0.65rem;
}

.image-name {
  font-size: 0.72rem;
  color: #6B7280;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 80px;
}

.verified-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.65rem;
  font-weight: 600;
  color: #10B981;
  background: #ECFDF5;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  flex-shrink: 0;
}

.security-banner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.65rem;
  background: #EFF6FF;
  border-top: 1px solid #BFDBFE;
  border-bottom: 1px solid #BFDBFE;
  padding: 0.85rem 2rem;
  font-size: 0.8rem;
  color: #1E4D7B;
  text-align: center;
}

.security-icon { width: 18px; height: 18px; color: #2E75B6; flex-shrink: 0; }

.visitor-cta {
  background: #1E4D7B;
  padding: 4rem 2rem;
  text-align: center;
}

.visitor-cta__inner {
  max-width: 520px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.85rem;
}

.cta-title {
  font-size: clamp(1.3rem, 3vw, 1.85rem);
  font-weight: 800;
  color: white;
  margin: 0;
}

.cta-sub {
  font-size: 0.88rem;
  color: rgba(255,255,255,0.72);
  margin: 0;
  line-height: 1.6;
}

.cta-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.cta-btn {
  display: inline-block;
  padding: 0.7rem 1.4rem;
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.88rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.cta-btn--primary { background: #2E75B6; color: white; }
.cta-btn--primary:hover { background: #1a5c96; transform: translateY(-1px); }
.cta-btn--ghost { background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.85); border: 1px solid rgba(255,255,255,0.2); }
.cta-btn--ghost:hover { background: rgba(255,255,255,0.18); }

@media (max-width: 900px) {
  .images-grid { grid-template-columns: repeat(3, 1fr); }
  .album-banner__body { flex-direction: column; align-items: flex-start; }
  .banner-cover { width: 80px; height: 80px; }
}

@media (max-width: 600px) {
  .images-grid { grid-template-columns: repeat(2, 1fr); }
  .album-banner { padding: 1.75rem 1.25rem; }
  .images-section { padding: 1.5rem 1rem; }
}
</style>
