# r/dataengineering

 > A data engineering tutorial

This is an end-to-end showcase of a data engineering pipeline.

## Workflow

![Workflow](./docs/workflow.png)

The workflow is composed of the following steps:

1. Extract data from the Mediotiempo website
2. Transform the data using dbt
3. Load the data into a PostgreSQL database

### Code

The code is organized in the following folders:

- `code/extract-load`: Contains the code for the extract-load task. This is a Python script that extracts data from the Mediotiempo website and stores it in a PostgreSQL database.
- `code/transform`: Contains the code for the transform task. This is a dbt project that transforms the data from the PostgreSQL database and stores it in a new PostgreSQL database.

## Infrastructure

The project uses Docker Compose to set up the following services:

### Docker Registry (`registry:2`)

- A private Docker registry for storing custom images
- Exposed on port `5001`

### Registry UI (`joxit/docker-registry-ui:main`)

- Web interface for managing Docker registry
- Accessible on port [8081](http://localhost:8081)
- Features:
  - Image deletion capability
  - Content digest display
  - Tag management
  - Catalog browsing

### PostgreSQL Database (`postgres:14`)

- Main database server
- Exposed on port [5432](http://localhost:5432)
- Includes health checking
- Initializes with custom SQL scripts
- Used by Airflow and other services

### SQLPad (`sqlpad/sqlpad:latest`)

- Web interface for querying databases
- Accessible on port [3000](http://localhost:3000)
- Uses PostgreSQL database
- Supports multiple connections
- Allows saving queries and result

### Apache Airflow

Uses Apache Airflow version 2.7.3 with two components:

1. Airflow Webserver (`apache/airflow:2.7.3`)
   - Web interface for Airflow
   - Accessible on port [8080](http://localhost:8080)
   - Uses LocalExecutor
   - Automatically initializes the database and creates admin user

2. Airflow Scheduler (`apache/airflow:2.7.3`)
   - Handles DAG scheduling and execution
   - Depends on webserver service
   - Shares DAG folder with webserver

### Docker in Docker (`docker:dind`)

- Allows running Docker containers inside Docker
- Exposed on port `2375`
- Runs in privileged mode
- Custom daemon configuration support

All services are configured to restart automatically and use environment variables from a .env file for configuration.

### GitHub Actions

The project uses GitHub Actions to build and push images to the Docker registry. This is done through the use of *act*, which is a tool that allows you to run GitHub Actions locally.

## Running the full tutorial

Run all the infrastructure with:

```bash
docker compose up --build
```

You can now access the Airflow webserver at [http://localhost:8080](http://localhost:8080), you can also access the Registry UI at [http://localhost:8081](http://localhost:8081) or even connect to the PostgreSQL database with your favorite tool.

The next step is to run the GitHub action to build the Docker images corresponding to the tasks in the `airflow/dags` folder.

Running the GitHub action is as simple as running:

```bash
act --container-architecture linux/amd64
```
