from __future__ import annotations
import asyncio
from typing import Any, AsyncIterator
import mysql.connector
from airflow.triggers.base import BaseTrigger, TriggerEvent

class MySQLRowTrigger(BaseTrigger):
    def __init__(self, host: str, user: str, password: str, database: str, poll_interval: int = 10):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.poll_interval = poll_interval

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return (
            "mysql_row_trigger.MySQLRowTrigger",
            {
                "host": self.host,
                "user": self.user,
                "password": self.password,
                "database": self.database,
                "poll_interval": self.poll_interval,
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
                await asyncio.sleep(self.poll_interval)
            finally:
                cursor.close()
                conn.close()
