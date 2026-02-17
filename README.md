# Jarvis - Personal Task Management System

Sistema di gestione task personale con integrazione Google Calendar e notifiche intelligenti.

## 🎯 Obiettivi

- Task management completo con priorità e categorie
- Sincronizzazione bidirezionale con Google Calendar
- Sistema notifiche (email/push)
- Analisi e statistiche completamento task
- OCR e AI per automazione (fase 2)

## 🏗️ Architettura

**Backend:**
- FastAPI (REST API)
- SQLite (database)
- Google Calendar API
- Sistema notifiche

**Frontend:**
- Streamlit (MVP)
- Future: React PWA

## 📁 Struttura Progetto

```
jarvis/
├── backend/          # API FastAPI
│   ├── api/         # Route endpoints
│   ├── models/      # Database models
│   ├── services/    # Business logic
│   └── main.py      # Entry point
├── frontend/         # Streamlit UI
├── database/         # SQLite DB
├── tests/           # Unit tests
└── requirements.txt
```

## 🚀 Setup

1. **Clone repository**
```bash
git clone [repository-url]
cd jarvis
```

2. **Virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate  # Windows
```

3. **Installa dipendenze**
```bash
pip install -r requirements.txt
```

4. **Configura environment**
```bash
cp .env.example .env
# Edita .env con le tue credenziali
```

5. **Avvia backend**
```bash
cd backend
python main.py
```

API disponibile su: `http://localhost:8000`
Documentazione: `http://localhost:8000/docs`

6. **Avvia frontend (in altro terminale)**
```bash
cd frontend
streamlit run app.py
```

## 🔑 Google Calendar Setup

1. Vai su [Google Cloud Console](https://console.cloud.google.com)
2. Crea nuovo progetto "Jarvis"
3. Abilita Google Calendar API
4. Crea credenziali OAuth 2.0
5. Scarica `credentials.json` e metti in root progetto
6. Aggiungi redirect URI: `http://localhost:8000/auth/callback`

## 📊 Database Schema

**Tasks**
- id, title, description
- due_date, priority, status
- category_id, calendar_event_id
- created_at, updated_at

**Categories**
- id, name, color

**Tags**
- id, name
- Many-to-many con Tasks

## 🛠️ Development

**Backend API:**
```bash
cd backend
uvicorn main:app --reload
```

**Run tests:**
```bash
pytest tests/
```

**Database migrations:**
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## 📝 Roadmap

### Fase 1 - MVP ✅
- [x] Setup progetto
- [ ] CRUD tasks API
- [ ] Database SQLite
- [ ] UI Streamlit base
- [ ] Auth Google Calendar
- [ ] Sync bidirezionale

### Fase 2 - Avanzate
- [ ] Sistema notifiche
- [ ] Ricerca/filtri avanzati
- [ ] Dashboard statistiche
- [ ] OCR immagini → task
- [ ] AI categorizzazione
- [ ] React PWA frontend

## 🤝 Contributing

Progetto personale per portfolio. Feedback benvenuti!

## 📄 License

MIT License

## 👤 Author

Nick - Data Product Specialist @ Autoguidovie
