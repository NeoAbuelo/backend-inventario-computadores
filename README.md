# 🖥️ InvCompu API

Sistema de **Inventario y Gestión de Sala de Computación** — Backend REST API construida con Django 5 y Django REST Framework.

---

## Tabla de contenidos

- [Descripción](#descripción)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Variables de entorno](#variables-de-entorno)
- [Base URL y estructura de respuesta](#base-url-y-estructura-de-respuesta)
- [Paginación](#paginación)
- [Códigos de respuesta](#códigos-de-respuesta)
- [Módulo Inventario](#módulo-inventario)
  - [Dispositivos](#dispositivos)
  - [Equipos](#equipos)
- [Módulo Sala de PCs](#módulo-sala-de-pcs)
  - [Profesores](#profesores)
  - [Reservas de Sala (SalaPC)](#reservas-de-sala-salapc)
- [Documentación web](#documentación-web)

---

## Descripción

**InvCompu API** es el backend de una aplicación para gestionar el inventario de hardware y el uso de un laboratorio de computación. Expone dos módulos principales:

| Módulo | Descripción |
|--------|-------------|
| `inventario` | Gestión de tipos de dispositivos y equipos físicos del laboratorio. |
| `salapcs` | Gestión de profesores y reservas de uso de la sala. |

---

## Tecnologías

- Python 3.x
- Django 5
- Django REST Framework
- SQLite (desarrollo)
- python-dotenv

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

# 4. Configurar variables de entorno (ver sección siguiente)
cp .env.example .env

# 5. Aplicar migraciones
python manage.py migrate

# 6. Iniciar servidor de desarrollo
python manage.py runserver
```

---

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes claves:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Django | `django-insecure-...` |
| `DEBUG` | Modo de depuración | `True` |

---

## Base URL y estructura de respuesta

Todas las rutas de la API están bajo el prefijo:

```
http://<host>/api/v1/
```

En desarrollo local: `http://127.0.0.1:8000/api/v1/`

---

## Paginación

Todos los listados devuelven resultados paginados. La estructura de respuesta es:

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
| `200 OK` | Éxito | GET y PUT exitosos. |
| `201 Created` | Recurso creado | POST exitoso. |
| `204 No Content` | Sin contenido | DELETE en algunos endpoints. |
| `400 Bad Request` | Error de validación | Los datos no pasaron la validación. |
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
  "date_reg": "2024-03-15"
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
{ "status": "ok", "message": "SalaPC created successfully" }
```

---

#### `GET /api/v1/salapcs/{id}`
Retorna el detalle de una reserva.

---

#### `PUT /api/v1/salapcs/{id}`
Actualización completa de una reserva. Todos los campos son requeridos.

**Respuesta 200:**
```json
{ "status": "ok", "message": "SalaPC updated successfully" }
```

---

#### `DELETE /api/v1/salapcs/{id}`
Elimina una reserva de sala.

**Respuesta 204:**
```json
{ "status": "ok", "message": "SalaPC deleted successfully" }
```

---

## Documentación web

La API incluye una interfaz de documentación HTML accesible en:

```
http://127.0.0.1:8000/docs/
```

| Ruta | Contenido |
|------|-----------|
| `/docs/` | Página principal: overview, paginación y códigos HTTP |
| `/docs/inventario/` | Documentación del módulo Inventario |
| `/docs/salapcs/` | Documentación del módulo Sala de PCs |
