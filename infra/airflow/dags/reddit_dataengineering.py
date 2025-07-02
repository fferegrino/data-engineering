from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.dummy import DummyOperator
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG(
    'futbol_dataengineering',
    default_args=default_args,
    description='A data engineering pipeline to extract data from Mediotiempo and load it into a PostgreSQL database',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    start = DummyOperator(
        task_id='start'
    )

    fetch_data = DockerOperator(
        task_id='fetch_data',
        image='registry:5000/python_futbol',  # Using official Docker Hello World image
        container_name='python_futbol',
        api_version='auto',
        auto_remove=True,
        docker_url='tcp://dind:2375',  # Unix socket path to Docker daemon
        network_mode='host',
        environment={
            'DB_HOST': 'postgres',
            'DB_PORT': '5432',
            'DB_DATABASE': 'futbol_db',
            'DB_USER': 'superuser',
            'DB_PASSWORD': 'superuser_password'
        },
        force_pull=True
    )

    build_dbt_models = DockerOperator(
        task_id='build_dbt_models',
        image='registry:5000/dbt_futbol',  # Using official Docker Hello World image
        container_name='dbt_futbol',
        api_version='auto',
        auto_remove=True,
        docker_url='tcp://dind:2375',  # Unix socket path to Docker daemon
        network_mode='host',
        force_pull=True
    )

    end = DummyOperator(
        task_id='end'
    )

    start >> fetch_data >> build_dbt_models >> end
