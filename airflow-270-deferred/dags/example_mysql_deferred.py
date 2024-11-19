from datetime import datetime
from airflow import DAG
from mysql_row_operator import MySQLRowExistenceOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id="demo_deferred_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    wait_for_row = MySQLRowExistenceOperator(
        task_id="wait_for_ready_row",
        host="mysql",
        user="airflow",
        password="airflow",
        database="airflow",
        poll_interval=10,
    )
