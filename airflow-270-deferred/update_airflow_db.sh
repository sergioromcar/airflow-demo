docker exec -it airflow-webserver airflow connections add 'airflow_db' \
    --conn-type 'mysql' \
    --conn-host 'mysql' \
    --conn-schema 'airflow' \
    --conn-login 'root' \
    --conn-password 'root' \
    --conn-port '3306'