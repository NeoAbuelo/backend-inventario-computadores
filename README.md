# 🖥️ InvCompu API

Backend REST API para la gestión de inventario de hardware y reservas de sala de computación, construida con **Django 6** y **Django REST Framework 3.16**.

---

## Tabla de contenidos

- [Descripción](#descripción)
- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Variables de entorno](#variables-de-entorno)
- [Base URL](#base-url)
- [Autenticación](#autenticación)
- [Rate Limiting](#rate-limiting)
- [Paginación](#paginación)
- [Códigos de respuesta](#códigos-de-respuesta)
- [Endpoints](#endpoints)
- [Documentación web](#documentación-web)

---

## Descripción

**InvCompu API** es el backend de una aplicación de gestión para laboratorios de computación. Expone **30 endpoints** organizados en 4 módulos:

| Módulo | Descripción | Endpoints |
|--------|-------------|----------|
| `inventario` | Tipos de dispositivos, equipos físicos y consumibles del laboratorio | 16 |
| `salapcs` | Profesores y reservas de uso de sala | 10 |
| `seguridad` | Registro, login y perfil de usuario con JWT | 3 |
| `dashboard` | Resumen semanal (equipos + reservas de la semana) | 1 |

---

## Tecnologías

| Componente | Tecnología |
|------------|-----------|
| Lenguaje | Python 3.13 |
| Framework | Django 6.0.3 |
| API | Django REST Framework 3.16.1 |
| Autenticación | JWT (python-jose, HS512, 24h) |
| Base de datos | SQLite (dev) / PostgreSQL (prod vía dj-database-url) |
| Archivos estáticos | WhiteNoise |
| CORS | django-cors-headers |
| Servidor producción | Gunicorn |

---

## Estructura del proyecto

```
backend/
├── backend/          # Configuración Django (settings, urls, wsgi)
├── inventario/       # App: Dispositivos + Equipos
├── salapcs/          # App: Profesores + Reservas de Sala
├── seguridad/        # App: Auth JWT (registro, login, perfil)
├── dashboard/        # App: Resumen semanal
├── doc/              # App: Documentación web interactiva
├── manage.py
├── requirements.txt
├── Procfile          # Gunicorn (producción)
└── runtime.txt       # Python 3.13
```

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd backend

# 2. Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env          # editar con tus valores

# 5. Aplicar migraciones
python manage.py migrate

# 6. Iniciar servidor de desarrollo
python manage.py runserver
```

---

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Django (usada también para firmar JWT) | `django-insecure-xxxxxx` |
| `DEBUG` | Modo de depuración | `True` |
| `DATABASE_URL` | URL de conexión PostgreSQL (si no se define, usa SQLite) | `postgres://user:pass@host/db` |
| `CORS_ALLOWED_ORIGINS` | Orígenes CORS permitidos (separados por coma) | `http://localhost:5173` |
| `CSRF_TRUSTED_ORIGINS` | Orígenes de confianza para CSRF | `http://localhost:5173` |
| `ALLOWED_HOSTS` | Hosts permitidos (separados por coma) | `localhost,127.0.0.1` |
| `BASE_URL` | URL base del servidor (para links de paginación) | `http://127.0.0.1:8000` |

---

## Base URL

Todas las rutas de la API están bajo el prefijo:

```
http://<host>/api/v1/
```

En desarrollo local: `http://127.0.0.1:8000/api/v1/`

---

## Autenticación

La API usa **JWT** (JSON Web Tokens) con el algoritmo **HS512**.

1. **Obtener token:** `POST /api/v1/seguridad/login` con `email` y `password`.
2. **Usar token:** Incluir en el header `Authorization` de cada petición protegida.

```
Authorization: Bearer eyJhbGciOiJIUzUxMiIs...
```

> **Nota:** El token debe enviarse con el prefijo `Bearer`.

**Roles:**

| Rol | Permisos |
|-----|----------|
| `profesor` | GET, POST, PUT en todos los módulos |
| `admin` | Todo lo anterior + DELETE |

---

## Rate Limiting

La API aplica throttling para proteger el servidor de uso excesivo.

| Tipo de cliente | Límite | Ventana | Identificador |
|-----------------|--------|---------|---------------|
| Anónimo (sin token) | **1 000 peticiones** | Por día | IP de origen |

> Las peticiones autenticadas no tienen límite configurado actualmente.

Al superar el límite se devuelve `429 Too Many Requests` con el header `Retry-After`.

---

## Paginación

Los listados devuelven resultados paginados con la siguiente estructura:

```json
{
  "links": { "next": "...?page=2", "previous": null },
  "items": 25,
  "status": "ok",
  "page": "1/3",
  "data": [ ... ]
}
```

| Módulo | Parámetro de tamaño | Predeterminado | Máximo |
|--------|---------------------|----------------|--------|
| `inventario` | `page_size` | 10 | 50 |
| `salapcs` | `Limit` | 20 | — |

---

## Códigos de respuesta

| Código | Significado |
|--------|-------------|
| `200` | Operación exitosa |
| `201` | Recurso creado exitosamente |
| `400` | Datos inválidos o incompletos |
| `401` | Token faltante, expirado o inválido |
| `403` | Permisos insuficientes (requiere admin) |
| `404` | Recurso no encontrado |
| `429` | Límite de peticiones superado (1000/día para usuarios anónimos) |
| `500` | Error interno del servidor |

---

## Endpoints

### Inventario — Dispositivos

| Método | Ruta | Descripción | Acceso |
|--------|------|-------------|--------|
| `GET` | `/api/v1/dispositivos` | Listar dispositivos (paginado) | 🔒 login |
| `POST` | `/api/v1/dispositivos` | Crear dispositivo | 🔒 login |
| `GET` | `/api/v1/dispositivos/{id}` | Obtener dispositivo por ID | 🔒 login |
| `PUT` | `/api/v1/dispositivos/{id}` | Actualizar dispositivo | 🔒 login |
| `DELETE` | `/api/v1/dispositivos/{id}` | Eliminar dispositivo | 🛡️ admin |

### Inventario — Equipos

| Método | Ruta | Descripción | Acceso |
|--------|------|-------------|--------|
| `GET` | `/api/v1/equipos` | Listar equipos (paginado) | 🔒 login |
| `POST` | `/api/v1/equipos` | Registrar equipo | 🔒 login |
| `GET` | `/api/v1/equipos/{id}` | Obtener equipo por ID | 🔒 login |
| `PUT` | `/api/v1/equipos/{id}` | Actualizar equipo | 🔒 login |
| `DELETE` | `/api/v1/equipos/{id}` | Eliminar equipo | 🛡️ admin |
| `GET` | `/api/v1/equipos/dispositivo/{id}` | Equipos por tipo de dispositivo | 🔒 login |

### Inventario — Consumibles

| Método | Ruta | Descripción | Acceso |
|--------|------|-------------|--------|
| `GET` | `/api/v1/consumibles` | Listar consumibles (paginado) | 🔒 login |
| `POST` | `/api/v1/consumibles` | Crear consumible | 🔒 login |
| `GET` | `/api/v1/consumibles/{id}` | Obtener consumible por ID | 🔒 login |
| `PUT` | `/api/v1/consumibles/{id}` | Actualizar consumible | 🔒 login |
| `DELETE` | `/api/v1/consumibles/{id}` | Eliminar consumible | 🛡️ admin |

### Sala de PCs — Profesores

| Método | Ruta | Descripción | Acceso |
|--------|------|-------------|--------|
| `GET` | `/api/v1/profesores` | Listar profesores (paginado) | 🔒 login |
| `POST` | `/api/v1/profesores` | Registrar profesor | 🔒 login |
| `GET` | `/api/v1/profesores/{id}` | Obtener profesor por ID | 🔒 login |
| `PUT` | `/api/v1/profesores/{id}` | Actualizar profesor | 🔒 login |
| `DELETE` | `/api/v1/profesores/{id}` | Eliminar profesor | 🛡️ admin |

### Sala de PCs — Reservas

| Método | Ruta | Descripción | Acceso |
|--------|------|-------------|--------|
| `GET` | `/api/v1/salapcs` | Listar reservas (paginado) | 🔒 login |
| `POST` | `/api/v1/salapcs` | Crear reserva | 🔒 login |
| `GET` | `/api/v1/salapcs/{id}` | Obtener reserva por ID | 🔒 login |
| `PUT` | `/api/v1/salapcs/{id}` | Actualizar reserva | 🔒 login |
| `DELETE` | `/api/v1/salapcs/{id}` | Eliminar reserva | 🛡️ admin |

### Seguridad

| Método | Ruta | Descripción | Acceso |
|--------|------|-------------|--------|
| `POST` | `/api/v1/seguridad/reg` | Registrar usuario | 🌐 público |
| `POST` | `/api/v1/seguridad/login` | Iniciar sesión (obtener JWT) | 🌐 público |
| `GET` | `/api/v1/seguridad/perfil` | Perfil del usuario autenticado | 🔒 login |

### Dashboard

| Método | Ruta | Descripción | Acceso |
|--------|------|-------------|--------|
| `GET` | `/api/v1/dashboard/` | Resumen semanal del sistema | 🔒 login |

---

## Documentación web

La API incluye una interfaz de documentación HTML interactiva accesible en:

**Producción:**
```
https://backend-inventario-computadores-production.up.railway.app/docs/
```

**Desarrollo local:**
```
http://127.0.0.1:8000/docs/
```

| Ruta | Contenido |
|------|----------|
| `/docs/` | Página principal: overview, paginación y códigos HTTP |
| `/docs/inventario/` | Documentación del módulo Inventario |
| `/docs/salapcs/` | Documentación del módulo Sala de PCs |
| `/docs/seguridad/` | Documentación del módulo Seguridad |
| `/docs/dashboard/` | Documentación del módulo Dashboard |

```json
{
  "links": {
    "next":     "http://127.0.0.1:8000/api/v1/dispositivos?page=2",
    "previous": null
  },
  "items":  42,
  "status": "ok",
  "page":   "1/5",
  "data":   [ ... ]
}
```

### Parámetros de consulta

| Parámetro | Tipo | Predeterminado | Descripción |
|-----------|------|----------------|-------------|
| `page` | integer | 1 | Número de página. |
| `page_size` / `Limit` | integer | 10 (inventario) / 20 (salapcs) | Registros por página (máx. 100). |

---

## Códigos de respuesta

| Código | Significado | Descripción |
|--------|-------------|-------------|
| `200 OK` | Éxito | GET, PUT y DELETE exitosos. |
| `201 Created` | Recurso creado | POST exitoso. |
| `400 Bad Request` | Error de validación | Los datos no pasaron la validación. |
| `401 Unauthorized` | Sin autorización | Token JWT ausente, inválido o expirado. |
| `403 Forbidden` | Permisos insuficientes | El usuario no tiene rol admin (DELETE). |
| `404 Not Found` | No encontrado | El recurso no existe. |

**Estructura de error (400):**

```json
{
  "status":  "error",
  "message": "Error de validación",
  "errors": {
    "campo": ["Este campo es obligatorio."]
  }
}
```

---

## Módulo Inventario

### Modelos

#### `Dispositivo` — tabla `dispositivo`

| Campo | Tipo | Constraint | Descripción |
|-------|------|------------|-------------|
| `id` | integer | auto | Clave primaria. |
| `name` | string(100) | requerido, único | Nombre del tipo de dispositivo. |
| `descripcion` | text | opcional | Descripción detallada. |

#### `Equipo` — tabla `equipo`

| Campo | Tipo | Constraint | Descripción |
|-------|------|------------|-------------|
| `id` | integer | auto | Clave primaria. |
| `dispositivo` | FK → Dispositivo | requerido | Tipo al que pertenece (CASCADE). |
| `marca` | string(100) | opcional | Marca del fabricante. |
| `modelo` | string(100) | opcional | Modelo específico. |
| `identificador` | string(100) | requerido, único | Código o número de serie. |
| `estacion` | integer | requerido, único | Número de estación de trabajo. |
| `descripcion` | text | opcional | Notas adicionales. |
| `date_reg` | date | requerido | Fecha de ingreso. Formato: `YYYY-MM-DD`. |
| `is_active` | boolean | opcional | Indica si el equipo está activo. Predeterminado: `true`. |

#### `Consumible` — tabla `consumible`

| Campo | Tipo | Constraint | Descripción |
|-------|------|------------|-------------|
| `id` | integer | auto | Clave primaria. |
| `name` | string(100) | requerido, único | Nombre del consumible. |
| `cantidad` | integer | opcional | Stock disponible. Predeterminado: `0`. |
| `descripcion` | text | opcional | Descripción o notas adicionales. |

---

### Dispositivos

#### `GET /api/v1/dispositivos`
Lista todos los dispositivos ordenados por `-id`, paginado.

**Respuesta 200:**
```json
{
  "links": { "next": null, "previous": null },
  "items": 15,
  "status": "ok",
  "page": "1/2",
  "data": [
    { "id": 3, "name": "Computadora de Escritorio", "descripcion": "PC con torre ATX" }
  ]
}
```

---

#### `POST /api/v1/dispositivos`
Crea un nuevo tipo de dispositivo.

**Body:**
```json
{ "name": "Monitor", "descripcion": "Pantalla LED 24 pulgadas" }
```

**Respuesta 201:**
```json
{ "status": "ok", "message": "Registro creado exitosamente" }
```

---

#### `GET /api/v1/dispositivos/{id}`
Retorna el detalle de un dispositivo.

**Respuesta 200:**
```json
{ "status": "ok", "data": { "id": 1, "name": "Monitor", "descripcion": "Pantalla LED 24 pulgadas" } }
```

---

#### `PUT /api/v1/dispositivos/{id}`
Actualización completa de un dispositivo. Requiere todos los campos.

**Respuesta 200:**
```json
{ "status": "ok", "message": "Registro actualizado exitosamente" }
```

---

#### `DELETE /api/v1/dispositivos/{id}`
Elimina un dispositivo y **todos los equipos asociados** (CASCADE).

**Respuesta 200:**
```json
{ "status": "ok", "message": "Registro eliminado exitosamente" }
```

---

### Equipos

#### `GET /api/v1/equipos`
Lista todos los equipos, paginado.

**Respuesta 200 — campo `data`:**
```json
{
  "id": 1,
  "dispositivo": 2,
  "dispositivo_name": "Computadora de Escritorio",
  "marca": "Dell",
  "modelo": "OptiPlex 7090",
  "identificador": "SN-001-DELL",
  "estacion": 1,
  "descripcion": null,
  "date_reg": "2024-03-15",
  "is_active": true
}
```

---

#### `POST /api/v1/equipos`
Registra un nuevo equipo.

**Body:**
```json
{
  "dispositivo":   1,
  "marca":         "HP",
  "modelo":        "ProDesk 400 G7",
  "identificador": "INV-2024-015",
  "estacion":      15,
  "descripcion":   "Equipo con SSD 512GB",
  "date_reg":      "2024-09-01"
}
```

**Respuesta 201:**
```json
{ "status": "ok", "data": "registro creado correctamente" }
```

---

#### `GET /api/v1/equipos/{id}`
Retorna el detalle de un equipo.

---

#### `PUT /api/v1/equipos/{id}`
Actualización completa de un equipo.

**Respuesta 200:**
```json
{ "status": "ok", "data": "registro actualizado correctamente" }
```

---

#### `DELETE /api/v1/equipos/{id}`
Elimina un equipo del inventario.

**Respuesta 200:**
```json
{ "status": "ok", "data": "registro eliminado correctamente" }
```

---

#### `GET /api/v1/equipos/dispositivo/{dispositivo_id}`
Lista los equipos filtrados por tipo de dispositivo, ordenados por `-id`, paginado.

---

### Consumibles

#### `GET /api/v1/consumibles`
Lista todos los consumibles ordenados por `-id`, paginado.

**Respuesta 200 — campo `data`:**
```json
{ "id": 1, "name": "Cable HDMI", "cantidad": 12, "descripcion": "Cables de repuesto para monitores" }
```

---

#### `POST /api/v1/consumibles`
Crea un nuevo consumible.

**Body:**
```json
{ "name": "Cable HDMI", "cantidad": 12, "descripcion": "Cables de repuesto para monitores" }
```

**Respuesta 201:**
```json
{ "status": "ok", "message": "Registro creado exitosamente" }
```

---

#### `GET /api/v1/consumibles/{id}`
Retorna el detalle de un consumible.

**Respuesta 200:**
```json
{ "status": "ok", "data": { "id": 1, "name": "Cable HDMI", "cantidad": 12, "descripcion": "Cables de repuesto para monitores" } }
```

---

#### `PUT /api/v1/consumibles/{id}`
Actualización completa de un consumible. Requiere todos los campos.

**Respuesta 200:**
```json
{ "status": "ok", "message": "Registro actualizado exitosamente" }
```

---

#### `DELETE /api/v1/consumibles/{id}`
Elimina un consumible del inventario. Requiere rol **admin**.

**Respuesta 200:**
```json
{ "status": "ok", "message": "Registro eliminado exitosamente" }
```

---

## Módulo Sala de PCs

### Modelos

#### `Profesor` — tabla `profesor`

| Campo | Tipo | Constraint | Descripción |
|-------|------|------------|-------------|
| `id` | integer | auto | Clave primaria. |
| `nombre` | string(100) | opcional | Nombre del profesor. |
| `apellido` | string(100) | opcional | Apellido del profesor. |
| `correo` | email | requerido | Correo electrónico válido. |
| `asignatura` | string(100) | requerido | Asignatura que imparte. |

#### `SalaPC` — tabla `salapc`

| Campo | Tipo | Constraint | Descripción |
|-------|------|------------|-------------|
| `id` | integer | auto | Clave primaria. |
| `profesor` | FK → Profesor | requerido | Profesor que reserva (CASCADE). |
| `curso` | string(100) | requerido | Curso que usará la sala (ej. `3°B`). |
| `asignatura` | string(100) | requerido | Asignatura de la sesión. |
| `date` | date | requerido | Fecha de uso. Formato: `YYYY-MM-DD`. |
| `hour` | time | requerido | Hora de inicio. Formato: `HH:MM:SS`. |

---

### Profesores

#### `GET /api/v1/profesores`
Lista todos los profesores, paginado. Usa el parámetro `Limit` para el tamaño de página.

**Respuesta 200 — campo `data`:**
```json
{ "nombre": "Carlos", "apellido": "González", "correo": "cgonzalez@colegio.cl", "asignatura": "Tecnología e Informática" }
```

---

#### `POST /api/v1/profesores`
Registra un nuevo profesor.

**Body:**
```json
{ "nombre": "Ana", "apellido": "Martínez", "correo": "amartinez@colegio.cl", "asignatura": "Matemáticas" }
```

**Respuesta 201:**
```json
{ "status": "ok", "message": "Profesor creado exitosamente" }
```

---

#### `GET /api/v1/profesores/{id}`
Retorna el detalle de un profesor.

---

#### `PUT /api/v1/profesores/{id}`
Actualización completa de un profesor.

**Respuesta 200:**
```json
{ "status": "ok", "message": "Profesor actualizado exitosamente" }
```

---

#### `DELETE /api/v1/profesores/{id}`
Elimina un profesor y **todas sus reservas de sala** (CASCADE).

**Respuesta 200:**
```json
{ "status": "ok", "message": "Profesor eliminado correctamente" }
```

---

### Reservas de Sala (SalaPC)

#### `GET /api/v1/salapcs`
Lista todas las reservas, paginado.

**Respuesta 200 — campo `data`:**
```json
{
  "profesor":      3,
  "profesor_name": "Ana",
  "curso":         "3°B",
  "asignatura":    "Tecnología",
  "date":          "2026-04-01",
  "hour":          "10:00:00"
}
```

---

#### `POST /api/v1/salapcs`
Registra una nueva reserva de sala.

**Body:**
```json
{
  "profesor":   3,
  "curso":      "3°B",
  "asignatura": "Tecnología",
  "date":       "2026-04-01",
  "hour":       "10:00:00"
}
```

**Respuesta 201:**
```json
{ "status": "ok", "message": "Reserva de sala creada exitosamente" }
```

---

#### `GET /api/v1/salapcs/{id}`
Retorna el detalle de una reserva.

---

#### `PUT /api/v1/salapcs/{id}`
Actualización completa de una reserva. Todos los campos son requeridos.

**Respuesta 200:**
```json
{ "status": "ok", "message": "Reserva de sala actualizada exitosamente" }
```

---

#### `DELETE /api/v1/salapcs/{id}`
Elimina una reserva de sala.

**Respuesta 200:**
```json
{ "status": "ok", "message": "Reserva de sala eliminada correctamente" }
```

---
