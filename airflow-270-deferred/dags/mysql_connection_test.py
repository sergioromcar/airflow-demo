from airflow import DAG
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.operators.python import PythonOperator
from datetime import datetime

def check_mysql_connection():
    hook = MySqlHook(mysql_conn_id="airflow_db")
    result = hook.get_first("SELECT NOW();")
    print(f"Hora actual en MySQL: {result[0]}")

with DAG(
    dag_id="mysql_connection_test",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    test_mysql_connection = PythonOperator(
        task_id="test_mysql_connection",
        python_callable=check_mysql_connection,
    )
