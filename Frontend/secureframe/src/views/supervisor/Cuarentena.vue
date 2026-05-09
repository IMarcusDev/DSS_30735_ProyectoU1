<script setup lang="ts">
import { ref, computed } from 'vue'

type RiskLevel = 'high' | 'medium'

interface Gradient { from: string; to: string }

const gradients: Gradient[] = [
  { from: '#667eea', to: '#764ba2' }, { from: '#4facfe', to: '#00f2fe' },
  { from: '#fa709a', to: '#fee140' }, { from: '#43e97b', to: '#38f9d7' },
  { from: '#30cfd0', to: '#330867' },
]

interface QuarantineImage {
  id: string; filename: string; album: string
  uploader: string; uploaderI: string; date: string
  risk: RiskLevel; reasons: string[]; gradient: Gradient
}

const images = ref<QuarantineImage[]>([
  { id: 'QRT-001', filename: 'foto_012.jpg',        album: 'Proyecto ESPE 2025',           uploader: 'Marcos Escobar',  uploaderI: 'ME', date: '07/05 14:23', risk: 'high',   reasons: ['Anomalía LSB detectada', 'Marcador EOF sospechoso'], gradient: gradients[0]! },
  { id: 'QRT-002', filename: 'arquitectura_05.jpg', album: 'Arquitectura Histórica Quito', uploader: 'Marcos Escobar',  uploaderI: 'ME', date: '08/05 09:11', risk: 'medium', reasons: ['Histograma de color anómalo'],                         gradient: gradients[1]! },
  { id: 'QRT-003', filename: 'paisaje_001.jpg',     album: 'Paisajes de los Andes',        uploader: 'Jorge Morales',   uploaderI: 'JM', date: '08/05 10:44', risk: 'high',   reasons: ['Anomalía LSB detectada', 'Ruido estadístico alto'],  gradient: gradients[2]! },
  { id: 'QRT-004', filename: 'mercado_07.jpg',      album: 'Mercado Artesanal Otavalo',    uploader: 'Lucía Paz',       uploaderI: 'LP', date: '08/05 11:02', risk: 'medium', reasons: ['Metadatos EXIF sospechosos'],                         gradient: gradients[3]! },
  { id: 'QRT-005', filename: 'campus_03.jpg',       album: 'ESPE Campus Universitario',   uploader: 'Marcos Escobar',  uploaderI: 'ME', date: '08/05 12:30', risk: 'high',   reasons: ['Marcador EOF attack', 'Payload oculto potencial'],   gradient: gradients[4]! },
])

const activeFilter = ref('all')
const searchQuery  = ref('')

const riskMap = {
  high:   { label: 'Alto',  color: '#EF4444', bg: '#FEF2F2' },
  medium: { label: 'Medio', color: '#F59E0B', bg: '#FFFBEB' },
}

const filteredImages = computed(() => {
  let list = images.value
  if (activeFilter.value !== 'all') list = list.filter(i => i.risk === activeFilter.value)
  const q = searchQuery.value.toLowerCase().trim()
  if (q) list = list.filter(i => i.filename.toLowerCase().includes(q) || i.album.toLowerCase().includes(q) || i.uploader.toLowerCase().includes(q))
  return list
})

const highCount   = computed(() => images.value.filter(i => i.risk === 'high').length)
const mediumCount = computed(() => images.value.filter(i => i.risk === 'medium').length)

function approve(id: string) {
  images.value = images.value.filter(i => i.id !== id)
}

function reject(id: string) {
  images.value = images.value.filter(i => i.id !== id)
}
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="workflow-tag">CUARENTENA</div>
        <h2 class="page-title">Bandeja de Imágenes en Cuarentena</h2>
        <p class="page-sub">
          Imágenes marcadas por el análisis automático LSB/MIME. Decide si aprobar (ignorar alerta) o rechazar (eliminar archivo).
        </p>
      </div>
    </div>

    <div class="stats-row">
      <div class="stat-chip stat-chip--danger">
        <span class="stat-chip__dot" style="background:#EF4444"></span>
        <strong>{{ highCount }}</strong> riesgo alto
      </div>
      <div class="stat-chip stat-chip--warn">
        <span class="stat-chip__dot" style="background:#F59E0B"></span>
        <strong>{{ mediumCount }}</strong> riesgo medio
      </div>
      <div class="stat-chip">
        <strong>{{ images.length }}</strong> total por revisar
      </div>
    </div>

    <div class="toolbar">
      <div class="filter-tabs">
        <button v-for="f in [{ key:'all', label:'Todas' }, { key:'high', label:'Riesgo Alto' }, { key:'medium', label:'Riesgo Medio' }]"
          :key="f.key"
          class="filter-tab"
          :class="{ 'filter-tab--active': activeFilter === f.key }"
          @click="activeFilter = f.key"
        >{{ f.label }}</button>
      </div>

      <div class="search-wrap">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
          <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input v-model="searchQuery" type="text" class="search-input" placeholder="Buscar imagen, álbum..." />
      </div>
    </div>

    <div v-if="filteredImages.length > 0" class="image-grid">
      <div v-for="img in filteredImages" :key="img.id" class="image-card">

        <div class="image-thumb" :style="{ background: `linear-gradient(135deg, ${img.gradient.from}, ${img.gradient.to})` }">
          <div class="risk-overlay" :style="{ background: riskMap[img.risk].bg, color: riskMap[img.risk].color }">
            <span class="risk-dot" :style="{ background: riskMap[img.risk].color }"></span>
            Riesgo {{ riskMap[img.risk].label }}
          </div>
          <svg class="photo-icon" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="3"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <path d="M21 15l-5-5L5 21"/>
          </svg>
          <div class="scan-lines"></div>
        </div>

        <div class="card-body">
          <div class="card-top">
            <span class="img-filename">{{ img.filename }}</span>
            <span class="img-id">{{ img.id }}</span>
          </div>

          <p class="img-album">📁 {{ img.album }}</p>

          <div class="uploader-row">
            <div class="uploader-avatar">{{ img.uploaderI }}</div>
            <span class="uploader-name">{{ img.uploader }}</span>
            <span class="img-date">{{ img.date }}</span>
          </div>

          <div class="reasons">
            <p class="reasons-label">Motivos del marcado:</p>
            <ul class="reasons-list">
              <li v-for="reason in img.reasons" :key="reason" class="reason-item">
                <span class="reason-icon">⚠</span>
                {{ reason }}
              </li>
            </ul>
          </div>
        </div>

        <div class="card-actions">
          <button class="action-approve" @click="approve(img.id)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" width="14" height="14">
              <path d="M20 6L9 17l-5-5"/>
            </svg>
            Aprobar (Ignorar alerta)
          </button>
          <button class="action-reject" @click="reject(img.id)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" width="14" height="14">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
            Rechazar (Eliminar)
          </button>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">🛡</div>
      <h3 class="empty-title">Sin imágenes en cuarentena</h3>
      <p class="empty-sub">Todas las imágenes han sido revisadas. Buen trabajo.</p>
    </div>
  </div>
</template>

<style scoped>
.page { display: flex; flex-direction: column; gap: 1.25rem; }

.page-header { }

.workflow-tag {
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #F59E0B;
  text-transform: uppercase;
  margin-bottom: 0.25rem;
}

.page-title { font-size: 1.4rem; font-weight: 800; color: #111827; margin: 0 0 0.3rem; }
.page-sub { font-size: 0.82rem; color: #6B7280; margin: 0; line-height: 1.55; max-width: 680px; }

.stats-row { display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; }

.stat-chip {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.85rem;
  border-radius: 99px;
  font-size: 0.78rem;
  background: white;
  border: 1px solid #E5E7EB;
  color: #374151;
}

.stat-chip--danger { border-color: #FECACA; background: #FEF2F2; color: #B91C1C; }
.stat-chip--warn   { border-color: #FDE68A; background: #FFFBEB; color: #92400E; }

.stat-chip__dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }

.toolbar { display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; }

.filter-tabs { display: flex; gap: 0.25rem; background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 0.25rem; }

.filter-tab {
  padding: 0.35rem 0.9rem;
  border-radius: 6px;
  border: none;
  background: none;
  font-family: inherit;
  font-size: 0.8rem;
  font-weight: 500;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}

.filter-tab:hover { color: #374151; background: #F9FAFB; }
.filter-tab--active { background: #F59E0B; color: white; font-weight: 600; }

.search-wrap { position: relative; }

.search-icon {
  position: absolute;
  left: 0.75rem; top: 50%;
  transform: translateY(-50%);
  width: 16px; height: 16px;
  color: #9CA3AF;
  pointer-events: none;
}

.search-input {
  padding: 0.55rem 0.85rem 0.55rem 2.25rem;
  border: 1.5px solid #E5E7EB;
  border-radius: 7px;
  font-family: inherit;
  font-size: 0.85rem;
  color: #111827;
  background: white;
  outline: none;
  width: 240px;
  box-sizing: border-box;
  transition: border-color 0.15s;
}

.search-input:focus { border-color: #F59E0B; }

.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.image-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.2s;
}

.image-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); }

.image-thumb {
  position: relative;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.photo-icon {
  width: 36px; height: 36px;
  pointer-events: none;
  z-index: 1;
}

.scan-lines {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 4px,
    rgba(0,0,0,0.04) 4px,
    rgba(0,0,0,0.04) 5px
  );
  pointer-events: none;
}

.risk-overlay {
  position: absolute;
  top: 0.6rem; left: 0.6rem;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.25rem 0.6rem;
  border-radius: 99px;
  font-size: 0.65rem;
  font-weight: 700;
  z-index: 2;
}

.risk-dot { width: 6px; height: 6px; border-radius: 50%; }

.card-body {
  padding: 0.9rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}

.card-top { display: flex; align-items: center; justify-content: space-between; }

.img-filename { font-size: 0.85rem; font-weight: 700; color: #111827; }
.img-id { font-size: 0.68rem; color: #9CA3AF; font-weight: 500; }

.img-album { font-size: 0.75rem; color: #6B7280; margin: 0; }

.uploader-row { display: flex; align-items: center; gap: 0.45rem; }

.uploader-avatar {
  width: 22px; height: 22px;
  background: linear-gradient(135deg, #F59E0B, #D97706);
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.58rem;
  font-weight: 700;
  flex-shrink: 0;
}

.uploader-name { font-size: 0.75rem; color: #374151; font-weight: 500; flex: 1; }
.img-date { font-size: 0.68rem; color: #9CA3AF; }

.reasons { background: #FEF2F2; border: 1px solid #FECACA; border-radius: 6px; padding: 0.55rem 0.7rem; }
.reasons-label { font-size: 0.68rem; font-weight: 700; color: #B91C1C; text-transform: uppercase; letter-spacing: 0.06em; margin: 0 0 0.35rem; }

.reasons-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.2rem; }

.reason-item {
  display: flex;
  align-items: flex-start;
  gap: 0.35rem;
  font-size: 0.75rem;
  color: #7F1D1D;
  line-height: 1.4;
}

.reason-icon { font-size: 0.7rem; flex-shrink: 0; margin-top: 1px; }

.card-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  padding: 0.75rem 0.9rem;
  border-top: 1px solid #F3F4F6;
}

.action-approve, .action-reject {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  padding: 0.55rem 0.5rem;
  border-radius: 6px;
  font-family: inherit;
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  border: none;
}

.action-approve { background: #2E75B6; color: white; }
.action-approve:hover { background: #1E4D7B; }

.action-reject { background: white; color: #EF4444; border: 1.5px solid #EF4444; }
.action-reject:hover { background: #FEF2F2; }

.empty-state { text-align: center; padding: 5rem 2rem; }
.empty-icon { font-size: 3rem; margin: 0 0 1rem; }
.empty-title { font-size: 1.1rem; font-weight: 700; color: #374151; margin: 0 0 0.35rem; }
.empty-sub { font-size: 0.85rem; color: #9CA3AF; margin: 0; }

@media (max-width: 1000px) { .image-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .image-grid { grid-template-columns: 1fr; } }
</style>
