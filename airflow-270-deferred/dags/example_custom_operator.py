from datetime import datetime
from airflow import DAG
from custom_trigger_operator import MyOperator

with DAG(
    dag_id="example_custom_operator",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    task = MyOperator(
        task_id="my_custom_task",
        wait_for_completion=True,
        poke_interval=10,
        deferrable=True
    )
