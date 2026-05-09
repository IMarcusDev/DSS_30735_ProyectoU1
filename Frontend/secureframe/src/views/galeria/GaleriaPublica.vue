<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import Header from '../../components/header.vue'

const searchQuery = ref('')

const publicAlbums = [
  {
    id: 'ALB-002',
    title: 'Arquitectura Histórica Quito',
    description: 'Registro fotográfico del centro histórico de la ciudad de Quito, Ecuador.',
    imageCount: 8,
    authorInitials: 'ME',
    authorName: 'Marcos Escobar',
    date: '03/05/2026',
    isNew: false,
    palette: ['#3B82F6', '#2563EB', '#60A5FA', '#BFDBFE'],
  },
  {
    id: 'ALB-005',
    title: 'Naturaleza en Cotacachi',
    description: 'Fotografías de la naturaleza del volcán Cotacachi y sus alrededores.',
    imageCount: 12,
    authorInitials: 'AV',
    authorName: 'Ana Vázquez',
    date: '05/05/2026',
    isNew: true,
    palette: ['#10B981', '#059669', '#34D399', '#A7F3D0'],
  },
  {
    id: 'ALB-006',
    title: 'Ciudad de Guayaquil',
    description: 'Vistas urbanas del puerto principal de Ecuador al atardecer y al amanecer.',
    imageCount: 15,
    authorInitials: 'CR',
    authorName: 'Carlos Reyes',
    date: '06/05/2026',
    isNew: true,
    palette: ['#F59E0B', '#D97706', '#FCD34D', '#FEF3C7'],
  },
  {
    id: 'ALB-007',
    title: 'Mercado Artesanal Otavalo',
    description: 'Colores, texturas y cultura del mercado indígena más grande de Sudamérica.',
    imageCount: 10,
    authorInitials: 'LP',
    authorName: 'Lucía Paz',
    date: '07/05/2026',
    isNew: false,
    palette: ['#8B5CF6', '#7C3AED', '#C4B5FD', '#EDE9FE'],
  },
  {
    id: 'ALB-008',
    title: 'Paisajes de los Andes',
    description: 'La majestuosidad de la cordillera andina ecuatoriana captada en distintas épocas.',
    imageCount: 20,
    authorInitials: 'JM',
    authorName: 'Jorge Morales',
    date: '08/05/2026',
    isNew: true,
    palette: ['#EF4444', '#DC2626', '#FCA5A5', '#FEE2E2'],
  },
  {
    id: 'ALB-009',
    title: 'ESPE Campus Universitario',
    description: 'La vida universitaria y la infraestructura del campus de la ESPE.',
    imageCount: 6,
    authorInitials: 'ME',
    authorName: 'Marcos Escobar',
    date: '01/05/2026',
    isNew: false,
    palette: ['#0EA5E9', '#0284C7', '#38BDF8', '#BAE6FD'],
  },
]

const filteredAlbums = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return publicAlbums
  return publicAlbums.filter(a =>
    a.title.toLowerCase().includes(q) ||
    a.description.toLowerCase().includes(q) ||
    a.authorName.toLowerCase().includes(q)
  )
})

const totalImages = publicAlbums.reduce((sum, a) => sum + a.imageCount, 0)
</script>

<template>
  <div class="gallery-page">
    <Header />

    <section class="gallery-hero">
      <div class="gallery-hero__inner">
        <span class="hero-tag">GALERÍA PÚBLICA · ACCESO LIBRE</span>
        <h1 class="hero-heading">Explora imágenes verificadas</h1>
        <p class="hero-sub">
          Todas las fotos han pasado análisis de esteganografía LSB, validación MIME real
          y eliminación de metadatos EXIF antes de publicarse.
        </p>

        <div class="search-bar">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
            <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            class="search-input"
            placeholder="Buscar álbumes, autores..."
          />
        </div>

        <div class="security-badge">
          <span class="security-badge__dot"></span>
          Imágenes verificadas · LSB + MIME + EXIF
        </div>
      </div>
    </section>

    <div class="gallery-stats">
      <span><strong>{{ publicAlbums.length }}</strong> álbumes públicos</span>
      <span class="stats-sep">·</span>
      <span><strong>{{ totalImages }}</strong> imágenes verificadas</span>
      <span class="stats-sep">·</span>
      <span>Actualizado hoy</span>
    </div>

    <section class="albums-section">
      <div v-if="filteredAlbums.length > 0" class="albums-grid">
        <RouterLink
          v-for="album in filteredAlbums"
          :key="album.id"
          :to="`/galeria/${album.id}`"
          class="album-card"
        >
          <div class="album-cover">
            <div v-for="(color, i) in album.palette" :key="i" class="cover-swatch" :style="{ background: color }"></div>
            <span v-if="album.isNew" class="new-badge">Nuevo</span>
          </div>

          <div class="album-info">
            <div class="album-info__top">
              <h3 class="album-title">{{ album.title }}</h3>
              <p class="album-desc">{{ album.description }}</p>
            </div>
            <div class="album-meta">
              <div class="author-chip">
                <div class="author-avatar">{{ album.authorInitials }}</div>
                <span class="author-name">{{ album.authorName }}</span>
              </div>
              <span class="image-count">{{ album.imageCount }} fotos</span>
            </div>
          </div>
        </RouterLink>
      </div>

      <div v-else class="empty-state">
        <p class="empty-icon">🔍</p>
        <p class="empty-title">No se encontraron álbumes</p>
        <p class="empty-sub">Intenta con otro término de búsqueda</p>
        <button class="empty-reset" @click="searchQuery = ''">Limpiar búsqueda</button>
      </div>
    </section>

    <section class="visitor-cta">
      <div class="visitor-cta__inner">
        <h2 class="cta-title">¿Quieres compartir tus imágenes?</h2>
        <p class="cta-sub">Crea tu cuenta gratuita, solicita un álbum y sube fotos con análisis de seguridad automático.</p>
        <div class="cta-actions">
          <RouterLink to="/register" class="cta-btn cta-btn--primary">Crear cuenta gratis →</RouterLink>
          <RouterLink to="/login" class="cta-btn cta-btn--ghost">Ya tengo cuenta</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.gallery-page {
  min-height: 100vh;
  background: #F9FAFB;
  font-family: 'Inter', system-ui, sans-serif;
}

.gallery-hero {
  background: linear-gradient(160deg, #1E4D7B 0%, #2E75B6 100%);
  padding: 3.5rem 2rem 4rem;
  text-align: center;
  color: white;
}

.gallery-hero__inner {
  max-width: 680px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.hero-tag {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.7;
}

.hero-heading {
  font-size: clamp(1.75rem, 4vw, 2.75rem);
  font-weight: 800;
  margin: 0;
  line-height: 1.15;
}

.hero-sub {
  font-size: 0.9rem;
  opacity: 0.8;
  line-height: 1.65;
  margin: 0;
  max-width: 520px;
}

.search-bar {
  position: relative;
  width: 100%;
  max-width: 480px;
  margin-top: 0.5rem;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #9CA3AF;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.8rem 1rem 0.8rem 2.85rem;
  border: none;
  border-radius: 10px;
  font-family: inherit;
  font-size: 0.9rem;
  color: #111827;
  background: white;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  outline: none;
  box-sizing: border-box;
  transition: box-shadow 0.15s;
}

.search-input:focus { box-shadow: 0 4px 24px rgba(0,0,0,0.25); }

.security-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.2);
  padding: 0.35rem 0.85rem;
  border-radius: 99px;
  font-size: 0.72rem;
  font-weight: 500;
  opacity: 0.9;
}

.security-badge__dot {
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

.gallery-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.9rem 2rem;
  background: white;
  border-bottom: 1px solid #E5E7EB;
  font-size: 0.82rem;
  color: #6B7280;
}

.gallery-stats strong { color: #111827; }
.stats-sep { color: #D1D5DB; }

.albums-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2.5rem 2rem;
}

.albums-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}

.album-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
}

.album-card:hover {
  box-shadow: 0 8px 30px rgba(46,117,182,0.15);
  transform: translateY(-2px);
  border-color: #93C5FD;
}

.album-cover {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 90px 90px;
  height: 180px;
  overflow: hidden;
}

.cover-swatch { transition: transform 0.3s ease; }
.album-card:hover .cover-swatch { transform: scale(1.04); }

.new-badge {
  position: absolute;
  top: 0.6rem;
  right: 0.6rem;
  background: #2E75B6;
  color: white;
  font-size: 0.65rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: 99px;
  letter-spacing: 0.04em;
  z-index: 1;
}

.album-info {
  padding: 1rem 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
}

.album-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
  line-height: 1.3;
}

.album-desc {
  font-size: 0.78rem;
  color: #6B7280;
  margin: 0.3rem 0 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.album-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.65rem;
  border-top: 1px solid #F3F4F6;
}

.author-chip {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.author-avatar {
  width: 26px;
  height: 26px;
  background: linear-gradient(135deg, #2E75B6, #1E4D7B);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.62rem;
  font-weight: 700;
  flex-shrink: 0;
}

.author-name {
  font-size: 0.75rem;
  color: #374151;
  font-weight: 500;
}

.image-count {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon { font-size: 2.5rem; margin: 0 0 0.75rem; }
.empty-title { font-size: 1rem; font-weight: 600; color: #374151; margin: 0 0 0.3rem; }
.empty-sub { font-size: 0.82rem; color: #9CA3AF; margin: 0 0 1.25rem; }

.empty-reset {
  background: none;
  border: 1.5px solid #D1D5DB;
  border-radius: 7px;
  padding: 0.5rem 1.25rem;
  font-family: inherit;
  font-size: 0.85rem;
  color: #374151;
  cursor: pointer;
  transition: all 0.15s;
}
.empty-reset:hover { border-color: #2E75B6; color: #2E75B6; }

.visitor-cta {
  background: #1E4D7B;
  padding: 4rem 2rem;
  text-align: center;
}

.visitor-cta__inner {
  max-width: 560px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.85rem;
}

.cta-title {
  font-size: clamp(1.4rem, 3vw, 2rem);
  font-weight: 800;
  color: white;
  margin: 0;
}

.cta-sub {
  font-size: 0.9rem;
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
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.cta-btn--primary {
  background: #2E75B6;
  color: white;
  box-shadow: 0 4px 14px rgba(46,117,182,0.4);
}

.cta-btn--primary:hover {
  background: #1a5c96;
  transform: translateY(-1px);
}

.cta-btn--ghost {
  background: rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.85);
  border: 1px solid rgba(255,255,255,0.2);
}

.cta-btn--ghost:hover {
  background: rgba(255,255,255,0.18);
}

@media (max-width: 900px) {
  .albums-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 600px) {
  .albums-grid { grid-template-columns: 1fr; }
  .gallery-hero { padding: 2.5rem 1.25rem 3rem; }
  .albums-section { padding: 1.5rem 1rem; }
}
</style>
