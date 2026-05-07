# SecureFrame Gallery

Galería multimedia pública con detección de esteganografía y gestión de riesgos en el SDLC.

Proyecto Integrador — Desarrollo de Software Seguro  
Universidad de las Fuerzas Armadas ESPE · 2026

---

## Descripción

SecureFrame Gallery es una aplicación web segura para la gestión de una galería pública de imágenes. El núcleo del proyecto es la detección automatizada de esteganografía en archivos subidos por usuarios, combinada con un flujo de aprobación por roles y controles de seguridad aplicados en todas las capas del SDLC.

---

## Roles del sistema

| Rol | Descripción |
|-----|-------------|
| **Visitante** | Navega álbumes y ve imágenes aprobadas sin autenticarse |
| **Usuario** | Se registra, solicita álbumes y sube imágenes |
| **Supervisor** | Aprueba/rechaza solicitudes de álbumes e imágenes en cuarentena |

---

## Requisitos funcionales

### RF01 — Registro y Autenticación Segura
- Registro de nuevos usuarios con política de contraseñas robusta
- Almacenamiento de credenciales con **Argon2id** (salting + hashing fuerte)
- Protección contra enumeración de usuarios
- Rate limiting para prevenir fuerza bruta

### RF02 — Gestión de Álbumes (Solicitud y Aprobación)
- Usuario autenticado solicita creación de álbum (Título, Descripción, Privacidad)
- La solicitud queda en estado **"Pendiente de Revisión"**
- El Supervisor aprueba o rechaza desde un panel de administración
- Validación estricta de entradas para prevenir **Stored XSS** en descripciones

### RF03 — Subida de Imágenes y Detección de Esteganografía *(Núcleo del proyecto)*
Flujo de validación antes de almacenar cualquier archivo:

1. **Validación de tipo MIME real** — File Magic Numbers (no solo extensión)
2. **Re-encoding y stripping de metadatos EXIF** — elimina amenazas de geolocalización y XSS en EXIF
3. **Análisis esteganográfico automatizado:**
   - Análisis del histograma de color
   - Análisis LSB (Least Significant Bit) para detección de ruido estadístico anómalo
   - Detección de marcadores sospechosos (EOF attacks)
4. **Resultado:**
   - `Limpio` → se almacena y muestra en la galería pública
   - `Sospechoso / Positivo` → va a cuarentena para revisión manual del Supervisor

### RF04 — Flujo de Revisión Manual (Supervisor)
- Bandeja de "Imágenes en Cuarentena"
- Vista de la imagen con metadatos del análisis automático (motivo del marcado)
- Acciones: **Aprobar** (ignorar alerta) o **Rechazar** (eliminar archivo)

### RF05 — Visualización Pública Segura
- Visitantes no autenticados navegan álbumes y ven imágenes aprobadas
- Cabeceras de seguridad implementadas:
  - `Content-Security-Policy (CSP)` — mitiga XSS y SVG maliciosos
  - `X-Content-Type-Options: nosniff` — previene MIME sniffing

---

## Controles de seguridad transversales

- RBAC (Control de Acceso Basado en Roles) en todos los endpoints
- Gestión segura de sesiones
- Validación y sanitización de todas las entradas del usuario
- Protección CSRF
- Sin almacenamiento de archivos originales antes de pasar el análisis completo

---

## Stack tecnológico

> *Por definir — se actualizará esta sección con las tecnologías elegidas.*

---

## Instalación y despliegue

> *Por completar — se incluirán variables de entorno, dependencias y pasos de despliegue.*

---

## Credenciales de prueba

> *Por completar — se agregarán credenciales demo para los roles Usuario y Supervisor.*

---

## Justificación técnica — Detección de esteganografía

> *Por completar — se documentará la librería/método elegido y su justificación técnica.*

---

## Alineación con estándares de seguridad

- **OWASP ASVS Nivel 2** — validación de entradas, gestión de sesiones, control de acceso
- **NIST SP 800-218 (SSDF)** — prácticas de seguridad integradas en el SDLC
- **OWASP Top 10** — mitigación de las vulnerabilidades más críticas en aplicaciones web

---

## Entregables del proyecto

- [ ] Código fuente de la aplicación web
- [ ] Repositorio público en GitHub con historial de commits completo
- [ ] Documento de Plan Estratégico de Seguridad (PDF, máx. 10 páginas)
- [ ] Aplicación desplegada y funcional al momento de la entrega

**Fecha límite de entrega:** 12 de mayo de 2026, 11:00  
**Defensas:** 12 y 14 de mayo de 2026 (selección aleatoria)
