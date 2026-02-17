from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class Categoria(str, Enum):
    IU = "IU"
    INU = "INU"
    U = "U"
    NU = "NU"
    IN_ATTESA = "In Attesa"
    LONG_TERM = "Long-term"

class Stato(str, Enum):
    APERTO = "aperto"
    COMPLETATO = "completato"
    WARNING = "warning"

class SottoTaskBase(BaseModel):
    titolo: str
    completato: bool = False

class TaskBase(BaseModel):
    titolo: str
    categoria: Categoria = Categoria.INU
    dettagli: str | None = None
    
class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    sotto_task: list[SottoTaskBase] = []
    outcome: str | None = None
    stato: Stato = Stato.APERTO
    created_at: datetime
    completed_at: datetime | None = None
    task_derivati_ids: list[int] = []

    class Config:
        from_attributes = True