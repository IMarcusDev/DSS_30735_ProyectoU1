<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { albumsService } from '../services/albums'
import { imagesService } from '../services/images'

const route  = useRoute()
const router = useRouter()
const mobileOpen = ref(false)

const { user, fetchMe, logout: authLogout } = useAuth()

const counts = ref({ pending: 0, quarantine: 0 })

onMounted(async () => {
  await fetchMe()
  try {
    const [albums, imgs] = await Promise.all([
      albumsService.getPending(),
      imagesService.getSuspicious(),
    ])
    counts.value = { pending: albums.length, quarantine: imgs.length }
  } catch {}
})

const icons = {
  home:    'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
  inbox:   'M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4',
  check:   'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
  xcirc:   'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
  shield:  'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
  user:    'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
  users:   'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z',
  logout:  'M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1',
  bell:    'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',
  menu:    'M4 6h16M4 12h16M4 18h16',
  chart:   'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
  clock:   'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
}

const navGroups = computed(() => [
  {
    label: 'SOLICITUDES',
    items: [
      { label: 'Álbumes pendientes', to: '/supervisor/solicitudes', icon: 'inbox', badge: counts.value.pending || null },
    ],
  },
  {
    label: 'CUARENTENA',
    items: [
      { label: 'Por revisar', to: '/supervisor/cuarentena', icon: 'shield', badge: counts.value.quarantine || null },
    ],
  },
  {
    label: 'SISTEMA',
    items: [
      { label: 'Dashboard', to: '/supervisor/dashboard', icon: 'chart', badge: null },
      { label: 'Historial', to: '/supervisor/historial', icon: 'clock', badge: null },
    ],
  },
])

const pageTitle = computed(() => {
  const map = {
    SuperDashboard:      'Dashboard',
    SolicitudesAlbumes:  'Solicitudes de Álbumes',
    Cuarentena:          'Bandeja de Cuarentena',
    Historial:           'Historial de Actividad',
  }
  return (map as Record<string, string>)[route.name as string] || 'Panel de Supervisor'
})

function isActive(to: string) {
  return route.path === to.split('?')[0]
}

function logout() {
  authLogout()
  router.push('/login')
}
</script>

<template>
  <div class="shell">
    <div v-if="mobileOpen" class="overlay" @click="mobileOpen = false"></div>

    <aside class="sidebar" :class="{ 'sidebar--open': mobileOpen }">
      <RouterLink to="/" class="sidebar-brand">
        <img src="/logo.png" alt="logo" class="sidebar-logo" />
        <span class="sidebar-brand-name">Secureframe</span>
      </RouterLink>

      <div class="sidebar-role">
        <span class="role-dot"></span>
        Panel de Supervisor
      </div>

      <nav class="sidebar-nav">
        <RouterLink to="/supervisor/dashboard" class="nav-item" :class="{ 'nav-item--active': isActive('/supervisor/dashboard') }">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path :d="icons.home" />
          </svg>
          <span>Inicio</span>
        </RouterLink>

        <div v-for="group in navGroups" :key="group.label" class="nav-group">
          <p class="nav-group-label">{{ group.label }}</p>
          <RouterLink
            v-for="item in group.items"
            :key="item.label"
            :to="item.to"
            class="nav-item"
            :class="{ 'nav-item--active': isActive(item.to) }"
            @click="mobileOpen = false"
          >
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path :d="(icons as Record<string, string>)[item.icon]" />
            </svg>
            <span>{{ item.label }}</span>
            <span v-if="item.badge" class="nav-badge nav-badge--alert">{{ item.badge }}</span>
          </RouterLink>
        </div>
      </nav>

      <button class="sidebar-logout" @click="logout">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path :d="icons.logout" />
        </svg>
        Cerrar sesión
      </button>
    </aside>

    <div class="main">
      <header class="topbar">
        <div class="topbar-left">
          <button class="hamburger" @click="mobileOpen = !mobileOpen">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
              <path :d="icons.menu" />
            </svg>
          </button>
          <div>
            <p class="topbar-sub">PANEL ADMINISTRATIVO</p>
            <h1 class="topbar-title">{{ pageTitle }}</h1>
          </div>
        </div>

        <div class="topbar-right">

          <div class="user-chip">
            <div class="user-avatar">AD</div>
            <div class="user-info">
              <span class="user-name">Administrador</span>
              <span class="user-role">{{ user?.role ?? 'Supervisor' }}</span>
            </div>
          </div>
        </div>
      </header>

      <main class="content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.shell {
  display: flex;
  min-height: 100vh;
  font-family: 'Inter', system-ui, sans-serif;
  background: #F3F4F6;
}

.sidebar {
  width: 240px;
  flex-shrink: 0;
  background: #0A1628;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0; left: 0;
  height: 100vh;
  z-index: 200;
  overflow-y: auto;
  transition: transform 0.25s ease;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 1.25rem 1.25rem 0.75rem;
  text-decoration: none;
  border-bottom: 1px solid rgba(255,255,255,0.07);
}

.sidebar-logo { height: 28px; width: auto; object-fit: contain; }

.sidebar-brand-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: white;
  border: 1.5px solid rgba(255,255,255,0.3);
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

.sidebar-role {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.25rem;
  font-size: 0.7rem;
  font-weight: 600;
  color: #F59E0B;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  margin-bottom: 0.25rem;
}

.role-dot {
  width: 7px;
  height: 7px;
  background: #F59E0B;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.sidebar-nav {
  flex: 1;
  padding: 0 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.nav-group { margin-top: 1.25rem; }

.nav-group-label {
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: rgba(255,255,255,0.3);
  text-transform: uppercase;
  padding: 0 0.5rem;
  margin: 0 0 0.35rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.55rem 0.75rem;
  border-radius: 7px;
  font-size: 0.85rem;
  font-weight: 500;
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
  position: relative;
}

.nav-item:hover { background: rgba(255,255,255,0.07); color: white; }

.nav-item--active {
  background: rgba(245,158,11,0.18);
  color: white;
  font-weight: 600;
}

.nav-item--active::before {
  content: '';
  position: absolute;
  left: 0; top: 20%; bottom: 20%;
  width: 3px;
  background: #F59E0B;
  border-radius: 0 3px 3px 0;
}

.nav-icon { width: 16px; height: 16px; flex-shrink: 0; }

.nav-badge {
  margin-left: auto;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.1rem 0.45rem;
  border-radius: 99px;
}

.nav-badge--alert {
  background: rgba(239,68,68,0.2);
  color: #FCA5A5;
}

.sidebar-logout {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: 1rem 0.75rem;
  padding: 0.6rem 0.75rem;
  border-radius: 7px;
  font-family: inherit;
  font-size: 0.85rem;
  font-weight: 500;
  color: rgba(255,255,255,0.45);
  background: none;
  border: none;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  width: calc(100% - 1.5rem);
}

.sidebar-logout svg { width: 16px; height: 16px; flex-shrink: 0; }
.sidebar-logout:hover { background: rgba(239,68,68,0.12); color: #FCA5A5; }

.main {
  flex: 1;
  margin-left: 240px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.topbar {
  position: sticky; top: 0; z-index: 100;
  background: white;
  border-bottom: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  height: 64px;
  gap: 1rem;
}

.topbar-left { display: flex; align-items: center; gap: 1rem; }

.topbar-sub {
  font-size: 0.62rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: #F59E0B;
  text-transform: uppercase;
  margin: 0;
}

.topbar-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
  line-height: 1.2;
}

.topbar-right { display: flex; align-items: center; gap: 0.75rem; }

.hamburger {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.35rem;
  color: #374151;
}

.hamburger svg { width: 20px; height: 20px; }

.topbar-btn {
  position: relative;
  background: none;
  border: 1.5px solid #E5E7EB;
  border-radius: 8px;
  padding: 0.4rem;
  cursor: pointer;
  color: #374151;
  display: flex;
  align-items: center;
}

.topbar-btn svg { width: 18px; height: 18px; }

.topbar-btn-dot {
  position: absolute;
  top: 4px; right: 4px;
  width: 7px; height: 7px;
  background: #EF4444;
  border-radius: 50%;
  border: 1.5px solid white;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: #FFFBEB;
  border: 1.5px solid #FDE68A;
  border-radius: 10px;
  padding: 0.35rem 0.75rem 0.35rem 0.35rem;
}

.user-avatar {
  width: 30px; height: 30px;
  background: linear-gradient(135deg, #F59E0B, #D97706);
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  flex-shrink: 0;
}

.user-info { display: flex; flex-direction: column; }
.user-name { font-size: 0.8rem; font-weight: 600; color: #111827; line-height: 1.2; }
.user-role { font-size: 0.68rem; color: #D97706; font-weight: 600; }

.content { flex: 1; padding: 2rem; }

.overlay {
  display: none;
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 150;
}

@media (max-width: 768px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar--open { transform: translateX(0); }
  .main { margin-left: 0; }
  .hamburger { display: flex; }
  .topbar { padding: 0 1rem; }
  .content { padding: 1rem; }
  .overlay { display: block; }
  .user-info { display: none; }
}
</style>
