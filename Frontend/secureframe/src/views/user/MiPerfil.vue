<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAuth } from '../../composables/useAuth'

const { user, fetchMe } = useAuth()

onMounted(fetchMe)

const initials = computed(() => {
  if (!user.value?.name) return 'U'
  const first = user.value.name[0] ?? ''
  const last  = user.value.last_name?.[0] ?? ''
  return (first + last).toUpperCase()
})

const fullName = computed(() =>
  user.value ? `${user.value.name ?? ''} ${user.value.last_name ?? ''}`.trim() : '—'
)

const roleLabel = computed(() =>
  user.value?.role === 'Administrator' ? 'Supervisor' : 'Usuario'
)

const roleColor = computed(() =>
  user.value?.role === 'Administrator'
    ? { color: '#D97706', bg: '#FFFBEB', border: '#FDE68A' }
    : { color: '#2563EB', bg: '#EFF6FF', border: '#BFDBFE' }
)
</script>

<template>
  <div class="page">
    <div class="page-header">
      <h2 class="page-title">Mi Perfil</h2>
      <p class="page-sub">Información de tu cuenta</p>
    </div>

    <div class="profile-card">
      <div class="avatar-section">
        <div class="avatar">{{ initials }}</div>
        <div class="avatar-info">
          <h3 class="full-name">{{ fullName }}</h3>
          <span
            class="role-badge"
            :style="{ color: roleColor.color, background: roleColor.bg, borderColor: roleColor.border }"
          >
            {{ roleLabel }}
          </span>
        </div>
      </div>

      <div class="divider"></div>

      <div class="info-grid">
        <div class="info-row">
          <div class="info-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
              <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            Nombre
          </div>
          <div class="info-value">{{ user?.name ?? '—' }}</div>
        </div>

        <div class="info-row">
          <div class="info-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
              <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            Apellido
          </div>
          <div class="info-value">{{ user?.last_name ?? '—' }}</div>
        </div>

        <div class="info-row">
          <div class="info-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
              <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            Correo electrónico
          </div>
          <div class="info-value">{{ user?.email ?? '—' }}</div>
        </div>

        <div class="info-row">
          <div class="info-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
              <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
            Rol
          </div>
          <div class="info-value">{{ roleLabel }}</div>
        </div>

        <div class="info-row">
          <div class="info-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
              <path d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0"/>
            </svg>
            ID de usuario
          </div>
          <div class="info-value info-value--mono">{{ user?.user_id ?? '—' }}</div>
        </div>
      </div>

      <div class="divider"></div>

      <div class="security-section">
        <p class="security-title">Seguridad</p>
        <p class="security-note">
          Para cambiar tu contraseña o datos personales, contacta al administrador del sistema.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page { display: flex; flex-direction: column; gap: 1.25rem; font-family: 'Inter', system-ui, sans-serif; }

.page-header {}
.page-title { font-size: 1.4rem; font-weight: 800; color: #111827; margin: 0 0 0.2rem; }
.page-sub   { font-size: 0.82rem; color: #6B7280; margin: 0; }

.profile-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 2rem;
  max-width: 620px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.avatar-section { display: flex; align-items: center; gap: 1.25rem; }

.avatar {
  width: 72px; height: 72px;
  background: linear-gradient(135deg, #2E75B6, #1E4D7B);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.6rem;
  font-weight: 800;
  flex-shrink: 0;
  letter-spacing: -0.02em;
}

.avatar-info { display: flex; flex-direction: column; gap: 0.4rem; }
.full-name { font-size: 1.2rem; font-weight: 700; color: #111827; margin: 0; }

.role-badge {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.65rem;
  border-radius: 99px;
  border: 1.5px solid;
  width: fit-content;
}

.divider { height: 1px; background: #F3F4F6; }

.info-grid { display: flex; flex-direction: column; gap: 0; }

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 0;
  border-bottom: 1px solid #F9FAFB;
  gap: 1rem;
}

.info-row:last-child { border-bottom: none; }

.info-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  font-weight: 500;
  color: #9CA3AF;
  min-width: 180px;
}

.info-label svg { width: 16px; height: 16px; flex-shrink: 0; }

.info-value {
  font-size: 0.88rem;
  font-weight: 600;
  color: #111827;
  text-align: right;
  word-break: break-all;
}

.info-value--mono {
  font-family: 'Menlo', 'Monaco', monospace;
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 400;
}

.security-section {}
.security-title { font-size: 0.82rem; font-weight: 700; color: #374151; margin: 0 0 0.4rem; }
.security-note  { font-size: 0.78rem; color: #9CA3AF; margin: 0; line-height: 1.6; }

@media (max-width: 600px) {
  .profile-card { padding: 1.25rem; }
  .info-label   { min-width: 130px; }
  .avatar       { width: 56px; height: 56px; font-size: 1.2rem; border-radius: 12px; }
}
</style>
