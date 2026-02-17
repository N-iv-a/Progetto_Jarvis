# === IMPORTS ===
# SQLAlchemy è l'ORM (Object Relational Mapper) - traduce classi Python in tabelle SQL
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum


# === CONFIGURAZIONE DATABASE ===
# SQLite salva tutto in un file "jarvis.db" nella cartella corrente
# Il ./ significa "cartella attuale"
SQLALCHEMY_DATABASE_URL = "sqlite:///./jarvis.db"

# Engine = il "motore" che gestisce la connessione al database
# check_same_thread=False serve per SQLite con FastAPI (evita errori di threading)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal = fabbrica di sessioni (ogni richiesta API avrà la sua sessione)
# autocommit=False: le modifiche non vengono salvate automaticamente
# autoflush=False: non scrive sul DB finché non fai commit esplicito
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = classe madre da cui erediteranno tutti i modelli/tabelle
Base = declarative_base()


# === ENUMS (liste di valori ammessi) ===
# str + enum.Enum permette di usarli sia come stringhe che come enum
class Categoria(str, enum.Enum):
    IU = "IU"              # Importante Urgente
    INU = "INU"            # Importante Non Urgente
    U = "U"                # Urgente (non importante)
    NU = "NU"              # Non Urgente
    IN_ATTESA = "In Attesa"
    LONG_TERM = "Long-term"


class Stato(str, enum.Enum):
    APERTO = "aperto"
    EARNING = "earning"      # Task in lavorazione
    COMPLETATO = "completato"


# === MODELLO DATABASE ===
# Questa classe diventa la tabella "tasks" nel database SQLite
class TaskDB(Base):
    __tablename__ = "tasks"  # Nome della tabella SQL

    # Ogni attributo = una colonna della tabella
    id = Column(Integer, primary_key=True, index=True)  # Chiave primaria, auto-incrementa
    titolo = Column(String, nullable=False)              # Obbligatorio (nullable=False)
    categoria = Column(String, default=Categoria.INU)    # Default: INU
    dettagli = Column(String, nullable=True)             # Opzionale
    outcome = Column(String, nullable=True)              # Risultato finale
    stato = Column(String, default=Stato.APERTO)         # Default: aperto
    created_at = Column(DateTime, default=datetime.now)  # Timestamp creazione
    completed_at = Column(DateTime, nullable=True)       # Timestamp completamento


# === FUNZIONI UTILITY ===

# Crea le tabelle nel database (se non esistono)
def init_db():
    Base.metadata.create_all(bind=engine)


# Dependency injection per FastAPI
# Ogni route riceve una sessione DB, che viene chiusa automaticamente dopo
def get_db():
    db = SessionLocal()  # Apre connessione
    try:
        yield db         # Passa la connessione alla route
    finally:
        db.close()       # Chiude connessione (sempre, anche se errore)