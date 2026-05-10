<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { albumsService } from '../../services/albums'
import { imagesService } from '../../services/images'
import { timeAgo, hoursAgo } from '../../utils/time'

const pendingAlbums  = ref([])
const suspiciousImgs = ref([])
const loading        = ref(true)

onMounted(async () => {
  try {
    const [albums, images] = await Promise.all([
      albumsService.getPending(),
      imagesService.getSuspicious(),
    ])
    pendingAlbums.value  = albums
    suspiciousImgs.value = images
  } catch {
    pendingAlbums.value  = []
    suspiciousImgs.value = []
  } finally {
    loading.value = false
  }
})

const kpis = computed(() => [
  {
    label: 'Solicitudes pendientes',
    value: pendingAlbums.value.length,
    delta: 'álbumes por aprobar',
    color: '#F59E0B', bg: '#FFFBEB', icon: '📋',
  },
  {
    label: 'Imágenes en cuarentena',
    value: suspiciousImgs.value.length,
    delta: 'requieren revisión',
    color: '#EF4444', bg: '#FEF2F2', icon: '🛡',
  },
  {
    label: 'Riesgo alto',
    value: suspiciousImgs.value.filter(i => i.image.image_state === 'Positivo').length,
    delta: 'estado Positivo',
    color: '#DC2626', bg: '#FEF2F2', icon: '⚠',
  },
  {
    label: 'Riesgo medio',
    value: suspiciousImgs.value.filter(i => i.image.image_state === 'Sospechoso').length,
    delta: 'estado Sospechoso',
    color: '#F59E0B', bg: '#FFFBEB', icon: '⚡',
  },
])

const riskMap = { Positivo: { label: 'Alto', color: '#EF4444', bg: '#FEF2F2' }, Sospechoso: { label: 'Medio', color: '#F59E0B', bg: '#FFFBEB' } }

function priorityColor(iso) {
  const h = hoursAgo(iso)
  return h > 48 ? '#EF4444' : h > 24 ? '#F59E0B' : '#9CA3AF'
}

function priorityLabel(iso) {
  const h = hoursAgo(iso)
  return h > 48 ? 'Urgente' : h > 24 ? 'Media' : 'Normal'
}
</script>

<template>
  <div class="dashboard">
    <!-- KPIs -->
    <div class="kpi-grid">
      <div v-for="kpi in kpis" :key="kpi.label" class="kpi-card">
        <div class="kpi-icon" :style="{ background: kpi.bg, color: kpi.color }">{{ kpi.icon }}</div>
        <div class="kpi-body">
          <p class="kpi-label">{{ kpi.label }}</p>
          <div v-if="loading" class="skeleton-val"></div>
          <p v-else class="kpi-value" :style="{ color: kpi.color }">{{ kpi.value }}</p>
          <p class="kpi-delta">{{ kpi.delta }}</p>
        </div>
      </div>
    </div>

    <div class="bottom-row">
      <div class="card">
        <div class="card-header">
          <div>
            <h3 class="card-title">Cola de solicitudes</h3>
            <p class="card-sub">Álbumes esperando aprobación</p>
          </div>
          <RouterLink to="/supervisor/solicitudes" class="card-link">Ver todas →</RouterLink>
        </div>

        <div v-if="loading" class="loading-rows">
          <div v-for="n in 3" :key="n" class="skeleton-row"></div>
        </div>

        <div v-else-if="pendingAlbums.length === 0" class="empty-state">
          <p class="empty-icon">✓</p>
          <p class="empty-title">Sin solicitudes pendientes</p>
          <p class="empty-sub">Todas las solicitudes han sido procesadas.</p>
        </div>

        <table v-else class="data-table">
          <thead>
            <tr>
              <th>PRIORIDAD</th>
              <th>ÁLBUM</th>
              <th>USUARIO</th>
              <th>ESPERA</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="req in pendingAlbums.slice(0, 5)" :key="req.id">
              <td>
                <div class="priority-cell">
                  <span class="priority-dot" :style="{ background: priorityColor(req.date_created) }"></span>
                  <span :style="{ color: priorityColor(req.date_created), fontWeight: 600, fontSize: '0.78rem' }">
                    {{ priorityLabel(req.date_created) }}
                  </span>
                </div>
              </td>
              <td>
                <p class="td-main">{{ req.name }}</p>
                <p class="td-sub">{{ req.id.slice(0, 8) }}…</p>
              </td>
              <td class="td-muted">{{ req.owner?.name ?? '—' }}</td>
              <td class="td-muted">{{ timeAgo(req.date_created) }}</td>
              <td>
                <RouterLink to="/supervisor/solicitudes" class="action-btn">Revisar</RouterLink>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card card--narrow">
        <div class="card-header">
          <h3 class="card-title">Cuarentena reciente</h3>
          <RouterLink to="/supervisor/cuarentena" class="card-link">Ver →</RouterLink>
        </div>

        <div v-if="loading" class="loading-rows">
          <div v-for="n in 3" :key="n" class="skeleton-row"></div>
        </div>

        <div v-else-if="suspiciousImgs.length === 0" class="empty-state">
          <p class="empty-icon">🛡</p>
          <p class="empty-title">Sin imágenes en cuarentena</p>
        </div>

        <ul v-else class="quarantine-list">
          <li v-for="item in suspiciousImgs.slice(0, 5)" :key="item.image.image_id" class="quarantine-item">
            <div class="q-filename">
              <span class="q-name">{{ item.image.image_name }}</span>
              <span class="q-risk" :style="{ color: riskMap[item.image.image_state]?.color ?? '#9CA3AF', background: riskMap[item.image.image_state]?.bg ?? '#F3F4F6' }">
                {{ riskMap[item.image.image_state]?.label ?? item.image.image_state }}
              </span>
            </div>
            <p class="q-uploader">Por {{ item.owner.name }}</p>
            <p class="q-date">{{ timeAgo(item.image.image_date_uploaded) }}</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 1.25rem; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.kpi-card { background: white; border: 1px solid #E5E7EB; border-radius: 10px; padding: 1.25rem; display: flex; align-items: center; gap: 1rem; }
.kpi-icon { width: 46px; height: 46px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0; }
.kpi-label { font-size: 0.72rem; font-weight: 500; color: #6B7280; margin: 0; text-transform: uppercase; letter-spacing: 0.04em; }
.kpi-value { font-size: 1.75rem; font-weight: 800; margin: 0.1rem 0; line-height: 1; }
.kpi-delta { font-size: 0.72rem; color: #9CA3AF; margin: 0; }
.skeleton-val { height: 28px; width: 48px; background: #E5E7EB; border-radius: 4px; margin: 0.1rem 0; animation: shimmer 1.5s infinite; }
@keyframes shimmer { 0%,100%{opacity:1} 50%{opacity:0.5} }

.bottom-row { display: grid; grid-template-columns: 1fr 300px; gap: 1rem; align-items: start; }

.card { background: white; border: 1px solid #E5E7EB; border-radius: 10px; overflow: hidden; }
.card-header { display: flex; align-items: center; justify-content: space-between; padding: 1.1rem 1.25rem 0; }
.card-title { font-size: 0.9rem; font-weight: 700; color: #111827; margin: 0; }
.card-sub { font-size: 0.75rem; color: #9CA3AF; margin: 0.2rem 0 0; }
.card-link { font-size: 0.8rem; color: #2E75B6; text-decoration: none; font-weight: 500; }
.card-link:hover { text-decoration: underline; }

.loading-rows { display: flex; flex-direction: column; gap: 0; padding: 0.5rem 0; }
.skeleton-row { height: 52px; background: linear-gradient(90deg, #F9FAFB 25%, #F3F4F6 50%, #F9FAFB 75%); background-size: 200% 100%; animation: slide 1.5s infinite; border-bottom: 1px solid #F3F4F6; }
@keyframes slide { 0%{background-position:200% 0} 100%{background-position:-200% 0} }

.empty-state { text-align: center; padding: 2rem 1rem; display: flex; flex-direction: column; align-items: center; gap: 0.3rem; }
.empty-icon { font-size: 1.75rem; margin: 0; }
.empty-title { font-size: 0.85rem; font-weight: 600; color: #374151; margin: 0; }
.empty-sub { font-size: 0.75rem; color: #9CA3AF; margin: 0; }

.data-table { width: 100%; border-collapse: collapse; margin-top: 0.75rem; }
.data-table th { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.07em; text-transform: uppercase; color: #9CA3AF; padding: 0.6rem 1rem; text-align: left; background: #F9FAFB; border-bottom: 1px solid #F3F4F6; }
.data-table td { padding: 0.8rem 1rem; border-bottom: 1px solid #F3F4F6; font-size: 0.83rem; color: #374151; vertical-align: middle; }
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: #FAFAFA; }

.priority-cell { display: flex; align-items: center; gap: 0.45rem; }
.priority-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }
.td-main { font-weight: 600; color: #111827; margin: 0; font-size: 0.83rem; }
.td-sub { font-size: 0.7rem; color: #9CA3AF; margin: 0.1rem 0 0; }
.td-muted { color: #9CA3AF; font-size: 0.8rem; }

.action-btn { font-size: 0.78rem; font-weight: 600; padding: 0.25rem 0.65rem; background: #2E75B6; color: white; border-radius: 5px; text-decoration: none; transition: background 0.15s; }
.action-btn:hover { background: #1E4D7B; }

.quarantine-list { list-style: none; margin: 0.75rem 0 0; padding: 0; }
.quarantine-item { padding: 0.75rem 1.25rem; border-bottom: 1px solid #F3F4F6; }
.quarantine-item:last-child { border-bottom: none; }
.q-filename { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; margin-bottom: 0.2rem; }
.q-name { font-size: 0.82rem; font-weight: 600; color: #111827; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 130px; }
.q-risk { font-size: 0.65rem; font-weight: 700; padding: 0.15rem 0.45rem; border-radius: 4px; flex-shrink: 0; }
.q-uploader { font-size: 0.75rem; color: #6B7280; margin: 0 0 0.1rem; }
.q-date { font-size: 0.7rem; color: #9CA3AF; margin: 0; }

@media (max-width: 1100px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 900px) { .bottom-row { grid-template-columns: 1fr; } }
</style>
