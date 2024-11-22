from __future__ import annotations
import os
import asyncio
from typing import Any, AsyncIterator
from airflow.triggers.base import BaseTrigger, TriggerEvent

class FileExistenceTrigger(BaseTrigger):
    """
    Trigger que verifica si un archivo existe.
    """
    def __init__(self, file_path: str, poke_interval: int = 10):
        super().__init__()
        self.file_path = file_path
        self.poke_interval = poke_interval

    def serialize(self) -> tuple[str, dict[str, Any]]:
        """
        Serializa el Trigger para que pueda ser reusado.
        """
        return (
            "cbd.triggers.file_existence_trigger.FileExistenceTrigger",
            {"file_path": self.file_path, "poke_interval": self.poke_interval},
        )

    async def run(self) -> AsyncIterator[TriggerEvent]:
        """
        Método principal del Trigger.
        """
        while True:
            if os.path.exists(self.file_path):
                yield TriggerEvent({"status": "success", "file_path": self.file_path})
                return
            await asyncio.sleep(self.poke_interval)
