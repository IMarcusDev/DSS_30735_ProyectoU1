import { createRouter, createWebHistory } from 'vue-router'
import Home            from '@/views/Home.vue'
import Login           from '@/views/Login.vue'
import Register        from '@/views/Register.vue'
import GaleriaPublica  from '@/views/galeria/GaleriaPublica.vue'
import AlbumPublico    from '@/views/galeria/AlbumPublico.vue'
import UserLayout      from '@/layouts/UserLayout.vue'
import Dashboard       from '@/views/user/Dashboard.vue'
import MisAlbumes      from '@/views/user/MisAlbumes.vue'
import SolicitarAlbum  from '@/views/user/SolicitarAlbum.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/',             name: 'Home',          component: Home           },
    { path: '/login',        name: 'Login',         component: Login          },
    { path: '/register',     name: 'Register',      component: Register       },

    // Visitante
    { path: '/galeria',      name: 'GaleriaPublica', component: GaleriaPublica },
    { path: '/galeria/:id',  name: 'AlbumPublico',   component: AlbumPublico   },

    // Usuario
    {
      path: '/user',
      component: UserLayout,
      redirect: '/user/dashboard',
      children: [
        { path: 'dashboard',  name: 'UserDashboard',  component: Dashboard      },
        { path: 'albums',     name: 'MisAlbumes',     component: MisAlbumes     },
        { path: 'albums/new', name: 'SolicitarAlbum', component: SolicitarAlbum },
      ],
    },
  ],
})

export default router
