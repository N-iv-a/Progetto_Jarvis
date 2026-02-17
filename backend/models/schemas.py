# === SCHEMAS PYDANTIC ===
# Pydantic valida i dati in entrata/uscita dalle API
# Separati da SQLAlchemy perché hanno scopi diversi:
# - SQLAlchemy: parla col database
# - Pydantic: parla con le API (validazione JSON)

from pydantic import BaseModel
from datetime import datetime
from models.database import Categoria, Stato


# Schema base - campi comuni a più operazioni
class TaskBase(BaseModel):
    titolo: str
    categoria: Categoria = Categoria.INU  # Default INU se non specificato
    dettagli: str | None = None           # Opzionale (può essere None)


# Schema per CREARE una task (eredita da TaskBase)
# Per ora identico, ma potrebbe divergere in futuro
class TaskCreate(TaskBase):
    pass


# Schema per MODIFICARE una task
# Tutti i campi opzionali - modifichi solo quello che vuoi
class TaskUpdate(BaseModel):
    titolo: str | None = None
    categoria: Categoria | None = None
    dettagli: str | None = None
    outcome: str | None = None


# Schema per LEGGERE una task (risposta API)
# Include tutti i campi, anche quelli generati dal DB
class Task(TaskBase):
    id: int                                # Generato dal DB
    outcome: str | None = None
    stato: Stato = Stato.APERTO
    created_at: datetime                   # Generato dal DB
    completed_at: datetime | None = None

    class Config:
        from_attributes = True  # Permette di convertire oggetti SQLAlchemy in Pydantic