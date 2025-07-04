# r/dataengineering

> Un tutorial de ingeniería de datos

Este es un ejemplo *end to end* de un pipeline de ingeniería de datos.

## Flujo de trabajo

![Workflow](./docs/workflow.png)

El flujo de trabajo se compone de los siguientes pasos:

1. Extraer datos del sitio web de Mediotiempo  
2. Transformar los datos usando dbt  
3. Cargar los datos en una base de datos PostgreSQL

### Código

El código está organizado en las siguientes carpetas:

- `code/extract-load`: Contiene el código para la tarea de extracción y carga. Es un script en Python que extrae datos del sitio web de Mediotiempo y los almacena en una base de datos PostgreSQL.
- `code/transform`: Contiene el código para la tarea de transformación. Es un proyecto dbt que transforma los datos desde la base de datos PostgreSQL y los almacena en una nueva base de datos PostgreSQL.

## Infraestructura

El proyecto utiliza Docker Compose para configurar los siguientes servicios:

### Registro Docker (`registry:2`)

- Un registro Docker privado para almacenar imágenes personalizadas  
- Expuesto en el puerto `5001`

### Interfaz del Registro (`joxit/docker-registry-ui:main`)

- Interfaz web para administrar el registro Docker  
- Accesible en el puerto [8081](http://localhost:8081)  
- Características:
  - Capacidad para eliminar imágenes  
  - Muestra el digest del contenido  
  - Gestión de etiquetas  
  - Navegación del catálogo

### Base de Datos PostgreSQL (`postgres:14`)

- Servidor principal de base de datos  
- Expuesto en el puerto [5432](http://localhost:5432)  
- Incluye verificación de estado  
- Se inicializa con scripts SQL personalizados  
- Utilizado por Airflow y otros servicios

### SQLPad (`sqlpad/sqlpad:latest`)

- Interfaz web para consultas en bases de datos  
- Accesible en el puerto [3000](http://localhost:3000)  
- Utiliza la base de datos PostgreSQL  
- Soporta múltiples conexiones  
- Permite guardar consultas y resultados

### Apache Airflow

Se utiliza Apache Airflow versión 2.7.3 con dos componentes:

1. **Airflow Webserver** (`apache/airflow:2.7.3`)  
   - Interfaz web de Airflow  
   - Accesible en el puerto [8080](http://localhost:8080)  
   - Usa `LocalExecutor`  
   - Inicializa automáticamente la base de datos y crea un usuario administrador

2. **Airflow Scheduler** (`apache/airflow:2.7.3`)  
   - Se encarga de la programación y ejecución de DAGs  
   - Depende del servicio webserver  
   - Comparte la carpeta de DAGs con el webserver

### Docker dentro de Docker (`docker:dind`)

- Permite ejecutar contenedores Docker dentro de Docker  
- Expuesto en el puerto `2375`  
- Se ejecuta en modo privilegiado  
- Soporte para configuración personalizada del daemon

Todos los servicios están configurados para reiniciarse automáticamente y utilizan variables de entorno definidas en un archivo `.env` para su configuración.

### GitHub Actions

El proyecto utiliza GitHub Actions para construir y subir imágenes al registro Docker. Esto se realiza mediante **act**, una herramienta que permite ejecutar GitHub Actions localmente.

## Ejecutar el tutorial completo

Ejecuta toda la infraestructura con:

```bash
docker compose up --build
```

Ahora puedes acceder al servidor web de Airflow en [http://localhost:8080](http://localhost:8080), también puedes acceder a la interfaz del registro en [http://localhost:8081](http://localhost:8081) o incluso conectarte a la base de datos PostgreSQL con tu herramienta favorita.

El siguiente paso es ejecutar la acción de GitHub para construir las imágenes Docker correspondientes a las tareas en la carpeta `airflow/dags`.

Ejecutar la acción de GitHub es tan simple como correr:

```bash
act --container-architecture linux/amd64
```
