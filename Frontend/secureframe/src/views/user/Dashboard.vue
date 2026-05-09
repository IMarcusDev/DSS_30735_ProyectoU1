<script setup>
import { RouterLink } from 'vue-router'

const kpis = [
  { label: 'Álbumes aprobados', value: 2, delta: '+1 este mes', color: '#10B981', bg: '#ECFDF5', icon: '✓' },
  { label: 'Pendientes revisión', value: 1, delta: 'Enviado hace 2d',  color: '#F59E0B', bg: '#FFFBEB', icon: '⏳' },
  { label: 'Imágenes subidas',  value: 20, delta: '+5 esta semana',    color: '#2E75B6', bg: '#EFF6FF', icon: '🖼' },
  { label: 'En cuarentena',     value: 2,  delta: 'Requieren revisión',color: '#EF4444', bg: '#FEF2F2', icon: '🛡' },
]

const recentAlbums = [
  { id: 'ALB-001', title: 'Proyecto ESPE 2025',        privacy: 'Privado', images: 12, quarantined: 1, status: 'approved', date: '01/05/2026' },
  { id: 'ALB-002', title: 'Arquitectura Histórica Quito', privacy: 'Público', images: 8, quarantined: 1, status: 'approved', date: '03/05/2026' },
  { id: 'ALB-003', title: 'Laboratorio DSS 2026',      privacy: 'Privado', images: 0, quarantined: 0, status: 'pending',  date: '07/05/2026' },
]

const statusMap = {
  approved: { label: 'Aprobado',  color: '#10B981', bg: '#ECFDF5' },
  pending:  { label: 'Pendiente', color: '#F59E0B', bg: '#FFFBEB' },
  rejected: { label: 'Rechazado', color: '#EF4444', bg: '#FEF2F2' },
}

const activity = [
  { msg: 'Tu álbum "Proyecto ESPE 2025" fue aprobado',         time: 'hace 2 días',  icon: '✓', color: '#10B981' },
  { msg: 'La imagen "foto_lab.jpg" fue marcada como sospechosa', time: 'hace 3 días', icon: '⚠', color: '#F59E0B' },
  { msg: 'Solicitaste el álbum "Laboratorio DSS 2026"',         time: 'hace 7 días',  icon: '⊕', color: '#2E75B6' },
  { msg: 'Subiste 5 imágenes a "Arquitectura Histórica Quito"', time: 'hace 10 días', icon: '↑', color: '#6B7280' },
]
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
          <p class="kpi-value" :style="{ color: kpi.color }">{{ kpi.value }}</p>
          <p class="kpi-delta">{{ kpi.delta }}</p>
        </div>
      </div>
    </div>

    <div class="bottom-row">
      <div class="card card--wide">
        <div class="card-header">
          <div>
            <h3 class="card-title">Mis álbumes recientes</h3>
            <p class="card-sub">Últimas solicitudes y álbumes activos</p>
          </div>
          <RouterLink to="/user/albums/new" class="btn-primary">+ Solicitar álbum</RouterLink>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th>ÁLBUM</th>
              <th>PRIVACIDAD</th>
              <th>IMÁGENES</th>
              <th>CUARENTENA</th>
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
              <td class="td-center">{{ album.images }}</td>
              <td class="td-center">
                <span v-if="album.quarantined > 0" class="quarantine-count">{{ album.quarantined }}</span>
                <span v-else class="td-muted">—</span>
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
                  <RouterLink :to="`/user/albums/${album.id}`" class="action-link">Ver</RouterLink>
                  <RouterLink v-if="album.status === 'approved'" to="/user/upload" class="action-btn">Subir</RouterLink>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="card-footer">
          <RouterLink to="/user/albums" class="footer-link">Ver todos los álbumes →</RouterLink>
        </div>
      </div>

      <div class="card card--narrow">
        <div class="card-header">
          <h3 class="card-title">Actividad reciente</h3>
        </div>
        <ul class="activity-list">
          <li v-for="item in activity" :key="item.msg" class="activity-item">
            <div class="activity-icon" :style="{ color: item.color, background: item.color + '18' }">
              {{ item.icon }}
            </div>
            <div class="activity-body">
              <p class="activity-msg">{{ item.msg }}</p>
              <p class="activity-time">{{ item.time }}</p>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

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

.kpi-card__icon {
  width: 46px;
  height: 46px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.kpi-label {
  font-size: 0.75rem;
  font-weight: 500;
  color: #6B7280;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.kpi-value {
  font-size: 1.75rem;
  font-weight: 800;
  margin: 0.1rem 0;
  line-height: 1;
}

.kpi-delta {
  font-size: 0.72rem;
  color: #9CA3AF;
  margin: 0;
}

.bottom-row {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 1rem;
  align-items: start;
}

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
  padding: 1.25rem 1.25rem 0;
  gap: 1rem;
}

.card-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.card-sub {
  font-size: 0.78rem;
  color: #9CA3AF;
  margin: 0.2rem 0 0;
}

.card-footer {
  padding: 0.85rem 1.25rem;
  border-top: 1px solid #F3F4F6;
}

.footer-link {
  font-size: 0.82rem;
  color: #2E75B6;
  text-decoration: none;
  font-weight: 500;
}

.footer-link:hover { text-decoration: underline; }

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.data-table th {
  font-size: 0.68rem;
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
  padding: 0.85rem 1rem;
  border-bottom: 1px solid #F3F4F6;
  font-size: 0.85rem;
  color: #374151;
  vertical-align: middle;
}

.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: #FAFAFA; }

.td-main {
  font-weight: 600;
  color: #111827;
  margin: 0;
  font-size: 0.85rem;
}

.td-sub {
  font-size: 0.72rem;
  color: #9CA3AF;
  margin: 0.15rem 0 0;
}

.td-center { text-align: center; }
.td-muted { color: #9CA3AF; }

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.25rem 0.65rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.privacy-badge {
  font-size: 0.72rem;
  font-weight: 500;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

.privacy-badge--pub { background: #EFF6FF; color: #2E75B6; }
.privacy-badge--priv { background: #F3F4F6; color: #6B7280; }

.quarantine-count {
  display: inline-block;
  background: #FEF2F2;
  color: #EF4444;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

.row-actions {
  display: flex;
  gap: 0.4rem;
  align-items: center;
}

.action-link {
  font-size: 0.8rem;
  color: #2E75B6;
  text-decoration: none;
  font-weight: 500;
}

.action-link:hover { text-decoration: underline; }

.action-btn {
  font-size: 0.78rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  background: #2E75B6;
  color: white;
  border-radius: 5px;
  text-decoration: none;
  transition: background 0.15s;
}

.action-btn:hover { background: #1E4D7B; }

.btn-primary {
  display: inline-block;
  background: #2E75B6;
  color: white;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 7px;
  text-decoration: none;
  white-space: nowrap;
  transition: background 0.15s;
}

.btn-primary:hover { background: #1E4D7B; }

.activity-list {
  list-style: none;
  margin: 0;
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}

.activity-icon {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.activity-body { flex: 1; }

.activity-msg {
  font-size: 0.8rem;
  color: #374151;
  margin: 0;
  line-height: 1.45;
}

.activity-time {
  font-size: 0.72rem;
  color: #9CA3AF;
  margin: 0.2rem 0 0;
}

@media (max-width: 1100px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 900px) {
  .bottom-row { grid-template-columns: 1fr; }
}

@media (max-width: 600px) {
  .kpi-grid { grid-template-columns: 1fr 1fr; }
}
</style>
