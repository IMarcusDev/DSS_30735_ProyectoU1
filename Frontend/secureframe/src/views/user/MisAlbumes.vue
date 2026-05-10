<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { albumsService } from '../../services/albums'

const albums      = ref([])
const loading     = ref(true)
const activeTab   = ref('all')
const searchQuery = ref('')
const selected    = ref(null)

const stateToKey = { 'Aprobado': 'approved', 'Pendiente': 'pending', 'Negado': 'rejected' }

const statusMap = {
  approved: { label: 'Aprobado',  color: '#10B981', bg: '#ECFDF5' },
  pending:  { label: 'Pendiente', color: '#F59E0B', bg: '#FFFBEB' },
  rejected: { label: 'Rechazado', color: '#EF4444', bg: '#FEF2F2' },
}

const tabs = [
  { key: 'all',      label: 'Todos' },
  { key: 'approved', label: 'Aprobados' },
  { key: 'pending',  label: 'Pendientes' },
  { key: 'rejected', label: 'Rechazados' },
]

onMounted(async () => {
  try {
    const data = await albumsService.getMine()
    albums.value = data.map(a => ({
      id:          a.id,
      title:       a.name,
      description: a.description,
      privacy:     a.is_public ? 'Público' : 'Privado',
      images:      a.image_count ?? 0,
      quarantined: 0,
      status:      stateToKey[a.state] ?? 'pending',
      date:        new Date(a.date_created).toLocaleDateString('es-EC'),
    }))
  } catch {
    albums.value = []
  } finally {
    loading.value = false
  }
})

const filteredAlbums = computed(() => {
  let list = albums.value
  if (activeTab.value !== 'all') list = list.filter(a => a.status === activeTab.value)
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(a => a.title.toLowerCase().includes(q) || a.id.toLowerCase().includes(q))
  }
  return list
})

function tabCount(key) {
  if (key === 'all') return albums.value.length
  return albums.value.filter(a => a.status === key).length
}

function selectRow(album) {
  selected.value = selected.value?.id === album.id ? null : album
}

function closePreview() { selected.value = null }
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <h2 class="page-title">Mis Álbumes</h2>
        <p class="page-sub">Administra tus álbumes y solicita nuevos</p>
      </div>
      <RouterLink to="/user/albums/new" class="btn-primary">
        <span class="btn-icon">+</span> Solicitar álbum
      </RouterLink>
    </div>

    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="tab"
        :class="{ 'tab--active': activeTab === tab.key }"
        @click="activeTab = tab.key; selected = null"
      >
        {{ tab.label }}
        <span class="tab-count" :class="{ 'tab-count--active': activeTab === tab.key }">
          {{ tabCount(tab.key) }}
        </span>
      </button>
    </div>

    <div class="toolbar">
      <div class="search-wrap">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
          <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="Buscar por nombre o ID..."
        />
      </div>
    </div>

    <div class="content-area" :class="{ 'content-area--split': selected }">

      <!-- Table -->
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>ÁLBUM</th>
              <th>PRIVACIDAD</th>
              <th>IMÁGENES</th>
              <th>CUARENTENA</th>
              <th>FECHA</th>
              <th>ESTADO</th>
              <th>ACCIONES</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="album in filteredAlbums"
              :key="album.id"
              class="table-row"
              :class="{ 'table-row--selected': selected?.id === album.id }"
              @click="selectRow(album)"
            >
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
              <td @click.stop>
                <div class="row-actions">
                  <RouterLink :to="`/user/albums/${album.id}`" class="action-link">Ver</RouterLink>
                  <RouterLink
                    v-if="album.status === 'approved'"
                    to="/user/upload"
                    class="action-btn"
                  >Subir</RouterLink>
                </div>
              </td>
            </tr>

            <tr v-if="filteredAlbums.length === 0">
              <td colspan="7" class="empty-cell">
                <p class="empty-title">No se encontraron álbumes</p>
                <p class="empty-sub">Intenta cambiar los filtros o solicita uno nuevo</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <aside v-if="selected" class="preview-panel">
        <div class="preview-header">
          <p class="preview-tag">VISTA RÁPIDA</p>
          <button class="preview-close" @click="closePreview" aria-label="Cerrar">✕</button>
        </div>

        <div class="preview-body">
          <div class="preview-status-row">
            <span class="status-badge" :style="{ color: statusMap[selected.status].color, background: statusMap[selected.status].bg }">
              <span class="status-dot" :style="{ background: statusMap[selected.status].color }"></span>
              {{ statusMap[selected.status].label }}
            </span>
            <span class="preview-id">{{ selected.id }}</span>
          </div>

          <h3 class="preview-title">{{ selected.title }}</h3>
          <p class="preview-desc">{{ selected.description }}</p>

          <div class="preview-meta">
            <div class="meta-item">
              <span class="meta-label">Privacidad</span>
              <span class="meta-value">
                <span class="privacy-badge" :class="selected.privacy === 'Público' ? 'privacy-badge--pub' : 'privacy-badge--priv'">
                  {{ selected.privacy }}
                </span>
              </span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Fecha de solicitud</span>
              <span class="meta-value">{{ selected.date }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Imágenes subidas</span>
              <span class="meta-value meta-value--strong">{{ selected.images }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">En cuarentena</span>
              <span class="meta-value" :style="selected.quarantined > 0 ? { color: '#EF4444', fontWeight: 700 } : {}">
                {{ selected.quarantined || '—' }}
              </span>
            </div>
          </div>
        </div>

        <div class="preview-actions">
          <RouterLink :to="`/user/albums/${selected.id}`" class="preview-btn preview-btn--primary">
            Ver álbum →
          </RouterLink>
          <RouterLink
            v-if="selected.status === 'approved'"
            to="/user/upload"
            class="preview-btn preview-btn--outline"
          >
            Subir imagen
          </RouterLink>
          <button
            v-if="selected.quarantined > 0"
            class="preview-btn preview-btn--warn"
            disabled
          >
            Ver cuarentena
          </button>
        </div>
      </aside>

    </div>
  </div>
</template>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.page-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: #111827;
  margin: 0;
}

.page-sub {
  font-size: 0.82rem;
  color: #6B7280;
  margin: 0.2rem 0 0;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: #2E75B6;
  color: white;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.55rem 1.1rem;
  border-radius: 7px;
  text-decoration: none;
  white-space: nowrap;
  transition: background 0.15s;
}

.btn-primary:hover { background: #1E4D7B; }
.btn-icon { font-size: 1rem; line-height: 1; }

.tabs {
  display: flex;
  gap: 0.25rem;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 9px;
  padding: 0.3rem;
  width: fit-content;
}

.tab {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.9rem;
  border-radius: 6px;
  border: none;
  background: none;
  font-family: inherit;
  font-size: 0.82rem;
  font-weight: 500;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.15s;
}

.tab:hover { color: #374151; background: #F9FAFB; }

.tab--active {
  background: #2E75B6;
  color: white;
  font-weight: 600;
}

.tab-count {
  background: #F3F4F6;
  color: #6B7280;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.05rem 0.45rem;
  border-radius: 99px;
}

.tab-count--active {
  background: rgba(255,255,255,0.25);
  color: white;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.search-wrap {
  position: relative;
  flex: 1;
  max-width: 380px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
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

.search-input:focus { border-color: #2E75B6; }

.content-area {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  transition: grid-template-columns 0.25s ease;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  overflow: hidden;
}

.content-area--split {
  grid-template-columns: 1fr 340px;
}

.table-wrap { overflow-x: auto; }

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  font-size: 0.67rem;
  font-weight: 600;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: #9CA3AF;
  padding: 0.7rem 1rem;
  text-align: left;
  background: #F9FAFB;
  border-bottom: 1px solid #F3F4F6;
  white-space: nowrap;
}

.data-table td {
  padding: 0.9rem 1rem;
  border-bottom: 1px solid #F3F4F6;
  font-size: 0.84rem;
  color: #374151;
  vertical-align: middle;
}

.table-row { cursor: pointer; transition: background 0.1s; }
.table-row:hover td { background: #F9FAFB; }
.table-row--selected td { background: #EFF6FF; }
.data-table tr:last-child td { border-bottom: none; }

.td-main {
  font-weight: 600;
  color: #111827;
  margin: 0;
  font-size: 0.85rem;
}

.td-sub {
  font-size: 0.72rem;
  color: #9CA3AF;
  margin: 0.1rem 0 0;
}

.td-center { text-align: center; }
.td-muted { color: #9CA3AF; font-size: 0.82rem; }

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.25rem 0.65rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }

.privacy-badge {
  font-size: 0.72rem;
  font-weight: 500;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}
.privacy-badge--pub { background: #EFF6FF; color: #2E75B6; }
.privacy-badge--priv { background: #F3F4F6; color: #6B7280; }

.quarantine-count {
  background: #FEF2F2;
  color: #EF4444;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

.row-actions { display: flex; gap: 0.4rem; align-items: center; }

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

.empty-cell { text-align: center; padding: 3rem 1rem !important; }
.empty-title { font-weight: 600; color: #374151; margin: 0 0 0.3rem; }
.empty-sub { font-size: 0.82rem; color: #9CA3AF; margin: 0; }

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
  padding: 1rem 1.25rem 0.75rem;
  border-bottom: 1px solid #F3F4F6;
}

.preview-tag {
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #9CA3AF;
  text-transform: uppercase;
  margin: 0;
}

.preview-close {
  background: none;
  border: none;
  font-size: 0.9rem;
  color: #9CA3AF;
  cursor: pointer;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  transition: background 0.15s, color 0.15s;
}
.preview-close:hover { background: #F3F4F6; color: #374151; }

.preview-body {
  flex: 1;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.preview-status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.preview-id {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
}

.preview-title {
  font-size: 1rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
  line-height: 1.35;
}

.preview-desc {
  font-size: 0.8rem;
  color: #6B7280;
  margin: 0;
  line-height: 1.55;
}

.preview-meta {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  padding-top: 0.75rem;
  border-top: 1px solid #F3F4F6;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.meta-label {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
}

.meta-value {
  font-size: 0.82rem;
  color: #374151;
  font-weight: 500;
}

.meta-value--strong { font-weight: 700; color: #111827; }

.preview-actions {
  padding: 1rem 1.25rem;
  border-top: 1px solid #F3F4F6;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.preview-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.6rem 1rem;
  border-radius: 7px;
  font-family: inherit;
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.15s;
}

.preview-btn--primary { background: #2E75B6; color: white; }
.preview-btn--primary:hover { background: #1E4D7B; }

.preview-btn--outline { background: white; color: #2E75B6; border: 1.5px solid #2E75B6; }
.preview-btn--outline:hover { background: #EFF6FF; }

.preview-btn--warn { background: #FEF2F2; color: #EF4444; border: 1px solid #FECACA; opacity: 0.8; cursor: not-allowed; }

@media (max-width: 900px) {
  .content-area--split { grid-template-columns: 1fr; }
  .preview-panel { border-left: none; border-top: 1px solid #E5E7EB; }
}

@media (max-width: 600px) {
  .page-header { flex-direction: column; align-items: flex-start; }
  .tabs { flex-wrap: wrap; }
}
</style>
