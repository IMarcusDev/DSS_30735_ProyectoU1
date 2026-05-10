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
- Registro de nuevos usuarios con política de contraseñas robusta (mínimo 8 caracteres, mayúscula, dígito y carácter especial)
- Almacenamiento de credenciales con **bcrypt** (salting + hashing fuerte, factor de coste adaptativo)
- Protección contra enumeración de usuarios (mismo mensaje de error en login independientemente del motivo)
- Rate limiting en `/auth/login` (10 req/min) y `/auth/register` (5 req/min) para prevenir fuerza bruta

### RF02 — Gestión de Álbumes (Solicitud y Aprobación)
- Usuario autenticado solicita creación de álbum (Título, Descripción, Privacidad)
- La solicitud queda en estado **"Pendiente de Revisión"**
- El Supervisor aprueba o rechaza desde un panel de administración
- Validación estricta de entradas para prevenir **Stored XSS** en descripciones

### RF03 — Subida de Imágenes y Detección de Esteganografía *(Núcleo del proyecto)*
Flujo de validación antes de almacenar cualquier archivo:

1. **Validación de tipo MIME real** — File Magic Numbers (no solo extensión ni cabecera HTTP)
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
- Historial de auditoría personal del supervisor (aprobaciones y rechazos)

### RF05 — Visualización Pública Segura
- Visitantes no autenticados navegan álbumes y ven imágenes aprobadas
- Cabeceras de seguridad implementadas:
  - `Content-Security-Policy (CSP)` — mitiga XSS y SVG maliciosos
  - `X-Content-Type-Options: nosniff` — previene MIME sniffing

---

## Controles de seguridad transversales

- RBAC (Control de Acceso Basado en Roles) en todos los endpoints mediante JWT
- Gestión segura de sesiones con tokens firmados HS256
- Validación y sanitización de todas las entradas del usuario (Pydantic)
- Protección contra timing attacks en login (hash dummy para usuarios inexistentes)
- Sin almacenamiento de archivos originales antes de pasar el análisis completo
- Archivos temporales eliminados del disco inmediatamente tras el análisis

---

## Stack tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| **Frontend** | Vue 3 + TypeScript + Vite | Vue 3.x |
| **Backend** | FastAPI (Python) | 0.136.1 |
| **Base de datos** | PostgreSQL vía Supabase | – |
| **Almacenamiento** | Supabase Storage | – |
| **Autenticación** | JWT HS256 + bcrypt | PyJWT 2.12 / bcrypt 5.0 |
| **Rate limiting** | slowapi (Starlette) | 0.1.9 |
| **Validación MIME** | python-magic (libmagic) | 0.4.27 |
| **Análisis de imagen** | Pillow + OpenCV + numpy | 12.2 / 4.13 / 2.4 |
| **ORM / Driver DB** | psycopg2-binary | 2.9.12 |
| **Gestión de config** | python-dotenv | 1.2.2 |

---

## Instalación y despliegue

### Prerrequisitos

- Python 3.11+
- Node.js 18+
- Cuenta en [Supabase](https://supabase.com) (base de datos PostgreSQL + Storage)
- `libmagic` instalado en el sistema:
  ```bash
  # Ubuntu / Debian
  sudo apt install libmagic1
  # Arch Linux
  sudo pacman -S file
  # macOS
  brew install libmagic
  ```

### 1. Clonar el repositorio

```bash
git clone https://github.com/IMarcusDev/DSS_30735_ProyectoU1.git
cd DSS_30735_ProyectoU1
```

### 2. Backend

```bash
cd Backend

# Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env            # editar con tus valores
```

Contenido de `.env`:

```env
# Base de datos (Supabase → Project Settings → Database)
DB_HOST=db.<tu-proyecto>.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=<tu-password>

# JWT — genera con: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=<clave-aleatoria-256-bits>

# Supabase Storage (usar service_role key)
SUPABASE_URL=https://<tu-proyecto>.supabase.co
SUPABASE_KEY=<service-role-key>
SUPABASE_BUCKET=images

# CORS
ALLOWED_ORIGINS=http://localhost:5173
```

Ejecutar migraciones de base de datos (en orden):

```bash
# Desde psql o el SQL Editor de Supabase
# 1. Esquema inicial
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f db/init.sql

# 2. Migraciones incrementales
psql ... -f db/migration_v2.sql
psql ... -f db/migration_v3.sql
```

Arrancar el servidor:

```bash
uvicorn main:app --reload
# API disponible en http://localhost:8000
# Documentación Swagger: http://localhost:8000/docs
```

### 3. Frontend

```bash
cd Frontend/secureframe
npm install

# Crear archivo de entorno
echo "VITE_API_URL=http://localhost:8000" > .env

npm run dev
# Aplicación disponible en http://localhost:5173
```

---

## Credenciales de prueba

Las siguientes cuentas demo están creadas en la base de datos de producción:

| Rol | Email | Contraseña |
|-----|-------|-----------|
| **Usuario** | `demo.usuario@secureframe.ec` | `Demo1234*` |
| **Supervisor** | `demo.supervisor@secureframe.ec` | `Admin1234*` |

> La cuenta de Visitante no requiere credenciales — acceder directamente a `/galeria`.

---

## Justificación técnica — Detección de esteganografía

### ¿Por qué no basta con validar la extensión o el Content-Type?

Un atacante puede renombrar cualquier archivo a `.jpg` y enviar `Content-Type: image/jpeg`. Estas validaciones superficiales no inspeccionan el contenido real del archivo. El proyecto aplica **cuatro técnicas complementarias** que operan sobre los bytes del archivo:

### 1. Validación MIME por File Magic Numbers (`python-magic` / libmagic)

La librería `python-magic` invoca `libmagic`, la misma base de datos que usa el comando `file` de Unix, para identificar el tipo real del archivo leyendo sus primeros bytes (magic bytes). Para PNG: `\x89PNG\r\n\x1a\n`; para JPEG: `\xFF\xD8`. Esta comprobación se realiza **en memoria** antes de escribir en disco, y se reutiliza el resultado para el análisis posterior (evitando falsos positivos por variaciones del detector al leer desde fichero).

**Amenaza mitigada:** File Upload Bypass — subir malware disfrazado de imagen.

### 2. Stripping de metadatos EXIF (`Pillow`)

La librería `Pillow` (PIL) abre la imagen y la re-codifica eliminando todos los chunks de metadatos (`pnginfo=None` en PNG, `exif=b""` en JPEG). Los metadatos EXIF pueden contener:
- Coordenadas GPS (privacidad del usuario)
- Identificadores de cámara/software (fingerprinting)
- Scripts JS embebidos en comentarios EXIF (XSS en visores vulnerables)

**Amenaza mitigada:** Fuga de información geográfica, XSS vía EXIF.

### 3. Análisis LSB — Least Significant Bit (`numpy`)

El análisis LSB es la técnica de esteganografía más común: los mensajes se ocultan modificando el bit menos significativo de cada píxel. En imágenes naturales, la distribución de bits LSB sigue una distribución aproximadamente uniforme (ratio ≈ 0.50). Una imagen manipulada presenta una desviación estadística medible.

```python
arr = np.array(img)
lsb = arr & 1
ratio = np.mean(lsb)
suspicious = bool(ratio > 0.52 or ratio < 0.48)
```

**Amenaza mitigada:** Exfiltración de datos ocultos en píxeles, C2 encubierto.

### 4. Análisis de histograma de color (`OpenCV + numpy`)

Las imágenes con datos esteganográficos suelen presentar una distribución de valores de píxel anormalmente uniforme (la información oculta "aplana" el histograma). Se calcula la varianza del histograma por canal (R, G, B):

```python
variance = np.var(hist_r) + np.var(hist_g) + np.var(hist_b)
suspicious = bool(variance < 5000)
```

Una varianza muy baja indica una imagen estadísticamente "demasiado uniforme" para ser natural.

**Amenaza mitigada:** Detección de manipulación masiva de píxeles.

### 5. Análisis de marcadores EOF (`built-in`)

Las imágenes válidas terminan con marcadores bien definidos (JPEG: `\xFF\xD9`, PNG: `IEND` + CRC). Cualquier byte extra tras el EOF es una señal de datos appended — técnica trivial de ocultamiento de archivos binarios.

**Amenaza mitigada:** Archivos ZIP/EXE concatenados tras una imagen legítima.

---

## Alineación con estándares de seguridad

- **OWASP ASVS Nivel 2** — validación de entradas (V5), gestión de sesiones (V3), control de acceso (V4), manejo de archivos (V12)
- **NIST SP 800-218 (SSDF)** — prácticas de seguridad integradas en todas las fases del SDLC: modelado de amenazas en diseño, validación en desarrollo, revisión manual en operación
- **OWASP Top 10** — mitigación directa de A01 (Control de Acceso), A02 (Fallos Criptográficos), A03 (Inyección), A04 (Diseño Inseguro), A05 (Configuración Incorrecta), A07 (Autenticación), A08 (Integridad de Software y Datos)

---

## Entregables del proyecto

- [x] Código fuente de la aplicación web
- [x] Repositorio público en GitHub con historial de commits completo
- [ ] Documento de Plan Estratégico de Seguridad (PDF, máx. 10 páginas)
- [x] Aplicación desplegada y funcional al momento de la entrega

**Fecha límite de entrega:** 12 de mayo de 2026, 11:00  
**Defensas:** 12 y 14 de mayo de 2026 (selección aleatoria)
