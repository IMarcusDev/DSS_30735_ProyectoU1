<template>
  <div class="brand-panel">
    <div class="brand-header">
      <img src="/logo.png" alt="SecureFrame" />
      <span class="brand-name">Secureframe</span>
    </div>

    <div class="brand-body">
      <p class="brand-tag">SEGURIDAD EN CADA PÍXEL</p>
      <h1 class="brand-heading">
        Protege tus imágenes<br>
        <strong>con análisis automático.</strong>
      </h1>
      <p class="brand-sub">
        Detección de esteganografía, control por roles y
        publicación segura — todo en una sola plataforma.
      </p>
    </div>

    <div class="brand-footer">
      <span>LSB + MIME</span>
      <span class="dot">·</span>
      <span>100% EXIF removido</span>
    </div>

    <div class="deco deco--1"></div>
    <div class="deco deco--2"></div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.brand-panel {
  position: relative;
  overflow: hidden;
  background: linear-gradient(160deg, #1E4D7B 0%, #193f64 55%, #142f4e 100%);
  padding: 2.5rem 3rem;
  display: flex;
  flex-direction: column;
  color: white;
  font-family: 'Inter', system-ui, sans-serif;
  min-height: 100vh;
}

.brand-header {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  z-index: 1;
}

.brand-header img {
  height: 36px;
  width: auto;
  object-fit: contain;
}

.brand-name {
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  border: 1.5px solid rgba(255, 255, 255, 0.35);
  padding: 0.2rem 0.65rem;
  border-radius: 4px;
}

.brand-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 2rem 0;
  z-index: 1;
}

.brand-tag {
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.6;
  margin: 0 0 1.25rem;
}

.brand-heading {
  font-size: clamp(1.6rem, 2.2vw, 2.4rem);
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 1.25rem;
  max-width: 360px;
}

.brand-heading strong {
  font-weight: 800;
}

.brand-sub {
  font-size: 0.875rem;
  opacity: 0.7;
  line-height: 1.65;
  margin: 0;
  max-width: 320px;
}

.brand-footer {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 0.8rem;
  opacity: 0.5;
  z-index: 1;
}

.deco {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.07);
  pointer-events: none;
}

.deco--1 {
  width: 420px;
  height: 420px;
  bottom: -120px;
  right: -120px;
}

.deco--2 {
  width: 280px;
  height: 280px;
  bottom: -30px;
  right: 70px;
}
</style>
