from __future__ import annotations
from typing import Any, Sequence
from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from airflow.triggers.base import TriggerEvent
from file_existence_trigger import FileExistenceTrigger
import os 

class FileExistenceOperator(BaseOperator):
    """
    Operador que espera hasta que un archivo exista.
    """
    template_fields: Sequence[str] = ("file_path",)
    ui_color = "#ffefeb"

    def __init__(self, file_path: str, poll_interval: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.poll_interval = poll_interval

    def execute(self, context: Context):
        """
        Método de ejecución inicial.
        """
        self.log.info(f"Verificando si el archivo {self.file_path} existe.")
        if os.path.exists(self.file_path):
            self.log.info(f"Archivo encontrado: {self.file_path}. Continuando ejecución.")
            return {"status": "success", "file_path": self.file_path}
        else:
            self.log.info(f"Archivo no encontrado. Entrando en modo diferido.")
            self.defer(
                trigger=FileExistenceTrigger(self.file_path, self.poll_interval),
                method_name="execute_complete",
            )

    def execute_complete(self, context: Context, event: dict[str, Any]):
        """
        Se ejecuta cuando el Trigger finaliza.
        """
        self.log.info(f"Archivo encontrado: {event['file_path']}. Finalizando.")
        return event
