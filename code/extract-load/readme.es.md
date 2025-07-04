# Extractor de Datos de Mediotiempo

Una herramienta de extracción y carga de datos basada en Python, diseñada para recolectar datos de partidos de fútbol desde la API de Mediotiempo y almacenarlos en una base de datos PostgreSQL.

Este proyecto forma parte de un pipeline de ingeniería de datos más amplio para análisis deportivos.

## 🎯 Propósito

Este extractor está diseñado específicamente para:

- Obtener datos de partidos de torneos regulares desde la API pública de Mediotiempo
- Manejar la extracción incremental de datos, rastreando la última temporada, liga y jornada procesadas

## 🛠️ Tecnologías Utilizadas

### Tecnologías Principales

- **Python 3.11+** - Lenguaje de programación principal
- **PostgreSQL** - Base de datos destino para almacenamiento
- **psycopg2-binary** - Adaptador de PostgreSQL para Python
- **requests** - Librería HTTP para interacción con APIs

## 📦 Estructura del Proyecto

```text
src/
├── mediotiempo_data/
│   ├── __init__.py              # Punto de entrada principal
│   ├── database_interactions.py # Conexión y operaciones con PostgreSQL
│   └── torneo_regular_resolver.py # Lógica de progreso de torneos
├── tests/                   # Conjunto de pruebas
├── Dockerfile              # Configuración del contenedor
├── pyproject.toml          # Metadatos del proyecto y dependencias
└── uv.lock                 # Versiones bloqueadas de dependencias
```

## 🔧 Componentes Clave

### 1. Aplicación Principal (`__init__.py`)

- Orquesta el proceso de extracción de datos
- Administra conexiones a la base de datos y solicitudes a la API
- Maneja la transformación e inserción de datos

### 2. Interacciones con la Base de Datos (`database_interactions.py`)

- **`get_max_values()`** - Recupera la última temporada, liga y jornada procesadas
- **`insert_data()`** - Inserta en bloque los datos de partidos en la tabla de aterrizaje

### 3. Resolución de Torneo (`torneo_regular_resolver.py`)

- Administra la lógica de progreso del torneo
- Maneja las transiciones de temporada (Clausura → Apertura → siguiente año)
- Soporta las ligas 385 (Clausura) y 199 (Apertura)

## 🚀 Primeros Pasos

### Requisitos Previos

- Python 3.11 o superior
- Base de datos PostgreSQL
- Docker (opcional, para despliegue en contenedor)

### Variables de Entorno

La aplicación requiere las siguientes variables de entorno:

```bash
DB_HOST=tu_host_postgres
DB_PORT=tu_puerto_postgres
DB_DATABASE=tu_nombre_base_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
```

## 📊 Esquema de Datos

El extractor llena la tabla `landing_mediotiempo_torneo_regular` con la siguiente estructura:

| Campo | Descripción |
|-------|-------------|
| season_id | Año del torneo |
| league_id | Identificador de liga (385=Clausura, 199=Apertura) |
| round_id | Número de jornada dentro del torneo |
| league_id_config | ID de liga según configuración de la API |
| league_name | Nombre de la liga |
| league_label | Etiqueta para mostrar de la liga |
| league_image | URL del logo de la liga |
| season_id_config | ID de temporada según configuración de la API |
| season_name | Nombre de la temporada |
| season_label | Etiqueta de la temporada |
| season_round_id | ID de la jornada de la temporada |
| season_round_name | Nombre de la jornada de la temporada |
| season_round_label | Etiqueta de la jornada de la temporada |
| round_id_config | ID de la jornada según configuración de la API |
| round_name | Nombre de la jornada |
| round_label | Etiqueta de la jornada |
| match_id | Identificador único del partido |
| match_date | Fecha y hora del partido |
| home_team_id | ID del equipo local |
| home_team_name | Nombre del equipo local |
| home_team_logo | URL del logo del equipo local |
| home_team_logo_large | URL del logo grande del equipo local |
| away_team_id | ID del equipo visitante |
| away_team_name | Nombre del equipo visitante |
| away_team_logo | URL del logo del equipo visitante |
| away_team_logo_large | URL del logo grande del equipo visitante |
| match_status | Estado del partido (por ejemplo, "finished", "scheduled") |
| home_score | Marcador del equipo local |
| home_shootout | Marcador en penales del equipo local (si aplica) |
| away_score | Marcador del equipo visitante |
| away_shootout | Marcador en penales del equipo visitante (si aplica) |
| venue_id | ID del estadio |
| venue_stadium | Nombre del estadio |
| venue_city | Ciudad del estadio |

## 🔄 Procesamiento Incremental

La aplicación implementa un procesamiento incremental inteligente:

1. Consulta la base de datos para encontrar la última temporada, liga y jornada procesadas
2. Comienza la extracción desde el siguiente punto lógico en la progresión del torneo
3. Continúa hasta alcanzar la temporada máxima (2025) o hasta que no haya más datos disponibles
4. Maneja automáticamente las transiciones de torneo (Clausura → Apertura → siguiente año)

## 🧪 Pruebas

Ejecuta la suite de pruebas:

```bash
uv run pytest tests/
```
