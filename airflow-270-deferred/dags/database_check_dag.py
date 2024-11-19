from airflow import DAG
from datetime import datetime
from cbd.operators.database_check_operator import DatabaseCheckOperator

with DAG(
    dag_id="database_check",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    check_condition = DatabaseCheckOperator(
        task_id="check_condition",
        table_name="demo_deferred",
        condition="estado = 'READY'",
        poll_interval=10,
    )
