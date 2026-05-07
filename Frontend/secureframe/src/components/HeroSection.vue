<script setup>
const steps = [
  {
    number: 1,
    label: 'PASO 1',
    title: 'Explora la galería',
    description: 'Navega álbumes públicos y ve imágenes aprobadas sin necesidad de registrarte.',
  },
  {
    number: 2,
    label: 'PASO 2',
    title: 'Regístrate y sube',
    description: 'Crea tu cuenta, solicita un álbum y sube tus imágenes fácilmente.',
  },
  {
    number: 3,
    label: 'PASO 3',
    title: 'Análisis automático',
    description: 'Detección LSB, validación MIME real y limpieza completa de metadatos EXIF.',
  },
  {
    number: 4,
    label: 'PASO 4',
    title: 'Publicación segura',
    description: 'Imágenes limpias pasan a la galería. Las sospechosas van a cuarentena.',
  },
]

const stats = [
  { value: 'LSB', label: 'Análisis esteganográfico automatizado' },
  { value: '3',   label: 'Roles de acceso diferenciados' },
  { value: '100%',label: 'Metadatos EXIF eliminados en cada subida' },
]
</script>

<template>
  <section class="hero">
    <span class="hero-tag">DE LA SUBIDA A LA GALERÍA EN 4 PASOS</span>

    <h2 class="hero-heading">
      Compartir imágenes de forma segura<br>
      <span class="hero-heading-accent">nunca fue tan simple.</span>
    </h2>

    <p class="hero-sub">
      Detección automática de esteganografía, control por roles y auditoría completa
      en cada archivo que subas a SecureFrame Gallery.
    </p>

    <div class="steps">
      <template v-for="(step, i) in steps" :key="step.number">
        <div class="step-card" :class="{ 'step-card--active': i === 0 }">
          <div class="step-card__top">
            <span class="step-number" :class="{ 'step-number--active': i === 0 }">
              {{ step.number }}
            </span>
            <span class="step-label">{{ step.label }}</span>
          </div>

          <h3 class="step-title">{{ step.title }}</h3>
          <p class="step-desc">{{ step.description }}</p>

          <div class="step-illustration">
            <svg v-if="i === 0" viewBox="0 0 200 110" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="4"  y="4"  width="58" height="46" rx="4" fill="#D1D5DB"/>
              <rect x="70" y="4"  width="58" height="46" rx="4" fill="#E5E7EB"/>
              <rect x="136" y="4" width="60" height="46" rx="4" fill="#D1D5DB"/>
              <rect x="4"  y="58" width="58" height="46" rx="4" fill="#E5E7EB"/>
              <rect x="70" y="58" width="58" height="46" rx="4" fill="#D1D5DB"/>
              <rect x="136" y="58" width="60" height="46" rx="4" fill="#E5E7EB"/>
              <rect x="14" y="12" width="38" height="6" rx="2" fill="#9CA3AF"/>
              <rect x="80" y="12" width="38" height="6" rx="2" fill="#9CA3AF"/>
              <rect x="146" y="12" width="38" height="6" rx="2" fill="#9CA3AF"/>
            </svg>

            <svg v-if="i === 1" viewBox="0 0 200 110" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="20" y="6" width="160" height="30" rx="4" fill="#E5E7EB"/>
              <rect x="28" y="13" width="80" height="6" rx="2" fill="#9CA3AF"/>
              <rect x="28" y="14" width="60" height="4" rx="2" fill="#9CA3AF"/>
              <rect x="20" y="44" width="160" height="42" rx="6" stroke="#9CA3AF" stroke-width="2" stroke-dasharray="6 4" fill="#F9FAFB"/>
              <path d="M100 74 L100 58 M100 58 L93 65 M100 58 L107 65" stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <rect x="66" y="78" width="68" height="12" rx="4" fill="#2E75B6"/>
              <rect x="74" y="81" width="52" height="5" rx="2" fill="white" opacity="0.8"/>
            </svg>

            <svg v-if="i === 2" viewBox="0 0 200 110" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="16" y="8" width="168" height="20" rx="4" fill="#E5E7EB"/>
              <rect x="24" y="13" width="40" height="5" rx="2" fill="#9CA3AF"/>
              <rect x="24" y="13" width="110" height="5" rx="2" fill="#2E75B6" opacity="0.7"/>
              <rect x="16" y="36" width="168" height="10" rx="3" fill="#E5E7EB"/>
              <rect x="24" y="39" width="30" height="4" rx="2" fill="#9CA3AF"/>
              <rect x="24" y="39" width="80" height="4" rx="2" fill="#10B981" opacity="0.8"/>
              <rect x="16" y="54" width="168" height="10" rx="3" fill="#E5E7EB"/>
              <rect x="24" y="57" width="30" height="4" rx="2" fill="#9CA3AF"/>
              <rect x="24" y="57" width="60" height="4" rx="2" fill="#10B981" opacity="0.8"/>
              <rect x="16" y="72" width="168" height="10" rx="3" fill="#E5E7EB"/>
              <rect x="24" y="75" width="30" height="4" rx="2" fill="#9CA3AF"/>
              <rect x="24" y="75" width="40" height="4" rx="2" fill="#F59E0B" opacity="0.8"/>
              <rect x="50" y="90" width="100" height="14" rx="4" fill="#E5E7EB"/>
              <rect x="58" y="94" width="84" height="5" rx="2" fill="#9CA3AF"/>
            </svg>

            <svg v-if="i === 3" viewBox="0 0 200 110" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="8"  y="8"  width="86" height="64" rx="4" fill="#D1D5DB"/>
              <rect x="104" y="8"  width="88" height="64" rx="4" fill="#E5E7EB"/>
              <rect x="8"  y="80" width="86" height="22" rx="4" fill="#E5E7EB"/>
              <rect x="104" y="80" width="88" height="22" rx="4" fill="#D1D5DB"/>
              <circle cx="156" cy="28" r="14" fill="#10B981"/>
              <path d="M150 28 L154 32 L162 24" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              <rect x="116" y="86" width="64" height="5" rx="2" fill="#9CA3AF"/>
              <rect x="16" y="86" width="64" height="5" rx="2" fill="#9CA3AF"/>
            </svg>
          </div>
        </div>

        <span v-if="i < steps.length - 1" class="step-arrow" aria-hidden="true">→</span>
      </template>
    </div>

    <a href="#register" class="cta-btn">Comenzar ahora — es gratis &nbsp;→</a>
  </section>

  <section class="stats-bar">
    <div v-for="stat in stats" :key="stat.value" class="stat-item">
      <span class="stat-value">{{ stat.value }}</span>
      <span class="stat-label">{{ stat.label }}</span>
    </div>
  </section>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 5rem 2rem 4rem;
  font-family: 'Inter', 'Roboto', system-ui, sans-serif;
  background-color: #F5F3F5;
}

.hero-tag {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: #2E75B6;
  text-transform: uppercase;
  margin-bottom: 1.25rem;
}

.hero-heading {
  font-size: clamp(2rem, 4.5vw, 3.25rem);
  font-weight: 800;
  line-height: 1.15;
  color: #111827;
  margin: 0 0 1.25rem;
  max-width: 760px;
}

.hero-heading-accent {
  color: #2E75B6;
}

.hero-sub {
  font-size: clamp(0.9rem, 1.5vw, 1.05rem);
  color: #374151;
  max-width: 560px;
  line-height: 1.65;
  margin: 0 0 3.5rem;
}

.steps {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  gap: 0;
  width: 100%;
  max-width: 1100px;
  margin-bottom: 3rem;
}

.step-arrow {
  display: flex;
  align-items: center;
  padding: 0 0.5rem;
  font-size: 1.25rem;
  color: #9CA3AF;
  flex-shrink: 0;
  align-self: center;
  padding-bottom: 3rem;
}

.step-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border: 1.5px solid #E5E7EB;
  border-radius: 10px;
  padding: 1.25rem;
  text-align: left;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.step-card:hover {
  box-shadow: 0 4px 20px rgba(46, 117, 182, 0.12);
  border-color: #2E75B6;
}

.step-card--active {
  border-color: #2E75B6;
  box-shadow: 0 4px 20px rgba(46, 117, 182, 0.15);
}

.step-card__top {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.6rem;
}

.step-number {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 700;
  border: 1.5px solid #D1D5DB;
  color: #6B7280;
  flex-shrink: 0;
}

.step-number--active {
  background: #2E75B6;
  border-color: #2E75B6;
  color: white;
}

.step-label {
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: #9CA3AF;
  text-transform: uppercase;
}

.step-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.4rem;
}

.step-desc {
  font-size: 0.78rem;
  color: #6B7280;
  line-height: 1.55;
  margin: 0 0 1rem;
  flex: 1;
}

.step-illustration {
  width: 100%;
  margin-top: auto;
}

.step-illustration svg {
  width: 100%;
  height: auto;
  display: block;
}

.cta-btn {
  display: inline-block;
  background: #2E75B6;
  color: white;
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 1rem;
  font-weight: 600;
  padding: 0.85rem 2.25rem;
  border-radius: 8px;
  text-decoration: none;
  box-shadow: 0 4px 14px rgba(46, 117, 182, 0.35);
  transition: background 0.2s ease, box-shadow 0.2s ease, transform 0.15s ease;
}

.cta-btn:hover {
  background: #1E4D7B;
  box-shadow: 0 6px 20px rgba(30, 77, 123, 0.4);
  transform: translateY(-1px);
}

.cta-btn:active {
  transform: translateY(0);
  box-shadow: none;
}

.stats-bar {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 0;
  background: #1E4D7B;
  font-family: 'Inter', system-ui, sans-serif;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2.5rem 4rem;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  flex: 1;
  max-width: 340px;
}

.stat-item:last-child {
  border-right: none;
}

.stat-value {
  font-size: clamp(1.75rem, 3vw, 2.5rem);
  font-weight: 800;
  color: white;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.65);
  text-align: center;
  line-height: 1.4;
}

@media (max-width: 900px) {
  .steps {
    flex-direction: column;
    gap: 0.75rem;
  }

  .step-arrow {
    transform: rotate(90deg);
    padding: 0;
    align-self: center;
  }

  .step-illustration svg {
    max-height: 90px;
  }

  .stat-item {
    padding: 2rem 1.5rem;
  }
}

@media (max-width: 600px) {
  .hero {
    padding: 3rem 1.25rem 2.5rem;
  }

  .stats-bar {
    flex-direction: column;
  }

  .stat-item {
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: 1.5rem 1.25rem;
    max-width: 100%;
  }

  .stat-item:last-child {
    border-bottom: none;
  }
}
</style>
