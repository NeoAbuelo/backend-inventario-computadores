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
- [Módulo Inventario](#módulo-inventario)
- [Módulo Sala de PCs](#módulo-sala-de-pcs)
- [Módulo Dashboard](#módulo-dashboard)
- [Reportes PDF](#reportes-pdf)
- [Documentación web](#documentación-web)

---

## Descripción

**InvCompu API** es el backend de una aplicación de gestión para laboratorios de computación. Está organizada en módulos:

| Módulo | Descripción |
|--------|-------------|
| `inventario` | Tipos de dispositivos, equipos físicos y consumibles del laboratorio |
| `salapcs` | Profesores y reservas de uso de sala |
| `dashboard` | Resumen semanal (conteo de equipos, consumibles con bajo stock y reservas de la semana) |
| `doc` | Documentación web HTML interactiva (`/docs/`) |

> **Nota:** Esta versión **no incluye autenticación**. La app `seguridad` (login/registro/perfil con JWT) fue retirada del proyecto; todos los endpoints son de acceso público. Ver [Autenticación](#autenticación).

---

## Tecnologías

| Componente | Tecnología |
|------------|-----------|
| Lenguaje | Python 3.13 |
| Framework | Django 6.0.3 |
| API | Django REST Framework 3.16.1 |
| Base de datos | SQLite (activa) / PostgreSQL (opcional vía dj-database-url) |
| Reportes PDF | reportlab |
| Archivos estáticos | WhiteNoise |
| CORS | django-cors-headers |
| Utilidades dev | django-extensions, django-seed |
| Servidor producción | Gunicorn |

---

## Estructura del proyecto

```
backend/
├── backend/          # Configuración Django (settings, urls, wsgi, asgi)
├── inventario/       # App: Dispositivos + Equipos + Consumibles
│   └── views/        # Vistas por recurso + paginación + reporte PDF
├── salapcs/          # App: Profesores + Reservas de Sala
│   └── views/        # Vistas por recurso + paginación + reporte PDF
├── dashboard/        # App: Resumen semanal
├── doc/              # App: Documentación web interactiva
├── manage.py
├── pyproject.toml    # Dependencias (uv) + uv.lock
├── requirements.txt  # Dependencias (pip)
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

# 3. Instalar dependencias (pip o uv)
pip install -r requirements.txt
# o bien:  uv sync

# 4. Configurar variables de entorno
cp .env.example .env          # editar con tus valores

# 5. Aplicar migraciones
python manage.py migrate

# 6. (Opcional) Poblar datos de prueba
python manage.py seed inventario --number=20

# 7. Iniciar servidor de desarrollo
python manage.py runserver
```

---

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Django | `django-insecure-xxxxxx` |
| `DEBUG` | Modo de depuración (`True` para activarlo) | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos (separados por coma) | `localhost,127.0.0.1` |

> La base de datos por defecto es **SQLite** (`db.sqlite3`). Para usar PostgreSQL hay que descomentar la línea `dj_database_url.config(...)` en `backend/settings.py` y definir `DATABASE_URL`.
>
> Los orígenes CORS permitidos están fijados en `settings.py` (`CORS_ALLOWED_ORIGINS`) a `http://localhost:5173` y `http://127.0.0.1:5173`.

---

## Base URL

Todas las rutas de la API están bajo el prefijo:

```
http://<host>/api/v1/
```

En desarrollo local: `http://127.0.0.1:8000/api/v1/`

---

## Autenticación

⚠️ **Actualmente la API no implementa autenticación ni autorización.** Todos los endpoints son públicos y no requieren token ni roles. No hay distinción entre usuarios `profesor` y `admin`; cualquier cliente puede ejecutar operaciones de lectura y escritura (incluyendo `DELETE`).

---

## Rate Limiting

La API aplica throttling de DRF para clientes anónimos.

| Tipo de cliente | Límite | Ventana | Identificador |
|-----------------|--------|---------|---------------|
| Anónimo | **100 peticiones** | Por día | IP de origen |

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
| `salapcs` | `Limit` | 20 | 100 |

El número de página se controla con el parámetro `page`.

---

## Códigos de respuesta

| Código | Significado | Descripción |
|--------|-------------|-------------|
| `200 OK` | Éxito | GET, PUT y DELETE exitosos. |
| `201 Created` | Recurso creado | POST exitoso. |
| `400 Bad Request` | Error de validación | Los datos no pasaron la validación. |
| `404 Not Found` | No encontrado | El recurso no existe. |
| `409 Conflict` | Conflicto de recurso | La operación choca con el estado actual (ej.: reservar la sala en una fecha y hora ya ocupadas). |
| `429 Too Many Requests` | Límite superado | 100 peticiones/día para clientes anónimos. |
| `500 Internal Server Error` | Error interno | Error inesperado en el servidor. |

**Estructura de error de validación (400):**

```json
{
  "status":  "error",
  "message": "error de validación",
  "errors": {
    "campo": ["Este campo es obligatorio."]
  }
}
```

> El formato exacto del cuerpo de error varía ligeramente entre módulos (algunos usan `message` con los errores y otros una clave `error`/`errors`), pero siempre incluye `status: "error"`.

---

## Endpoints

### Inventario — Dispositivos

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/dispositivos` | Listar dispositivos (paginado, orden `-id`) |
| `POST` | `/api/v1/dispositivos` | Crear dispositivo |
| `GET` | `/api/v1/dispositivos/{id}` | Obtener dispositivo por ID |
| `PUT` | `/api/v1/dispositivos/{id}` | Actualizar dispositivo |
| `DELETE` | `/api/v1/dispositivos/{id}` | Eliminar dispositivo (CASCADE sobre equipos) |

### Inventario — Equipos

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/equipos` | Listar equipos (paginado, orden por `estacion`) |
| `POST` | `/api/v1/equipos` | Registrar equipo |
| `GET` | `/api/v1/equipos/pdf` | Descargar reporte PDF del inventario |
| `GET` | `/api/v1/equipos/{id}` | Obtener equipo por ID |
| `PUT` | `/api/v1/equipos/{id}` | Actualizar equipo |
| `DELETE` | `/api/v1/equipos/{id}` | Eliminar equipo |
| `GET` | `/api/v1/equipos/dispositivo/{id}` | Equipos por tipo de dispositivo (paginado) |

### Inventario — Consumibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/consumibles` | Listar consumibles **con bajo stock** (paginado, ver nota) |
| `POST` | `/api/v1/consumibles` | Crear consumible |
| `GET` | `/api/v1/consumibles/{id}` | Obtener consumible por ID |
| `PUT` | `/api/v1/consumibles/{id}` | Actualizar consumible |
| `DELETE` | `/api/v1/consumibles/{id}` | Eliminar consumible |

### Sala de PCs — Profesores

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/profesores` | Listar profesores (paginado) |
| `POST` | `/api/v1/profesores` | Registrar profesor |
| `GET` | `/api/v1/profesores/{id}` | Obtener profesor por ID |
| `PUT` | `/api/v1/profesores/{id}` | Actualizar profesor |
| `DELETE` | `/api/v1/profesores/{id}` | Eliminar profesor (CASCADE sobre reservas) |

### Sala de PCs — Reservas

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/salapcs` | Listar reservas (paginado) |
| `POST` | `/api/v1/salapcs` | Crear reserva |
| `GET` | `/api/v1/salapcs/{id}` | Obtener reserva por ID |
| `PUT` | `/api/v1/salapcs/{id}` | Actualizar reserva |
| `DELETE` | `/api/v1/salapcs/{id}` | Eliminar reserva |
| `GET` | `/api/v1/salapcs/reportes/horario` | Descargar reporte PDF del horario semanal |

### Dashboard

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/dashboard/` | Resumen semanal del sistema |

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
| `identificador` | string(100) | autogenerado, único, solo lectura | Código generado por el servidor con formato `ccpNNNN`. **No se envía en el body.** |
| `estacion` | integer | requerido | Número de estación de trabajo. |
| `is_active` | boolean | opcional | Indica si el equipo está activo. Predeterminado: `true`. |
| `descripcion` | text | opcional | Notas adicionales. |
| `date_reg` | date | auto, solo lectura | Fecha de ingreso (`auto_now_add`). |

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

**Respuesta 200 — campo `data`:**
```json
{ "id": 3, "name": "Computadora de Escritorio", "descripcion": "PC con torre ATX" }
```

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

#### `GET /api/v1/dispositivos/{id}`
```json
{ "status": "ok", "data": { "id": 1, "name": "Monitor", "descripcion": "Pantalla LED 24 pulgadas" } }
```

#### `PUT /api/v1/dispositivos/{id}`
Actualización completa. Requiere todos los campos.
```json
{ "status": "ok", "message": "Registro actualizado exitosamente" }
```

#### `DELETE /api/v1/dispositivos/{id}`
Elimina el dispositivo y **todos los equipos asociados** (CASCADE).
```json
{ "status": "ok", "message": "Registro eliminado exitosamente" }
```

---

### Equipos

#### `GET /api/v1/equipos`
Lista todos los equipos ordenados por `estacion`, paginado.

**Respuesta 200 — campo `data`:**
```json
{
  "id": 1,
  "dispositivo": 2,
  "dispositivo_name": "Computadora de Escritorio",
  "marca": "Dell",
  "modelo": "OptiPlex 7090",
  "identificador": "ccp0001",
  "estacion": 1,
  "descripcion": null,
  "date_reg": "2024-03-15",
  "is_active": true
}
```

#### `POST /api/v1/equipos`
Registra un nuevo equipo. **`identificador` y `date_reg` se generan automáticamente**, no los envíes.

**Body:**
```json
{
  "dispositivo":   1,
  "marca":         "HP",
  "modelo":        "ProDesk 400 G7",
  "estacion":      15,
  "descripcion":   "Equipo con SSD 512GB",
  "is_active":     true
}
```
**Respuesta 201:**
```json
{ "status": "ok", "data": "registro creado correctamente" }
```

#### `GET /api/v1/equipos/{id}`
Retorna el detalle de un equipo (`{ "status": "ok", "data": { ... } }`).

#### `PUT /api/v1/equipos/{id}`
```json
{ "status": "ok", "data": "registro actualizado correctamente" }
```

#### `DELETE /api/v1/equipos/{id}`
```json
{ "status": "ok", "data": "registro eliminado correctamente" }
```

#### `GET /api/v1/equipos/dispositivo/{dispositivo_id}`
Lista los equipos filtrados por tipo de dispositivo, orden `-id`, paginado.

---

### Consumibles

#### `GET /api/v1/consumibles`
Lista consumibles paginado, orden de inserción.

> ⚠️ **Importante:** este listado **solo devuelve los consumibles con `cantidad <= 3`** (alerta de bajo stock). Para acceder a un consumible con stock alto, usa su endpoint de detalle por ID.

**Respuesta 200 — campo `data`:**
```json
{ "id": 1, "name": "Cable HDMI", "cantidad": 2, "descripcion": "Cables de repuesto para monitores" }
```

#### `POST /api/v1/consumibles`
**Body:**
```json
{ "name": "Cable HDMI", "cantidad": 12, "descripcion": "Cables de repuesto para monitores" }
```
**Respuesta 201:**
```json
{ "status": "ok", "message": "Registro creado exitosamente" }
```

#### `GET /api/v1/consumibles/{id}`
```json
{ "status": "ok", "data": { "id": 1, "name": "Cable HDMI", "cantidad": 12, "descripcion": "Cables de repuesto para monitores" } }
```

#### `PUT /api/v1/consumibles/{id}`
```json
{ "status": "ok", "message": "Registro actualizado exitosamente" }
```

#### `DELETE /api/v1/consumibles/{id}`
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

> **Horario único:** la combinación `(date, hour)` es **única** (`unique_together`). No se puede registrar dos reservas en la misma fecha y hora; al intentarlo la API devuelve `409 Conflict`.
>
> **Franjas horarias (frontend):** el formulario de agendamiento acota la hora de inicio a tramos de **30 minutos, de 08:00 a 17:00**. El backend acepta cualquier `HH:MM:SS` válido; la restricción de tramos se aplica solo en la interfaz.

---

### Profesores

#### `GET /api/v1/profesores`
Lista profesores, paginado (tamaño con `Limit`).

**Respuesta 200 — campo `data`:**
```json
{ "id": 1, "nombre": "Carlos", "apellido": "González", "correo": "cgonzalez@colegio.cl", "asignatura": "Tecnología e Informática" }
```

#### `POST /api/v1/profesores`
**Body:**
```json
{ "nombre": "Ana", "apellido": "Martínez", "correo": "amartinez@colegio.cl", "asignatura": "Matemáticas" }
```
**Respuesta 201:**
```json
{ "status": "ok", "message": "Profesor creado exitosamente" }
```

#### `GET /api/v1/profesores/{id}`
Retorna el detalle de un profesor.

#### `PUT /api/v1/profesores/{id}`
```json
{ "status": "ok", "message": "Profesor actualizado exitosamente" }
```

#### `DELETE /api/v1/profesores/{id}`
Elimina el profesor y **todas sus reservas** (CASCADE).
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
  "id": 5,
  "profesor":      3,
  "profesor_name": "Ana",
  "curso":         "3°B",
  "asignatura":    "Tecnología",
  "date":          "2026-04-01",
  "hour":          "10:00:00"
}
```

#### `POST /api/v1/salapcs`
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

**Respuesta 409 — fecha y hora ya ocupadas:**
```json
{ "status": "error", "message": "Ya existe una reserva para esa fecha y hora. Elige otro horario." }
```

#### `GET /api/v1/salapcs/{id}`
Retorna el detalle de una reserva.

#### `PUT /api/v1/salapcs/{id}`
```json
{ "status": "ok", "message": "Reserva de sala actualizada exitosamente" }
```

> Al igual que el POST, si se cambia la reserva a una `date` y `hour` ya ocupadas por **otra** reserva, la API responde `409 Conflict` con el mismo mensaje.

#### `DELETE /api/v1/salapcs/{id}`
```json
{ "status": "ok", "message": "Reserva de sala eliminada correctamente" }
```

---

## Módulo Dashboard

#### `GET /api/v1/dashboard/`
Devuelve un resumen del estado actual y las reservas de la **semana en curso** (lunes a domingo, según la zona horaria `America/Santiago`).

**Respuesta 200:**
```json
{
  "numero_equipos": 42,
  "numero_consumibles_0": 3,
  "salas": [
    {
      "id": 5,
      "profesor": 3,
      "profesor_name": "Ana",
      "curso": "3°B",
      "asignatura": "Tecnología",
      "date": "2026-04-01",
      "hour": "10:00:00"
    }
  ]
}
```

| Campo | Descripción |
|-------|-------------|
| `numero_equipos` | Total de equipos registrados. |
| `numero_consumibles_0` | Consumibles con stock **bajo** (`cantidad <= 3`). |
| `salas` | Reservas de la semana actual, ordenadas por fecha y hora. |

---

## Reportes PDF

Dos endpoints generan reportes descargables (`Content-Disposition: attachment`) con **reportlab**:

| Ruta | Archivo | Contenido |
|------|---------|-----------|
| `GET /api/v1/equipos/pdf` | `reporte_tabla.pdf` | Tabla completa del inventario de equipos a la fecha. |
| `GET /api/v1/salapcs/reportes/horario` | `reporte_horario.pdf` | Horario de uso de la sala de la semana en curso. |

---

## Documentación web

La API incluye una interfaz de documentación HTML interactiva (app `doc`, templates Django):

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
| `/docs/dashboard/` | Documentación del módulo Dashboard |
| `/docs/seguridad/` | Página heredada del módulo de seguridad (la API ya no expone autenticación) |
