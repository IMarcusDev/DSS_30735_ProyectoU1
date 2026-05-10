<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { auditService, type AuditEntry } from '../../services/audit'
import { timeAgo } from '../../utils/time'

const entries  = ref<AuditEntry[]>([])
const loading  = ref(true)
const filter   = ref<string>('all')

onMounted(async () => {
  try {
    entries.value = await auditService.getMyLog()
  } catch {
    entries.value = []
  } finally {
    loading.value = false
  }
})

const actionMeta: Record<string, { label: string; color: string; bg: string; icon: string }> = {
  album_approved: { label: 'Álbum aprobado',   color: '#059669', bg: '#ECFDF5', icon: 'check'   },
  album_rejected: { label: 'Álbum rechazado',  color: '#DC2626', bg: '#FEF2F2', icon: 'x'       },
  image_approved: { label: 'Imagen aprobada',  color: '#2563EB', bg: '#EFF6FF', icon: 'shield'  },
  image_deleted:  { label: 'Imagen eliminada', color: '#DC2626', bg: '#FEF2F2', icon: 'trash'   },
}

const filterOptions = [
  { value: 'all',            label: 'Todo' },
  { value: 'album_approved', label: 'Álbumes aprobados' },
  { value: 'album_rejected', label: 'Álbumes rechazados' },
  { value: 'image_approved', label: 'Imágenes aprobadas' },
  { value: 'image_deleted',  label: 'Imágenes eliminadas' },
]

const filtered = computed(() =>
  filter.value === 'all' ? entries.value : entries.value.filter(e => e.action === filter.value)
)

const iconPaths: Record<string, string> = {
  check:  'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
  x:      'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
  shield: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
  trash:  'M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16',
}

const stats = computed(() => ({
  total:           entries.value.length,
  albumsApproved:  entries.value.filter(e => e.action === 'album_approved').length,
  albumsRejected:  entries.value.filter(e => e.action === 'album_rejected').length,
  imagesApproved:  entries.value.filter(e => e.action === 'image_approved').length,
  imagesDeleted:   entries.value.filter(e => e.action === 'image_deleted').length,
}))
</script>

<template>
  <div class="historial">
    <div class="stats-row">
      <div class="stat-card">
        <span class="stat-value">{{ stats.total }}</span>
        <span class="stat-label">Acciones totales</span>
      </div>
      <div class="stat-card stat-card--green">
        <span class="stat-value">{{ stats.albumsApproved }}</span>
        <span class="stat-label">Álbumes aprobados</span>
      </div>
      <div class="stat-card stat-card--red">
        <span class="stat-value">{{ stats.albumsRejected }}</span>
        <span class="stat-label">Álbumes rechazados</span>
      </div>
      <div class="stat-card stat-card--blue">
        <span class="stat-value">{{ stats.imagesApproved }}</span>
        <span class="stat-label">Imágenes aprobadas</span>
      </div>
      <div class="stat-card stat-card--red">
        <span class="stat-value">{{ stats.imagesDeleted }}</span>
        <span class="stat-label">Imágenes eliminadas</span>
      </div>
    </div>

    <div class="timeline-card">
      <div class="card-header">
        <div>
          <h3 class="card-title">Registro de actividad</h3>
          <p class="card-sub">Tus últimas {{ entries.length }} acciones como supervisor</p>
        </div>

        <div class="filter-tabs">
          <button
            v-for="opt in filterOptions"
            :key="opt.value"
            class="filter-tab"
            :class="{ 'filter-tab--active': filter === opt.value }"
            @click="filter = opt.value"
          >
            {{ opt.label }}
          </button>
        </div>
      </div>

      <!-- Loading skeletons -->
      <div v-if="loading" class="skeleton-list">
        <div v-for="n in 6" :key="n" class="skeleton-entry">
          <div class="sk-icon"></div>
          <div class="sk-lines">
            <div class="sk-line sk-line--main"></div>
            <div class="sk-line sk-line--sub"></div>
          </div>
        </div>
      </div>

      <div v-else-if="filtered.length === 0" class="empty-state">
        <div class="empty-icon">📋</div>
        <p class="empty-title">Sin actividad registrada</p>
        <p class="empty-sub">Las aprobaciones y rechazos que realices aparecerán aquí.</p>
      </div>

      <div v-else class="timeline">
        <div
          v-for="(entry, idx) in filtered"
          :key="entry.audit_id"
          class="timeline-entry"
          :class="{ 'timeline-entry--last': idx === filtered.length - 1 }"
        >
          <div class="tl-left">
            <div
              class="tl-icon"
              :style="{ background: actionMeta[entry.action]?.bg, color: actionMeta[entry.action]?.color }"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path :d="iconPaths[actionMeta[entry.action]?.icon ?? 'check']" />
              </svg>
            </div>
            <div v-if="idx < filtered.length - 1" class="tl-line"></div>
          </div>

          <div class="tl-body">
            <div class="tl-header">
              <span
                class="tl-badge"
                :style="{ background: actionMeta[entry.action]?.bg, color: actionMeta[entry.action]?.color }"
              >
                {{ actionMeta[entry.action]?.label }}
              </span>
              <span class="tl-time">{{ timeAgo(entry.timestamp) }}</span>
            </div>
            <p class="tl-name">{{ entry.target_name }}</p>
            <p class="tl-meta">
              {{ entry.target_type === 'album' ? 'Álbum' : 'Imagen' }}
              · ID {{ entry.target_id.slice(0, 8) }}…
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.historial { display: flex; flex-direction: column; gap: 1.25rem; }

.stats-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.85rem;
}

.stat-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  padding: 1rem 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-card--green  { border-left: 3px solid #059669; }
.stat-card--red    { border-left: 3px solid #DC2626; }
.stat-card--blue   { border-left: 3px solid #2563EB; }

.stat-value { font-size: 1.6rem; font-weight: 800; color: #111827; line-height: 1; }
.stat-label { font-size: 0.72rem; color: #6B7280; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }

.timeline-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 1.1rem 1.5rem 0.75rem;
  gap: 1rem;
  flex-wrap: wrap;
  border-bottom: 1px solid #F3F4F6;
}

.card-title { font-size: 0.9rem; font-weight: 700; color: #111827; margin: 0; }
.card-sub   { font-size: 0.75rem; color: #9CA3AF; margin: 0.2rem 0 0; }

.filter-tabs { display: flex; gap: 0.35rem; flex-wrap: wrap; }

.filter-tab {
  font-family: inherit;
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
  border: 1.5px solid #E5E7EB;
  background: white;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.15s;
}

.filter-tab:hover { border-color: #D1D5DB; color: #374151; }
.filter-tab--active { background: #F59E0B; border-color: #F59E0B; color: white; font-weight: 600; }

.skeleton-list { padding: 1rem 1.5rem; display: flex; flex-direction: column; gap: 1.25rem; }
.skeleton-entry { display: flex; align-items: flex-start; gap: 1rem; }
.sk-icon { width: 36px; height: 36px; border-radius: 50%; background: #E5E7EB; flex-shrink: 0; animation: shimmer 1.5s infinite; }
.sk-lines { flex: 1; display: flex; flex-direction: column; gap: 0.4rem; }
.sk-line { background: #E5E7EB; border-radius: 4px; animation: shimmer 1.5s infinite; }
.sk-line--main { height: 14px; width: 55%; }
.sk-line--sub  { height: 11px; width: 35%; }
@keyframes shimmer { 0%,100%{opacity:1} 50%{opacity:0.5} }

.empty-state { text-align: center; padding: 3rem 1rem; display: flex; flex-direction: column; align-items: center; gap: 0.4rem; }
.empty-icon  { font-size: 2rem; }
.empty-title { font-size: 0.9rem; font-weight: 600; color: #374151; margin: 0; }
.empty-sub   { font-size: 0.78rem; color: #9CA3AF; margin: 0; }

.timeline { padding: 1rem 1.5rem; display: flex; flex-direction: column; }

.timeline-entry {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.tl-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.tl-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tl-icon svg { width: 18px; height: 18px; }

.tl-line {
  width: 2px;
  flex: 1;
  min-height: 24px;
  background: #F3F4F6;
  margin: 4px 0;
}

.tl-body { padding: 0.1rem 0 1.25rem; flex: 1; min-width: 0; }

.tl-header { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.3rem; }

.tl-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.15rem 0.55rem;
  border-radius: 20px;
}

.tl-time { font-size: 0.72rem; color: #9CA3AF; margin-left: auto; white-space: nowrap; }

.tl-name {
  font-size: 0.87rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 0.15rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tl-meta { font-size: 0.72rem; color: #9CA3AF; margin: 0; }

@media (max-width: 1100px) { .stats-row { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px)  { .stats-row { grid-template-columns: repeat(2, 1fr); } }
</style>
