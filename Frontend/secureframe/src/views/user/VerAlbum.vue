<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { albumsService, type Album } from '../../services/albums'
import { imagesService, type GalleryImage } from '../../services/images'
import { timeAgo } from '../../utils/time'

const route = useRoute()
const albumId = route.params.id as string

const album  = ref<Album | null>(null)
const images = ref<GalleryImage[]>([])
const loading = ref(true)
const error   = ref('')

const stateMap: Record<string, { label: string; color: string; bg: string }> = {
  Limpio:     { label: 'Limpio',      color: '#059669', bg: 'rgba(5,150,105,0.12)'  },
  Sospechoso: { label: 'Cuarentena',  color: '#D97706', bg: 'rgba(217,119,6,0.18)'  },
  Positivo:   { label: 'Positivo',    color: '#DC2626', bg: 'rgba(220,38,38,0.15)'  },
}

onMounted(async () => {
  try {
    const [albumData, imagesData] = await Promise.all([
      albumsService.getById(albumId),
      imagesService.getByAlbum(albumId),
    ])
    album.value  = albumData
    images.value = imagesData
  } catch {
    error.value = 'No se pudo cargar el álbum.'
  } finally {
    loading.value = false
  }
})

const cleanCount      = computed(() => images.value.filter(i => i.image_state === 'Limpio').length)
const quarantineCount = computed(() => images.value.filter(i => i.image_state !== 'Limpio').length)

const selected = ref<GalleryImage | null>(null)
</script>

<template>
  <div class="page">
    <!-- Breadcrumb -->
    <nav class="breadcrumb">
      <RouterLink to="/user/albums" class="bc-link">Mis Álbumes</RouterLink>
      <span class="bc-sep">/</span>
      <span class="bc-current">{{ album?.name ?? 'Cargando…' }}</span>
    </nav>

    <div v-if="loading" class="loading-state">
      <div class="spinner-lg"></div>
      <p>Cargando álbum…</p>
    </div>

    <div v-else-if="error" class="alert-error">{{ error }}</div>

    <template v-else-if="album">
      <div class="album-header">
        <div class="album-info">
          <div class="album-meta-row">
            <span class="privacy-badge" :class="album.is_public ? 'privacy--pub' : 'privacy--priv'">
              {{ album.is_public ? 'Público' : 'Privado' }}
            </span>
            <span class="state-badge" :class="`state--${album.state.toLowerCase()}`">
              {{ album.state }}
            </span>
          </div>
          <h1 class="album-title">{{ album.name }}</h1>
          <p v-if="album.description" class="album-desc">{{ album.description }}</p>
        </div>

        <div class="album-stats">
          <div class="stat">
            <span class="stat-val">{{ images.length }}</span>
            <span class="stat-lbl">Total</span>
          </div>
          <div class="stat">
            <span class="stat-val stat-val--green">{{ cleanCount }}</span>
            <span class="stat-lbl">Limpias</span>
          </div>
          <div class="stat" v-if="quarantineCount > 0">
            <span class="stat-val stat-val--amber">{{ quarantineCount }}</span>
            <span class="stat-lbl">Cuarentena</span>
          </div>
          <RouterLink
            v-if="album.state === 'Aprobado'"
            to="/user/upload"
            class="btn-upload"
          >
            + Subir imagen
          </RouterLink>
        </div>
      </div>
      <div v-if="images.length === 0" class="empty-state">
        <div class="empty-icon">🖼</div>
        <h3 class="empty-title">Este álbum aún no tiene imágenes</h3>
        <p class="empty-sub">Sube tu primera imagen para empezar.</p>
        <RouterLink v-if="album.state === 'Aprobado'" to="/user/upload" class="btn-upload-lg">
          + Subir imagen
        </RouterLink>
      </div>

      <div v-else class="image-grid">
        <div
          v-for="img in images"
          :key="img.image_id"
          class="img-card"
          @click="selected = selected?.image_id === img.image_id ? null : img"
          :class="{ 'img-card--selected': selected?.image_id === img.image_id }"
        >
          <div class="img-thumb">
            <img :src="img.image_path" :alt="img.image_name" class="thumb" loading="lazy" />

            <div
              v-if="img.image_state !== 'Limpio'"
              class="state-overlay"
              :style="{ background: stateMap[img.image_state]?.bg, color: stateMap[img.image_state]?.color }"
            >
              {{ stateMap[img.image_state]?.label }}
            </div>
          </div>

          <div class="img-footer">
            <p class="img-name">{{ img.image_name }}</p>
            <p class="img-date">{{ timeAgo(img.image_date_uploaded) }}</p>
          </div>
        </div>
      </div>

      <div v-if="selected" class="lightbox" @click.self="selected = null">
        <div class="lightbox-inner">
          <button class="lb-close" @click="selected = null">✕</button>
          <img :src="selected.image_path" :alt="selected.image_name" class="lb-img" />
          <div class="lb-meta">
            <p class="lb-name">{{ selected.image_name }}</p>
            <div class="lb-chips">
              <span
                class="lb-state"
                :style="{ color: stateMap[selected.image_state]?.color, background: stateMap[selected.image_state]?.bg }"
              >
                {{ stateMap[selected.image_state]?.label ?? selected.image_state }}
              </span>
              <span class="lb-mime">{{ selected.image_mimetype }}</span>
            </div>
            <p class="lb-date">Subida {{ timeAgo(selected.image_date_uploaded) }}</p>
            <p v-if="selected.image_state !== 'Limpio'" class="lb-warn">
              Esta imagen está en cuarentena. Un supervisor revisará si es segura.
            </p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.page { display: flex; flex-direction: column; gap: 1.25rem; font-family: 'Inter', system-ui, sans-serif; }

.breadcrumb { display: flex; align-items: center; gap: 0.5rem; font-size: 0.82rem; }
.bc-link { color: #2E75B6; text-decoration: none; font-weight: 500; }
.bc-link:hover { text-decoration: underline; }
.bc-sep { color: #D1D5DB; }
.bc-current { color: #6B7280; }

.loading-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 4rem; color: #9CA3AF; }
.spinner-lg {
  width: 36px; height: 36px;
  border: 3px solid #E5E7EB;
  border-top-color: #2E75B6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.alert-error { background: #FEF2F2; border: 1px solid #FECACA; color: #B91C1C; padding: 0.9rem 1.1rem; border-radius: 8px; font-size: 0.85rem; }

.album-header {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  padding: 1.5rem 1.75rem;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.album-meta-row { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; }

.privacy-badge, .state-badge {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.2rem 0.6rem;
  border-radius: 99px;
}

.privacy--pub  { background: #EFF6FF; color: #2E75B6; }
.privacy--priv { background: #F3F4F6; color: #6B7280; }

.state--aprobado  { background: #ECFDF5; color: #059669; }
.state--pendiente { background: #FFFBEB; color: #D97706; }
.state--negado    { background: #FEF2F2; color: #DC2626; }

.album-title { font-size: 1.4rem; font-weight: 800; color: #111827; margin: 0 0 0.3rem; }
.album-desc  { font-size: 0.85rem; color: #6B7280; margin: 0; line-height: 1.6; max-width: 600px; }

.album-stats { display: flex; align-items: center; gap: 1.5rem; flex-shrink: 0; }

.stat { display: flex; flex-direction: column; align-items: center; }
.stat-val { font-size: 1.5rem; font-weight: 800; color: #111827; line-height: 1; }
.stat-val--green { color: #059669; }
.stat-val--amber { color: #D97706; }
.stat-lbl { font-size: 0.68rem; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }

.btn-upload {
  display: inline-flex;
  align-items: center;
  padding: 0.55rem 1.1rem;
  background: #2E75B6;
  color: white;
  border-radius: 7px;
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.15s;
  white-space: nowrap;
}
.btn-upload:hover { background: #1E4D7B; }

.empty-state {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  padding: 5rem 2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}
.empty-icon  { font-size: 2.5rem; }
.empty-title { font-size: 1rem; font-weight: 700; color: #374151; margin: 0; }
.empty-sub   { font-size: 0.82rem; color: #9CA3AF; margin: 0; }
.btn-upload-lg {
  margin-top: 0.5rem;
  padding: 0.65rem 1.5rem;
  background: #2E75B6;
  color: white;
  border-radius: 7px;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
}
.btn-upload-lg:hover { background: #1E4D7B; }

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.img-card {
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.img-card:hover { border-color: #2E75B6; box-shadow: 0 4px 14px rgba(46,117,182,0.12); }
.img-card--selected { border-color: #2E75B6; box-shadow: 0 0 0 3px rgba(46,117,182,0.2); }

.img-thumb { position: relative; height: 160px; overflow: hidden; background: #F3F4F6; }

.thumb { width: 100%; height: 100%; object-fit: cover; display: block; }

.state-overlay {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 0.35rem 0.6rem;
  font-size: 0.68rem;
  font-weight: 700;
  text-align: center;
}

.img-footer { padding: 0.6rem 0.75rem; }
.img-name { font-size: 0.78rem; font-weight: 600; color: #111827; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.img-date { font-size: 0.7rem; color: #9CA3AF; margin: 0.1rem 0 0; }

.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.75);
  z-index: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.lightbox-inner {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  max-width: 680px;
  width: 100%;
  position: relative;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.lb-close {
  position: absolute;
  top: 0.75rem; right: 0.75rem;
  background: rgba(0,0,0,0.55);
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px; height: 30px;
  font-size: 0.85rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.lb-img {
  width: 100%;
  max-height: 55vh;
  object-fit: contain;
  background: #111;
  display: block;
}

.lb-meta { padding: 1rem 1.25rem; }
.lb-name { font-size: 0.95rem; font-weight: 700; color: #111827; margin: 0 0 0.5rem; word-break: break-all; }
.lb-chips { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.4rem; }
.lb-state { font-size: 0.72rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 99px; }
.lb-mime  { font-size: 0.72rem; background: #F3F4F6; color: #6B7280; padding: 0.2rem 0.6rem; border-radius: 4px; font-family: monospace; }
.lb-date  { font-size: 0.75rem; color: #9CA3AF; margin: 0 0 0.4rem; }
.lb-warn  { font-size: 0.78rem; color: #B45309; background: #FFFBEB; border: 1px solid #FDE68A; padding: 0.5rem 0.75rem; border-radius: 6px; margin: 0; }

@media (max-width: 768px) {
  .album-header { flex-direction: column; }
  .album-stats  { flex-wrap: wrap; gap: 1rem; }
  .image-grid   { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); }
}
</style>
