<script setup>
import { RouterLink } from 'vue-router'

const kpis = [
  { label: 'Solicitudes pendientes', value: 3,  delta: '+1 hoy',          color: '#F59E0B', bg: '#FFFBEB', icon: '📋' },
  { label: 'Imágenes en cuarentena', value: 5,  delta: 'Requieren acción',color: '#EF4444', bg: '#FEF2F2', icon: '🛡' },
  { label: 'Aprobadas hoy',          value: 2,  delta: 'vs 1 ayer',        color: '#10B981', bg: '#ECFDF5', icon: '✓' },
  { label: 'Tiempo prom. revisión',  value: '4h', delta: 'meta: 24h',       color: '#2E75B6', bg: '#EFF6FF', icon: '⏱' },
]

const priorityMap = {
  urgent: { label: 'Urgente', color: '#EF4444' },
  media:  { label: 'Media',   color: '#F59E0B' },
  normal: { label: 'Normal',  color: '#9CA3AF' },
}

const recentRequests = [
  { id: 'REQ-045', title: 'Paisajes de los Andes',           user: 'Jorge Morales',   time: 'hace 2d',  priority: 'urgent' },
  { id: 'REQ-044', title: 'Naturaleza en Cotacachi',         user: 'Ana Vázquez',     time: 'hace 1d',  priority: 'urgent' },
  { id: 'REQ-043', title: 'Ciudad de Guayaquil',             user: 'Carlos Reyes',    time: 'hace 18h', priority: 'media'  },
  { id: 'REQ-042', title: 'Mercado Artesanal Otavalo',       user: 'Lucía Paz',       time: 'hace 14h', priority: 'media'  },
  { id: 'REQ-041', title: 'ESPE Campus Universitario',       user: 'Marcos Escobar',  time: 'hace 8h',  priority: 'normal' },
]

const recentQuarantine = [
  { id: 'QRT-001', filename: 'foto_012.jpg',         album: 'Proyecto ESPE 2025',           reason: 'LSB anomaly + EOF marker', risk: 'high'   },
  { id: 'QRT-002', filename: 'arquitectura_05.jpg',  album: 'Arquitectura Histórica Quito', reason: 'Histograma anómalo',        risk: 'medium' },
  { id: 'QRT-003', filename: 'paisaje_001.jpg',      album: 'Paisajes de los Andes',        reason: 'LSB anomaly detectado',     risk: 'high'   },
  { id: 'QRT-004', filename: 'mercado_07.jpg',       album: 'Mercado Artesanal Otavalo',    reason: 'Metadatos EXIF sospechosos',risk: 'medium' },
  { id: 'QRT-005', filename: 'campus_03.jpg',        album: 'ESPE Campus Universitario',    reason: 'EOF attack marker',          risk: 'high'   },
]

const riskMap = {
  high:   { label: 'Alto',  color: '#EF4444', bg: '#FEF2F2' },
  medium: { label: 'Medio', color: '#F59E0B', bg: '#FFFBEB' },
}

const activity = [
  { msg: 'Álbum "Arquitectura Histórica Quito" aprobado',     time: 'hace 1h',  color: '#10B981', icon: '✓' },
  { msg: 'Imagen "foto_012.jpg" enviada a cuarentena',        time: 'hace 3h',  color: '#EF4444', icon: '⚠' },
  { msg: 'Álbum "Laboratorio DSS 2026" rechazado',            time: 'hace 5h',  color: '#6B7280', icon: '✕' },
  { msg: 'Nueva solicitud: "Paisajes de los Andes"',          time: 'hace 2d',  color: '#2E75B6', icon: '+' },
]
</script>

<template>
  <div class="dashboard">
    <div class="kpi-grid">
      <div v-for="kpi in kpis" :key="kpi.label" class="kpi-card">
        <div class="kpi-icon" :style="{ background: kpi.bg, color: kpi.color }">
          {{ kpi.icon }}
        </div>
        <div class="kpi-body">
          <p class="kpi-label">{{ kpi.label }}</p>
          <p class="kpi-value" :style="{ color: kpi.color }">{{ kpi.value }}</p>
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

        <table class="data-table">
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
            <tr v-for="req in recentRequests" :key="req.id">
              <td>
                <div class="priority-cell">
                  <span class="priority-dot" :style="{ background: priorityMap[req.priority].color }"></span>
                  <span class="priority-label" :style="{ color: priorityMap[req.priority].color }">
                    {{ priorityMap[req.priority].label }}
                  </span>
                </div>
              </td>
              <td>
                <p class="td-main">{{ req.title }}</p>
                <p class="td-sub">{{ req.id }}</p>
              </td>
              <td class="td-muted">{{ req.user }}</td>
              <td class="td-muted">{{ req.time }}</td>
              <td>
                <RouterLink to="/supervisor/solicitudes" class="action-btn">Revisar</RouterLink>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="side-col">
        <div class="card">
          <div class="card-header">
            <h3 class="card-title">Cuarentena reciente</h3>
            <RouterLink to="/supervisor/cuarentena" class="card-link">Ver →</RouterLink>
          </div>
          <ul class="quarantine-list">
            <li v-for="img in recentQuarantine" :key="img.id" class="quarantine-item">
              <div class="q-filename">
                <span class="q-name">{{ img.filename }}</span>
                <span class="q-risk" :style="{ color: riskMap[img.risk].color, background: riskMap[img.risk].bg }">
                  {{ riskMap[img.risk].label }}
                </span>
              </div>
              <p class="q-album">{{ img.album }}</p>
              <p class="q-reason">{{ img.reason }}</p>
            </li>
          </ul>
        </div>

        <div class="card card--compact">
          <div class="card-header">
            <h3 class="card-title">Actividad reciente</h3>
          </div>
          <ul class="activity-list">
            <li v-for="item in activity" :key="item.msg" class="activity-item">
              <div class="activity-icon" :style="{ color: item.color, background: item.color + '18' }">
                {{ item.icon }}
              </div>
              <div>
                <p class="activity-msg">{{ item.msg }}</p>
                <p class="activity-time">{{ item.time }}</p>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 1.25rem; }

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.kpi-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.kpi-icon {
  width: 46px; height: 46px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.kpi-label { font-size: 0.72rem; font-weight: 500; color: #6B7280; margin: 0; text-transform: uppercase; letter-spacing: 0.04em; }
.kpi-value { font-size: 1.75rem; font-weight: 800; margin: 0.1rem 0; line-height: 1; }
.kpi-delta { font-size: 0.72rem; color: #9CA3AF; margin: 0; }

.bottom-row {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 1rem;
  align-items: start;
}

.side-col { display: flex; flex-direction: column; gap: 1rem; }

.card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.1rem 1.25rem 0;
}

.card-title { font-size: 0.9rem; font-weight: 700; color: #111827; margin: 0; }
.card-sub { font-size: 0.75rem; color: #9CA3AF; margin: 0.2rem 0 0; }
.card-link { font-size: 0.8rem; color: #2E75B6; text-decoration: none; font-weight: 500; }
.card-link:hover { text-decoration: underline; }

.data-table { width: 100%; border-collapse: collapse; margin-top: 0.75rem; }

.data-table th {
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: #9CA3AF;
  padding: 0.6rem 1rem;
  text-align: left;
  background: #F9FAFB;
  border-top: 1px solid #F3F4F6;
  border-bottom: 1px solid #F3F4F6;
}

.data-table td {
  padding: 0.8rem 1rem;
  border-bottom: 1px solid #F3F4F6;
  font-size: 0.83rem;
  color: #374151;
  vertical-align: middle;
}

.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: #FAFAFA; }

.priority-cell { display: flex; align-items: center; gap: 0.45rem; }
.priority-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.priority-label { font-size: 0.78rem; font-weight: 600; }

.td-main { font-weight: 600; color: #111827; margin: 0; font-size: 0.83rem; }
.td-sub { font-size: 0.7rem; color: #9CA3AF; margin: 0.1rem 0 0; }
.td-muted { color: #9CA3AF; font-size: 0.8rem; }

.action-btn {
  font-size: 0.78rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  background: #2E75B6;
  color: white;
  border-radius: 5px;
  text-decoration: none;
  transition: background 0.15s;
  white-space: nowrap;
}
.action-btn:hover { background: #1E4D7B; }

.quarantine-list { list-style: none; margin: 0.75rem 0 0; padding: 0; }

.quarantine-item {
  padding: 0.75rem 1.25rem;
  border-bottom: 1px solid #F3F4F6;
}

.quarantine-item:last-child { border-bottom: none; }

.q-filename { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; margin-bottom: 0.2rem; }
.q-name { font-size: 0.82rem; font-weight: 600; color: #111827; }

.q-risk {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  flex-shrink: 0;
}

.q-album { font-size: 0.75rem; color: #6B7280; margin: 0 0 0.15rem; }
.q-reason { font-size: 0.72rem; color: #EF4444; margin: 0; }

.activity-list { list-style: none; margin: 0; padding: 0.75rem 1.25rem; display: flex; flex-direction: column; gap: 0.85rem; }

.activity-item { display: flex; gap: 0.7rem; align-items: flex-start; }

.activity-icon {
  width: 28px; height: 28px;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  flex-shrink: 0;
}

.activity-msg { font-size: 0.78rem; color: #374151; margin: 0; line-height: 1.4; }
.activity-time { font-size: 0.7rem; color: #9CA3AF; margin: 0.15rem 0 0; }

@media (max-width: 1100px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 900px) {
  .bottom-row { grid-template-columns: 1fr; }
}
</style>
