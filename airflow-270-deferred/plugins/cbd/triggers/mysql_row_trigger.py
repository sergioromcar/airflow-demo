from __future__ import annotations
import asyncio
from typing import Any, AsyncIterator
import mysql.connector
from airflow.triggers.base import BaseTrigger, TriggerEvent

class MySQLRowTrigger(BaseTrigger):
    def __init__(self, host: str, user: str, password: str, database: str, poke_interval: int = 10):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.poke_interval = poke_interval

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return (
            "cbd.triggers.mysql_row_trigger.MySQLRowTrigger",
            {
                "host": self.host,
                "user": self.user,
                "password": self.password,
                "database": self.database,
                "poke_interval": self.poke_interval,
            },
        )

    async def run(self) -> AsyncIterator[TriggerEvent]:
        while True:
            try:
                conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM demo_deferred WHERE estado = 'READY' LIMIT 1;")
                result = cursor.fetchone()
                if result:
                    yield TriggerEvent({"status": "success", "row": result})
                    return
                await asyncio.sleep(self.poke_interval)
            finally:
                cursor.close()
                conn.close()
