from airflow import DAG
from file_existence_operator import FileExistenceOperator
from datetime import datetime

with DAG(
    dag_id="file_existence_dag",
    schedule_interval=None,
    start_date=datetime(2024, 11, 18),
    catchup=False,
    tags=["example"],
) as dag:

    wait_for_file = FileExistenceOperator(
        task_id="wait_for_file",
        file_path="/opt/airflow/dags/trigger-file.txt",
        poll_interval=10,  # Intervalo en segundos para revisar la existencia del archivo
    )

    wait_for_file
