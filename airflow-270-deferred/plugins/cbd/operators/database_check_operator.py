from __future__ import annotations
from typing import Any, Sequence
from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from airflow.triggers.base import TriggerEvent
from airflow.providers.mysql.hooks.mysql import MySqlHook
from cbd.triggers.database_check_trigger import DatabaseCheckTrigger

class DatabaseCheckOperator(BaseOperator):
    """
    Operador que espera hasta que se cumpla una condición en una tabla MySQL.
    """
    template_fields: Sequence[str] = ("table_name", "condition")
    ui_color = "#ffefeb"

    def __init__(self, table_name: str, condition: str, poke_interval: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.table_name = table_name
        self.condition = condition
        self.poke_interval = poke_interval

    def execute(self, context: Context):
        """
        Método de ejecución inicial.
        """
        self.log.info(f"Verificando la condición: {self.condition} en la tabla {self.table_name}.")
        hook = MySqlHook(mysql_conn_id="airflow_db")  # Conexión predeterminada
        result = hook.get_first(f"SELECT 1 FROM {self.table_name} WHERE {self.condition}")
        if result:
            self.log.info("Condición cumplida. Continuando ejecución.")
            return {"status": "success", "table_name": self.table_name, "condition": self.condition}
        else:
            self.log.info("Condición no cumplida. Entrando en modo diferido.")
            self.defer(
                trigger=DatabaseCheckTrigger(self.table_name, self.condition, self.poke_interval),
                method_name="execute_complete",
            )

    def execute_complete(self, context: Context, event: dict[str, Any]):
        """
        Se ejecuta cuando el Trigger finaliza.
        """
        self.log.info(f"Condición cumplida en la tabla {event['table_name']}. Finalizando.")
        return event
