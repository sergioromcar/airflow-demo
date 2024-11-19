# Demo Deferred Operators and Triggers

En esta demostración veremos el uso de los operadores y los triggers usando el servicio triggerer.

## Ejemplo 1
Creación del fichero para que salte el trigger y vuelva a la ejecución del DAG

```
touch /opt/airflow/dags/trigger-file.txt
```

## Ejemplo 2
Conexión mysql
```
docker exec -it mysql mysql -uroot -proot
```

Base de datos airflow
```
use airflow;
```

Tabla inicial
```
mysql> select * from demo_deferred;
+----+---------------------+---------+
| id | fecha               | estado  |
+----+---------------------+---------+
|  1 | 2024-11-19 13:27:47 | PENDING |
+----+---------------------+---------+
```

Actualización de la tabla para que salte el trigger y vuelva a la ejecución del DAG
```
update demo_deferred set estado='READY' where id=1;
```