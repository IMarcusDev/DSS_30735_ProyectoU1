<script setup>
import { ref, computed } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'

const route  = useRoute()
const router = useRouter()
const mobileOpen = ref(false)

const user = { name: 'Marcos Escobar', initials: 'ME', role: 'Usuario' }

const icons = {
  home:    'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
  folder:  'M3 7a2 2 0 012-2h4l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2V7z',
  check:   'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
  clock:   'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
  xcirc:   'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
  upload:  'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12',
  shield:  'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
  user:    'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
  logout:  'M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1',
  bell:    'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',
  menu:    'M4 6h16M4 12h16M4 18h16',
}

const navGroups = [
  {
    label: 'MIS ÁLBUMES',
    items: [
      { label: 'Todos',       to: '/user/albums',                              icon: 'folder', badge: 3 },
      { label: 'Aprobados',   to: '/user/albums?status=approved',              icon: 'check',  badge: 2 },
      { label: 'Pendientes',  to: '/user/albums?status=pending',               icon: 'clock',  badge: 1 },
      { label: 'Rechazados',  to: '/user/albums?status=rejected',              icon: 'xcirc', badge: null },
    ],
  },
  {
    label: 'MIS IMÁGENES',
    items: [
      { label: 'Subir imagen',    to: '/user/upload',     icon: 'upload', badge: null },
      { label: 'En cuarentena',   to: '/user/quarantine', icon: 'shield', badge: 2 },
    ],
  },
  {
    label: 'MI CUENTA',
    items: [
      { label: 'Mi perfil', to: '/user/profile', icon: 'user', badge: null },
    ],
  },
]

const pageTitle = computed(() => {
  const name = route.name
  const map = {
    UserDashboard:   'Dashboard',
    MisAlbumes:      'Mis Álbumes',
    SolicitarAlbum:  'Solicitar Álbum',
    AlbumDetalle:    'Detalle del Álbum',
  }
  return map[name] || 'Panel de Usuario'
})

function isActive(to) {
  const path = typeof to === 'string' ? to.split('?')[0] : to
  return route.path === path
}

function logout() {
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
      <nav class="sidebar-nav">
        <RouterLink to="/user/dashboard" class="nav-item" :class="{ 'nav-item--active': isActive('/user/dashboard') }">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path :d="icons.home" />
          </svg>
          <span>Dashboard</span>
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
              <path :d="icons[item.icon]" />
            </svg>
            <span>{{ item.label }}</span>
            <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
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
          <button class="hamburger" @click="mobileOpen = !mobileOpen" aria-label="Abrir menú">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
              <path :d="icons.menu" />
            </svg>
          </button>
          <div>
            <p class="topbar-sub">PANEL DE USUARIO</p>
            <h1 class="topbar-title">{{ pageTitle }}</h1>
          </div>
        </div>

        <div class="topbar-right">
          <button class="topbar-btn" aria-label="Notificaciones">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path :d="icons.bell" />
            </svg>
            <span class="topbar-btn-dot"></span>
          </button>

          <div class="user-chip">
            <div class="user-avatar">{{ user.initials }}</div>
            <div class="user-info">
              <span class="user-name">{{ user.name }}</span>
              <span class="user-role">{{ user.role }}</span>
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
  background: #0F1829;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  z-index: 200;
  overflow-y: auto;
  transition: transform 0.25s ease;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 1.25rem 1.25rem 1rem;
  text-decoration: none;
  border-bottom: 1px solid rgba(255,255,255,0.07);
  margin-bottom: 0.5rem;
}

.sidebar-logo {
  height: 28px;
  width: auto;
  object-fit: contain;
}

.sidebar-brand-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: white;
  border: 1.5px solid rgba(255,255,255,0.3);
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

.sidebar-nav {
  flex: 1;
  padding: 0 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.nav-group {
  margin-top: 1.25rem;
}

.nav-group-label {
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: rgba(255,255,255,0.35);
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
  color: rgba(255,255,255,0.65);
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
  position: relative;
}

.nav-item:hover {
  background: rgba(255,255,255,0.07);
  color: white;
}

.nav-item--active {
  background: rgba(46,117,182,0.25);
  color: white;
  font-weight: 600;
}

.nav-item--active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 20%;
  bottom: 20%;
  width: 3px;
  background: #2E75B6;
  border-radius: 0 3px 3px 0;
}

.nav-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.nav-badge {
  margin-left: auto;
  background: rgba(255,255,255,0.12);
  color: rgba(255,255,255,0.8);
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.1rem 0.45rem;
  border-radius: 99px;
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
  color: rgba(255,255,255,0.5);
  background: none;
  border: none;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  width: calc(100% - 1.5rem);
}

.sidebar-logout svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.sidebar-logout:hover {
  background: rgba(239,68,68,0.12);
  color: #FCA5A5;
}

.main {
  flex: 1;
  margin-left: 240px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  border-bottom: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  height: 64px;
  gap: 1rem;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.topbar-sub {
  font-size: 0.62rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: #2E75B6;
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

.topbar-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

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
  top: 4px;
  right: 4px;
  width: 7px;
  height: 7px;
  background: #EF4444;
  border-radius: 50%;
  border: 1.5px solid white;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: #F9FAFB;
  border: 1.5px solid #E5E7EB;
  border-radius: 10px;
  padding: 0.35rem 0.75rem 0.35rem 0.35rem;
  cursor: pointer;
}

.user-avatar {
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #2E75B6, #1E4D7B);
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  flex-shrink: 0;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.8rem;
  font-weight: 600;
  color: #111827;
  line-height: 1.2;
}

.user-role {
  font-size: 0.68rem;
  color: #6B7280;
}

.content {
  flex: 1;
  padding: 2rem;
}

.overlay {
  display: none;
  position: fixed;
  inset: 0;
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
