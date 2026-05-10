import { createRouter, createWebHistory } from 'vue-router'
import Home               from '@/views/Home.vue'
import Login              from '@/views/Login.vue'
import Register           from '@/views/Register.vue'
import GaleriaPublica     from '@/views/galeria/GaleriaPublica.vue'
import AlbumPublico       from '@/views/galeria/AlbumPublico.vue'
import UserLayout         from '@/layouts/UserLayout.vue'
import Dashboard          from '@/views/user/Dashboard.vue'
import MisAlbumes         from '@/views/user/MisAlbumes.vue'
import SolicitarAlbum     from '@/views/user/SolicitarAlbum.vue'
import SubirImagen        from '@/views/user/SubirImagen.vue'
import VerAlbum           from '@/views/user/VerAlbum.vue'
import MiPerfil           from '@/views/user/MiPerfil.vue'
import SupervisorLayout   from '@/layouts/SupervisorLayout.vue'
import SuperDashboard     from '@/views/supervisor/SuperDashboard.vue'
import SolicitudesAlbumes from '@/views/supervisor/SolicitudesAlbumes.vue'
import Cuarentena         from '@/views/supervisor/Cuarentena.vue'
import Historial          from '@/views/supervisor/Historial.vue'

function getTokenPayload(): { role?: string } | null {
  try {
    const t = localStorage.getItem('access_token')
    if (!t) return null
    return JSON.parse(atob(t.split('.')[1]!))
  } catch { return null }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/',            name: 'Home',          component: Home           },
    { path: '/login',       name: 'Login',         component: Login          },
    { path: '/register',    name: 'Register',      component: Register       },

    // Visitante
    { path: '/galeria',     name: 'GaleriaPublica', component: GaleriaPublica },
    { path: '/galeria/:id', name: 'AlbumPublico',   component: AlbumPublico   },

    // Usuario autenticado
    {
      path: '/user',
      component: UserLayout,
      redirect: '/user/dashboard',
      meta: { requiresAuth: true },
      children: [
        { path: 'dashboard',  name: 'UserDashboard',  component: Dashboard      },
        { path: 'albums',     name: 'MisAlbumes',     component: MisAlbumes     },
        { path: 'albums/new', name: 'SolicitarAlbum', component: SolicitarAlbum },
        { path: 'albums/:id', name: 'VerAlbum',       component: VerAlbum       },
        { path: 'upload',     name: 'SubirImagen',    component: SubirImagen    },
        { path: 'profile',   name: 'MiPerfil',       component: MiPerfil       },
      ],
    },

    // Supervisor
    {
      path: '/supervisor',
      component: SupervisorLayout,
      redirect: '/supervisor/dashboard',
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        { path: 'dashboard',   name: 'SuperDashboard',     component: SuperDashboard     },
        { path: 'solicitudes', name: 'SolicitudesAlbumes',  component: SolicitudesAlbumes },
        { path: 'cuarentena',  name: 'Cuarentena',          component: Cuarentena         },
        { path: 'historial',   name: 'Historial',           component: Historial          },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const payload = getTokenPayload()

  if (to.meta.requiresAuth && !payload) {
    return '/login'
  }

  if (to.meta.requiresAdmin && payload?.role !== 'Administrator') {
    return '/login'
  }
})

export default router
