import asyncio
from typing import Any, AsyncIterator
from airflow.triggers.base import BaseTrigger, TriggerEvent
from airflow.providers.mysql.hooks.mysql import MySqlHook

class DatabaseCheckTrigger(BaseTrigger):
    """
    Trigger que verifica si una condición se cumple en una tabla MySQL.
    """
    def __init__(self, table_name: str, condition: str, poke_interval: int = 10):
        super().__init__()
        self.table_name = table_name
        self.condition = condition
        self.poke_interval = poke_interval

    def serialize(self) -> tuple[str, dict[str, Any]]:
        """
        Serializa el Trigger para que pueda ser reusado.
        """
        return (
            "cbd.triggers.database_check_trigger.DatabaseCheckTrigger",
            {
                "table_name": self.table_name,
                "condition": self.condition,
                "poke_interval": self.poke_interval,
            },
        )

    async def run(self) -> AsyncIterator[TriggerEvent]:
        """
        Método principal del Trigger.
        """
        hook = MySqlHook(mysql_conn_id="airflow_db")  # Conexión predeterminada
        while True:
            result = hook.get_first(f"SELECT 1 FROM {self.table_name} WHERE {self.condition}")
            if result:
                yield TriggerEvent({"status": "success", "table_name": self.table_name, "condition": self.condition})
                return
            await asyncio.sleep(self.poke_interval)
