<script setup lang="ts">
import { ref, computed } from 'vue'

type Priority = 'urgent' | 'media' | 'normal'

interface RequestItem {
  id: string; title: string; description: string
  userInitials: string; userName: string; userEmail: string
  privacy: string; date: string; time: string
  priority: Priority; selected: boolean
}

const priorityMap: Record<Priority, { label: string; color: string }> = {
  urgent: { label: 'Urgente', color: '#EF4444' },
  media:  { label: 'Media',   color: '#F59E0B' },
  normal: { label: 'Normal',  color: '#9CA3AF' },
}

const requests = ref<RequestItem[]>([
  { id: 'REQ-045', title: 'Paisajes de los Andes',        description: 'Fotografías de la cordillera andina ecuatoriana. Nevados, valles y paisajes de altura.', userInitials: 'JM', userName: 'Jorge Morales',  userEmail: 'j.morales@email.com', privacy: 'Público', date: '08/05/2026 10:30', time: 'hace 2d',  priority: 'urgent', selected: false },
  { id: 'REQ-044', title: 'Naturaleza en Cotacachi',      description: 'Laguna de Cuicocha, flora andina y cielos despejados del norte de Ecuador.',              userInitials: 'AV', userName: 'Ana Vázquez',   userEmail: 'a.vazquez@email.com', privacy: 'Privado', date: '08/05/2026 09:15', time: 'hace 1d',  priority: 'urgent', selected: false },
  { id: 'REQ-043', title: 'Ciudad de Guayaquil',          description: 'Vistas del Malecón 2000 y el barrio Las Peñas al atardecer.',                             userInitials: 'CR', userName: 'Carlos Reyes',  userEmail: 'c.reyes@email.com',   privacy: 'Público', date: '08/05/2026 16:20', time: 'hace 18h', priority: 'media',  selected: false },
  { id: 'REQ-042', title: 'Mercado Artesanal Otavalo',    description: 'Colores, texturas y cultura del mercado indígena más grande de Sudamérica.',              userInitials: 'LP', userName: 'Lucía Paz',     userEmail: 'l.paz@email.com',     privacy: 'Público', date: '08/05/2026 08:00', time: 'hace 14h', priority: 'media',  selected: false },
  { id: 'REQ-041', title: 'ESPE Campus Universitario',   description: 'Vida universitaria e infraestructura del campus de la Universidad ESPE.',                  userInitials: 'ME', userName: 'Marcos Escobar',userEmail: 'm.escobar@email.com', privacy: 'Privado', date: '08/05/2026 11:45', time: 'hace 8h',  priority: 'normal', selected: false },
])

const searchQuery = ref('')
const selected = ref<RequestItem | null>(null)

const filteredRequests = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return requests.value
  return requests.value.filter(r =>
    r.title.toLowerCase().includes(q) ||
    r.userName.toLowerCase().includes(q) ||
    r.id.toLowerCase().includes(q)
  )
})

const selectedCount = computed(() => requests.value.filter(r => r.selected).length)
const allSelected   = computed(() => requests.value.length > 0 && requests.value.every(r => r.selected))

function toggleAll() {
  const val = !allSelected.value
  requests.value.forEach(r => r.selected = val)
}

function selectRow(req: RequestItem) {
  selected.value = selected.value?.id === req.id ? null : req
}

function approve(id: string) {
  requests.value = requests.value.filter(r => r.id !== id)
  if (selected.value?.id === id) selected.value = null
}

function reject(id: string) {
  requests.value = requests.value.filter(r => r.id !== id)
  if (selected.value?.id === id) selected.value = null
}

function clearSelection() {
  requests.value.forEach(r => r.selected = false)
}
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="workflow-tag">WORKFLOW</div>
        <h2 class="page-title">Solicitudes de Álbumes Pendientes</h2>
      </div>
      <div class="refresh-tag">
        <span class="refresh-dot"></span>
        Auto-refresh: 30s · Última: hace 12s
      </div>
    </div>
    <div class="mini-kpis">
      <div class="mini-kpi">
        <p class="mk-label">PENDIENTES</p>
        <p class="mk-value mk-value--warn">{{ requests.length }}</p>
        <p class="mk-delta">+1 hoy</p>
      </div>
      <div class="mini-kpi">
        <p class="mk-label">URGENTES</p>
        <p class="mk-value mk-value--danger">{{ requests.filter(r => r.priority === 'urgent').length }}</p>
        <p class="mk-delta">requieren acción</p>
      </div>
      <div class="mini-kpi">
        <p class="mk-label">TIEMPO PROM.</p>
        <p class="mk-value">4h</p>
        <p class="mk-delta">meta: 24h</p>
      </div>
      <div class="mini-kpi">
        <p class="mk-label">APROBADAS HOY</p>
        <p class="mk-value mk-value--ok">2</p>
        <p class="mk-delta">vs 1 ayer</p>
      </div>
    </div>

    <div class="toolbar">
      <div class="search-wrap">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
          <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input v-model="searchQuery" type="text" class="search-input" placeholder="Buscar por título, usuario o ID..." />
      </div>
      <span class="result-count">{{ filteredRequests.length }} solicitudes</span>
    </div>

    <Transition name="bulk-slide">
      <div v-if="selectedCount > 0" class="bulk-bar">
        <span class="bulk-count">{{ selectedCount }} solicitud{{ selectedCount > 1 ? 'es' : '' }} seleccionada{{ selectedCount > 1 ? 's' : '' }}</span>
        <span class="bulk-sep">·</span>
        <button class="bulk-action bulk-action--approve" @click="requests.filter(r=>r.selected).forEach(r=>approve(r.id))">
          Aprobar seleccionadas
        </button>
        <span class="bulk-sep">·</span>
        <button class="bulk-action bulk-action--reject" @click="requests.filter(r=>r.selected).forEach(r=>reject(r.id))">
          Rechazar seleccionadas
        </button>
        <button class="bulk-clear" @click="clearSelection">Limpiar selección</button>
      </div>
    </Transition>

    <div class="content-area" :class="{ 'content-area--split': selected }">

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th class="th-check">
                <input type="checkbox" :checked="allSelected" @change="toggleAll" class="checkbox" />
              </th>
              <th>PRIORIDAD</th>
              <th>ÁLBUM / ID</th>
              <th>USUARIO</th>
              <th>PRIVACIDAD</th>
              <th>FECHA</th>
              <th>ESPERA</th>
              <th>ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="req in filteredRequests"
              :key="req.id"
              class="table-row"
              :class="{ 'table-row--selected': selected?.id === req.id, 'table-row--checked': req.selected }"
              @click="selectRow(req)"
            >
              <td class="td-check" @click.stop>
                <input type="checkbox" v-model="req.selected" class="checkbox" />
              </td>
              <td>
                <div class="priority-cell">
                  <span class="priority-dot" :style="{ background: priorityMap[req.priority].color }"></span>
                  <span :style="{ color: priorityMap[req.priority].color, fontWeight: 600, fontSize: '0.78rem' }">
                    {{ priorityMap[req.priority].label }}
                  </span>
                </div>
              </td>
              <td>
                <p class="td-main">{{ req.title }}</p>
                <p class="td-sub">{{ req.id }}</p>
              </td>
              <td>
                <div class="user-cell">
                  <div class="user-avatar-sm">{{ req.userInitials }}</div>
                  <span class="td-muted">{{ req.userName }}</span>
                </div>
              </td>
              <td>
                <span class="privacy-badge" :class="req.privacy === 'Público' ? 'privacy--pub' : 'privacy--priv'">
                  {{ req.privacy }}
                </span>
              </td>
              <td class="td-muted">{{ req.date }}</td>
              <td class="td-muted">{{ req.time }}</td>
              <td @click.stop>
                <div class="row-actions">
                  <button class="btn-approve" @click="approve(req.id)">Aprobar</button>
                  <button class="btn-reject"  @click="reject(req.id)">Rechazar</button>
                </div>
              </td>
            </tr>

            <tr v-if="filteredRequests.length === 0">
              <td colspan="8" class="empty-cell">
                <p style="font-weight:600;color:#374151;margin:0 0 0.25rem">No hay solicitudes pendientes</p>
                <p style="font-size:0.8rem;color:#9CA3AF;margin:0">Todas las solicitudes han sido procesadas</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <aside v-if="selected" class="preview-panel">
        <div class="preview-header">
          <p class="preview-tag">QUICK PREVIEW</p>
          <button class="preview-close" @click="selected = null">✕</button>
        </div>

        <div class="preview-body">
          <div class="preview-top">
            <div class="priority-cell">
              <span class="priority-dot" :style="{ background: priorityMap[selected.priority].color }"></span>
              <span :style="{ color: priorityMap[selected.priority].color, fontWeight:700, fontSize:'0.8rem' }">
                {{ priorityMap[selected.priority].label }}
              </span>
            </div>
            <span class="preview-id">{{ selected.id }}</span>
          </div>

          <h3 class="preview-title">{{ selected.title }}</h3>
          <p class="preview-desc">{{ selected.description }}</p>

          <div class="preview-meta">
            <div class="meta-row">
              <span class="meta-label">Usuario</span>
              <div class="user-cell">
                <div class="user-avatar-sm">{{ selected.userInitials }}</div>
                <div>
                  <p class="meta-value" style="margin:0">{{ selected.userName }}</p>
                  <p class="meta-sub">{{ selected.userEmail }}</p>
                </div>
              </div>
            </div>
            <div class="meta-row">
              <span class="meta-label">Fecha solicitud</span>
              <span class="meta-value">{{ selected.date }}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Privacidad</span>
              <span class="privacy-badge" :class="selected.privacy === 'Público' ? 'privacy--pub' : 'privacy--priv'">
                {{ selected.privacy }}
              </span>
            </div>
            <div class="meta-row">
              <span class="meta-label">En cola</span>
              <span class="meta-value">{{ selected.time }}</span>
            </div>
          </div>
        </div>

        <div class="preview-actions">
          <button class="pa-btn pa-btn--approve" @click="approve(selected.id)">
            Aprobar álbum →
          </button>
          <button class="pa-btn pa-btn--reject" @click="reject(selected.id)">
            Rechazar
          </button>
        </div>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.page { display: flex; flex-direction: column; gap: 1.1rem; }

.page-header { display: flex; align-items: flex-start; justify-content: space-between; }

.workflow-tag {
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #F59E0B;
  text-transform: uppercase;
  margin-bottom: 0.25rem;
}

.page-title { font-size: 1.4rem; font-weight: 800; color: #111827; margin: 0; }

.refresh-tag {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.72rem;
  color: #9CA3AF;
  font-weight: 500;
  white-space: nowrap;
  padding-top: 0.2rem;
}

.refresh-dot {
  width: 7px; height: 7px;
  background: #10B981;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

.mini-kpis {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.mini-kpi {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  padding: 1rem 1.25rem;
}

.mk-label { font-size: 0.62rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #9CA3AF; margin: 0 0 0.25rem; }
.mk-value { font-size: 1.5rem; font-weight: 800; color: #111827; margin: 0 0 0.1rem; line-height: 1; }
.mk-value--warn   { color: #F59E0B; }
.mk-value--danger { color: #EF4444; }
.mk-value--ok     { color: #10B981; }
.mk-delta { font-size: 0.7rem; color: #9CA3AF; margin: 0; }

.toolbar { display: flex; align-items: center; gap: 0.75rem; }

.search-wrap { position: relative; flex: 1; max-width: 420px; }

.search-icon {
  position: absolute;
  left: 0.75rem; top: 50%;
  transform: translateY(-50%);
  width: 16px; height: 16px;
  color: #9CA3AF;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.55rem 0.85rem 0.55rem 2.25rem;
  border: 1.5px solid #E5E7EB;
  border-radius: 7px;
  font-family: inherit;
  font-size: 0.85rem;
  color: #111827;
  background: white;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.15s;
}

.search-input:focus { border-color: #F59E0B; }

.result-count { font-size: 0.78rem; color: #9CA3AF; white-space: nowrap; }

.bulk-bar {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.6rem 1.1rem;
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  border-radius: 8px;
  font-size: 0.82rem;
  flex-wrap: wrap;
}

.bulk-count { font-weight: 600; color: #1E4D7B; }
.bulk-sep { color: #93C5FD; }

.bulk-action {
  background: none;
  border: none;
  font-family: inherit;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
}

.bulk-action--approve { color: #10B981; }
.bulk-action--approve:hover { text-decoration: underline; }
.bulk-action--reject { color: #EF4444; }
.bulk-action--reject:hover { text-decoration: underline; }

.bulk-clear {
  margin-left: auto;
  background: none;
  border: none;
  font-family: inherit;
  font-size: 0.78rem;
  color: #6B7280;
  cursor: pointer;
}
.bulk-clear:hover { color: #374151; }

.bulk-slide-enter-active, .bulk-slide-leave-active { transition: all 0.2s ease; }
.bulk-slide-enter-from, .bulk-slide-leave-to { opacity: 0; transform: translateY(-6px); }

.content-area {
  display: grid;
  grid-template-columns: 1fr;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  overflow: hidden;
  transition: grid-template-columns 0.25s ease;
}

.content-area--split { grid-template-columns: 1fr 340px; }

.table-wrap { overflow-x: auto; }

.data-table { width: 100%; border-collapse: collapse; }

.data-table th {
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: #9CA3AF;
  padding: 0.7rem 0.85rem;
  text-align: left;
  background: #F9FAFB;
  border-bottom: 1px solid #F3F4F6;
  white-space: nowrap;
}

.th-check { width: 40px; }

.data-table td {
  padding: 0.85rem 0.85rem;
  border-bottom: 1px solid #F3F4F6;
  font-size: 0.83rem;
  color: #374151;
  vertical-align: middle;
}

.table-row { cursor: pointer; transition: background 0.1s; }
.table-row:hover td { background: #FAFAFA; }
.table-row--selected td { background: #FFFBEB; }
.table-row--checked td { background: #F0F7FF; }
.data-table tr:last-child td { border-bottom: none; }

.td-check { width: 40px; }

.checkbox { width: 15px; height: 15px; accent-color: #F59E0B; cursor: pointer; }

.priority-cell { display: flex; align-items: center; gap: 0.45rem; }
.priority-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }

.td-main { font-weight: 600; color: #111827; margin: 0; font-size: 0.83rem; }
.td-sub { font-size: 0.7rem; color: #9CA3AF; margin: 0.1rem 0 0; }
.td-muted { color: #9CA3AF; font-size: 0.8rem; }

.user-cell { display: flex; align-items: center; gap: 0.45rem; }

.user-avatar-sm {
  width: 26px; height: 26px;
  background: linear-gradient(135deg, #F59E0B, #D97706);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.6rem;
  font-weight: 700;
  flex-shrink: 0;
}

.privacy-badge { font-size: 0.72rem; font-weight: 500; padding: 0.2rem 0.5rem; border-radius: 4px; }
.privacy--pub { background: #EFF6FF; color: #2E75B6; }
.privacy--priv { background: #F3F4F6; color: #6B7280; }

.row-actions { display: flex; gap: 0.4rem; }

.btn-approve {
  font-family: inherit; font-size: 0.75rem; font-weight: 600;
  padding: 0.3rem 0.65rem; border-radius: 5px;
  background: #2E75B6; color: white; border: none;
  cursor: pointer; transition: background 0.15s; white-space: nowrap;
}
.btn-approve:hover { background: #1E4D7B; }

.btn-reject {
  font-family: inherit; font-size: 0.75rem; font-weight: 600;
  padding: 0.3rem 0.65rem; border-radius: 5px;
  background: white; color: #EF4444;
  border: 1.5px solid #EF4444;
  cursor: pointer; transition: all 0.15s; white-space: nowrap;
}
.btn-reject:hover { background: #FEF2F2; }

.empty-cell { text-align: center; padding: 3rem 1rem !important; }

.preview-panel {
  border-left: 1px solid #E5E7EB;
  display: flex;
  flex-direction: column;
  background: white;
}

.preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.1rem 0.75rem;
  border-bottom: 1px solid #F3F4F6;
}

.preview-tag { font-size: 0.62rem; font-weight: 700; letter-spacing: 0.1em; color: #9CA3AF; text-transform: uppercase; margin: 0; }

.preview-close {
  background: none; border: none;
  font-size: 0.9rem; color: #9CA3AF;
  cursor: pointer; padding: 0.2rem 0.4rem;
  border-radius: 4px; transition: background 0.15s;
}
.preview-close:hover { background: #F3F4F6; color: #374151; }

.preview-body { flex: 1; padding: 1.1rem; display: flex; flex-direction: column; gap: 0.85rem; overflow-y: auto; }

.preview-top { display: flex; align-items: center; justify-content: space-between; }
.preview-id { font-size: 0.75rem; color: #9CA3AF; font-weight: 500; }

.preview-title { font-size: 1rem; font-weight: 700; color: #111827; margin: 0; line-height: 1.35; }
.preview-desc { font-size: 0.8rem; color: #6B7280; margin: 0; line-height: 1.55; }

.preview-meta { display: flex; flex-direction: column; gap: 0.7rem; padding-top: 0.75rem; border-top: 1px solid #F3F4F6; }

.meta-row { display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; }
.meta-label { font-size: 0.75rem; color: #9CA3AF; font-weight: 500; flex-shrink: 0; }
.meta-value { font-size: 0.82rem; color: #374151; font-weight: 500; }
.meta-sub { font-size: 0.7rem; color: #9CA3AF; margin: 0.1rem 0 0; }

.preview-actions {
  padding: 1rem 1.1rem;
  border-top: 1px solid #F3F4F6;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.pa-btn {
  width: 100%;
  padding: 0.65rem;
  border-radius: 7px;
  font-family: inherit;
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.15s;
}

.pa-btn--approve { background: #2E75B6; color: white; }
.pa-btn--approve:hover { background: #1E4D7B; }
.pa-btn--reject { background: white; color: #EF4444; border: 1.5px solid #EF4444; }
.pa-btn--reject:hover { background: #FEF2F2; }

@media (max-width: 1000px) {
  .content-area--split { grid-template-columns: 1fr; }
  .preview-panel { border-left: none; border-top: 1px solid #E5E7EB; }
  .mini-kpis { grid-template-columns: repeat(2, 1fr); }
}
</style>
