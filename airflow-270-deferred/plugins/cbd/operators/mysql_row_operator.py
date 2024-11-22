from typing import Any, Sequence
from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from airflow.triggers.base import TriggerEvent
from cbd.triggers.mysql_row_trigger import MySQLRowTrigger

class MySQLRowExistenceOperator(BaseOperator):
    template_fields: Sequence[str] = ("host", "database")
    ui_color = "#ffefeb"

    def __init__(self, host: str, user: str, password: str, database: str, poke_interval: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.poke_interval = poke_interval

    def execute(self, context: Context):
        self.log.info(f"Esperando un registro en {self.database}.demo_deferred con estado 'READY'")
        self.defer(
            trigger=MySQLRowTrigger(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                poke_interval=self.poke_interval,
            ),
            method_name="execute_complete",
        )

    def execute_complete(self, context: Context, event: dict[str, Any]):
        self.log.info(f"Registro encontrado: {event['row']}")
        return event["row"]
