<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { albumsService } from '../../services/albums'

const albums  = ref([])
const loading = ref(true)

const stateToKey = { 'Aprobado': 'approved', 'Pendiente': 'pending', 'Negado': 'rejected' }

const statusMap = {
  approved: { label: 'Aprobado',  color: '#10B981', bg: '#ECFDF5' },
  pending:  { label: 'Pendiente', color: '#F59E0B', bg: '#FFFBEB' },
  rejected: { label: 'Rechazado', color: '#EF4444', bg: '#FEF2F2' },
}

onMounted(async () => {
  try {
    const data = await albumsService.getMine()
    albums.value = data.map(a => ({
      id:       a.id,
      title:    a.name,
      privacy:  a.is_public ? 'Público' : 'Privado',
      status:   stateToKey[a.state] ?? 'pending',
      date:     new Date(a.date_created).toLocaleDateString('es-EC'),
    }))
  } catch {
    albums.value = []
  } finally {
    loading.value = false
  }
})

const kpis = computed(() => [
  {
    label: 'Álbumes aprobados',
    value: albums.value.filter(a => a.status === 'approved').length,
    delta: 'de ' + albums.value.length + ' total',
    color: '#10B981', bg: '#ECFDF5', icon: '✓',
  },
  {
    label: 'Pendientes revisión',
    value: albums.value.filter(a => a.status === 'pending').length,
    delta: 'esperando aprobación',
    color: '#F59E0B', bg: '#FFFBEB', icon: '⏳',
  },
  {
    label: 'Rechazados',
    value: albums.value.filter(a => a.status === 'rejected').length,
    delta: 'solicitudes denegadas',
    color: '#EF4444', bg: '#FEF2F2', icon: '✕',
  },
  {
    label: 'Total álbumes',
    value: albums.value.length,
    delta: 'en tu cuenta',
    color: '#2E75B6', bg: '#EFF6FF', icon: '📁',
  },
])

const recentAlbums = computed(() => albums.value.slice(0, 5))
</script>

<template>
  <div class="dashboard">

    <div class="kpi-grid">
      <div v-for="kpi in kpis" :key="kpi.label" class="kpi-card">
        <div class="kpi-card__icon" :style="{ background: kpi.bg, color: kpi.color }">
          {{ kpi.icon }}
        </div>
        <div class="kpi-card__body">
          <p class="kpi-label">{{ kpi.label }}</p>
          <div v-if="loading" class="skeleton-val"></div>
          <p v-else class="kpi-value" :style="{ color: kpi.color }">{{ kpi.value }}</p>
          <p class="kpi-delta">{{ kpi.delta }}</p>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div>
          <h3 class="card-title">Mis álbumes recientes</h3>
          <p class="card-sub">Últimas solicitudes y álbumes activos</p>
        </div>
        <RouterLink to="/user/albums/new" class="btn-primary">+ Solicitar álbum</RouterLink>
      </div>

      <div v-if="loading" class="loading-rows">
        <div v-for="n in 3" :key="n" class="skeleton-row"></div>
      </div>

      <div v-else-if="recentAlbums.length === 0" class="empty-state">
        <p class="empty-icon">📁</p>
        <p class="empty-title">Aún no tienes álbumes</p>
        <p class="empty-sub">Solicita tu primer álbum para comenzar a subir imágenes.</p>
        <RouterLink to="/user/albums/new" class="btn-primary" style="margin-top:0.5rem">Solicitar álbum →</RouterLink>
      </div>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>ÁLBUM</th>
            <th>PRIVACIDAD</th>
            <th>FECHA</th>
            <th>ESTADO</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="album in recentAlbums" :key="album.id">
            <td>
              <p class="td-main">{{ album.title }}</p>
              <p class="td-sub">{{ album.id }}</p>
            </td>
            <td>
              <span class="privacy-badge" :class="album.privacy === 'Público' ? 'privacy-badge--pub' : 'privacy-badge--priv'">
                {{ album.privacy }}
              </span>
            </td>
            <td class="td-muted">{{ album.date }}</td>
            <td>
              <span class="status-badge" :style="{ color: statusMap[album.status].color, background: statusMap[album.status].bg }">
                <span class="status-dot" :style="{ background: statusMap[album.status].color }"></span>
                {{ statusMap[album.status].label }}
              </span>
            </td>
            <td>
              <div class="row-actions">
                <RouterLink to="/user/albums" class="action-link">Ver todos</RouterLink>
                <RouterLink v-if="album.status === 'approved'" to="/user/upload" class="action-btn">Subir</RouterLink>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="!loading && recentAlbums.length > 0" class="card-footer">
        <RouterLink to="/user/albums" class="footer-link">Ver todos los álbumes →</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 1.5rem; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }

.kpi-card { background: white; border: 1px solid #E5E7EB; border-radius: 10px; padding: 1.25rem; display: flex; align-items: center; gap: 1rem; }
.kpi-card__icon { width: 46px; height: 46px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0; }
.kpi-label { font-size: 0.72rem; font-weight: 500; color: #6B7280; margin: 0; text-transform: uppercase; letter-spacing: 0.04em; }
.kpi-value { font-size: 1.75rem; font-weight: 800; margin: 0.1rem 0; line-height: 1; }
.kpi-delta { font-size: 0.72rem; color: #9CA3AF; margin: 0; }

.skeleton-val { height: 28px; width: 48px; background: #E5E7EB; border-radius: 4px; margin: 0.1rem 0; animation: shimmer 1.5s infinite; }
@keyframes shimmer { 0%{opacity:1} 50%{opacity:0.5} 100%{opacity:1} }

.card { background: white; border: 1px solid #E5E7EB; border-radius: 10px; overflow: hidden; }
.card-header { display: flex; align-items: center; justify-content: space-between; padding: 1.25rem 1.25rem 0; gap: 1rem; }
.card-title { font-size: 0.95rem; font-weight: 700; color: #111827; margin: 0; }
.card-sub { font-size: 0.78rem; color: #9CA3AF; margin: 0.2rem 0 0; }
.card-footer { padding: 0.85rem 1.25rem; border-top: 1px solid #F3F4F6; }
.footer-link { font-size: 0.82rem; color: #2E75B6; text-decoration: none; font-weight: 500; }
.footer-link:hover { text-decoration: underline; }

.btn-primary { display: inline-block; background: #2E75B6; color: white; font-size: 0.82rem; font-weight: 600; padding: 0.5rem 1rem; border-radius: 7px; text-decoration: none; white-space: nowrap; transition: background 0.15s; }
.btn-primary:hover { background: #1E4D7B; }

.loading-rows { display: flex; flex-direction: column; gap: 0; padding: 0.5rem 0; }
.skeleton-row { height: 52px; background: linear-gradient(90deg, #F9FAFB 25%, #F3F4F6 50%, #F9FAFB 75%); background-size: 200% 100%; animation: slide 1.5s infinite; border-bottom: 1px solid #F3F4F6; }
@keyframes slide { 0%{background-position:200% 0} 100%{background-position:-200% 0} }

.empty-state { text-align: center; padding: 3rem 1.5rem; display: flex; flex-direction: column; align-items: center; gap: 0.4rem; }
.empty-icon { font-size: 2rem; margin: 0; }
.empty-title { font-size: 0.95rem; font-weight: 600; color: #374151; margin: 0; }
.empty-sub { font-size: 0.8rem; color: #9CA3AF; margin: 0; }

.data-table { width: 100%; border-collapse: collapse; margin-top: 0.75rem; }
.data-table th { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.07em; text-transform: uppercase; color: #9CA3AF; padding: 0.6rem 1rem; text-align: left; background: #F9FAFB; border-top: 1px solid #F3F4F6; border-bottom: 1px solid #F3F4F6; }
.data-table td { padding: 0.85rem 1rem; border-bottom: 1px solid #F3F4F6; font-size: 0.85rem; color: #374151; vertical-align: middle; }
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: #FAFAFA; }

.td-main { font-weight: 600; color: #111827; margin: 0; font-size: 0.85rem; }
.td-sub { font-size: 0.72rem; color: #9CA3AF; margin: 0.1rem 0 0; }
.td-muted { color: #9CA3AF; font-size: 0.82rem; }

.status-badge { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.25rem 0.65rem; border-radius: 99px; font-size: 0.75rem; font-weight: 600; }
.status-dot { width: 6px; height: 6px; border-radius: 50%; }
.privacy-badge { font-size: 0.72rem; font-weight: 500; padding: 0.2rem 0.5rem; border-radius: 4px; }
.privacy-badge--pub { background: #EFF6FF; color: #2E75B6; }
.privacy-badge--priv { background: #F3F4F6; color: #6B7280; }

.row-actions { display: flex; gap: 0.4rem; align-items: center; }
.action-link { font-size: 0.8rem; color: #2E75B6; text-decoration: none; font-weight: 500; }
.action-link:hover { text-decoration: underline; }
.action-btn { font-size: 0.78rem; font-weight: 600; padding: 0.25rem 0.65rem; background: #2E75B6; color: white; border-radius: 5px; text-decoration: none; transition: background 0.15s; }
.action-btn:hover { background: #1E4D7B; }

@media (max-width: 1100px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .kpi-grid { grid-template-columns: 1fr 1fr; } }
</style>
