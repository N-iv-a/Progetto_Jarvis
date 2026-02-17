# === IMPORTS ===
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# Importiamo tutto da models (grazie a __init__.py)
from models import (
    TaskDB, Task, TaskCreate, TaskUpdate,
    Categoria, Stato,
    init_db, get_db
)

# === INIZIALIZZAZIONE APP ===
app = FastAPI(title="Jarvis API")

# === CORS ===
# Permette al frontend (localhost:5173) di comunicare col backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend Vite
    allow_credentials=True,
    allow_methods=["*"],  # Permetti tutti i metodi (GET, POST, ecc.)
    allow_headers=["*"],  # Permetti tutti gli headers
)

# Crea le tabelle nel database all'avvio (se non esistono)
init_db()


# === ROUTES ===

@app.get("/")
def root():
    """Endpoint di test - verifica che Jarvis sia online"""
    return {"messaggio": "Jarvis è online"}


@app.get("/tasks", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)):
    """
    Lista tutte le task.
    
    Depends(get_db) = FastAPI inietta automaticamente la sessione DB
    """
    return db.query(TaskDB).all()  # SELECT * FROM tasks


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Recupera una singola task per ID"""
    
    # .first() ritorna None se non trova nulla
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task non trovata")
    
    return task


@app.post("/tasks", response_model=Task)
def create_task(task_input: TaskCreate, db: Session = Depends(get_db)):
    """
    Crea una nuova task.
    
    task_input: dati validati da Pydantic (TaskCreate schema)
    """
    
    # Crea oggetto TaskDB (modello SQLAlchemy)
    nuova_task = TaskDB(
        titolo=task_input.titolo,
        categoria=task_input.categoria,
        dettagli=task_input.dettagli,
        created_at=datetime.now()
    )
    
    db.add(nuova_task)      # Aggiunge alla sessione
    db.commit()             # Salva nel database
    db.refresh(nuova_task)  # Ricarica per ottenere l'ID generato
    
    return nuova_task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """
    Modifica parziale di una task.
    
    Aggiorna solo i campi che vengono passati (non-None)
    """
    
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task non trovata")
    
    # model_dump(exclude_unset=True) ritorna solo i campi effettivamente passati
    update_data = task_update.model_dump(exclude_unset=True)
    
    # Aggiorna ogni campo presente
    for campo, valore in update_data.items():
        setattr(task, campo, valore)  # task.campo = valore
    
    db.commit()
    db.refresh(task)
    
    return task


@app.patch("/tasks/{task_id}/status", response_model=Task)
def update_status(task_id: int, nuovo_stato: Stato, db: Session = Depends(get_db)):
    """
    Cambia solo lo stato di una task.
    
    Se completato, salva anche il timestamp di completamento
    """
    
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task non trovata")
    
    task.stato = nuovo_stato
    
    # Se completato, registra quando
    if nuovo_stato == Stato.COMPLETATO:
        task.completed_at = datetime.now()
    
    db.commit()
    db.refresh(task)
    
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Elimina una task"""
    
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task non trovata")
    
    db.delete(task)
    db.commit()
    
    return {"messaggio": f"Task '{task.titolo}' eliminata"}