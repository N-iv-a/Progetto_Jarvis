from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.models import init_db, get_db
import uvicorn

app = FastAPI(
    title="Jarvis API",
    description="Personal Task Management System",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()
    print("✅ Database initialized")


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Jarvis API",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {"status": "healthy", "database": "connected"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
