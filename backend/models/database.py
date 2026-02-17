from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

# Many-to-many relationship table
task_tags = Table('task_tags', Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(DateTime)
    priority = Column(String, default='medium')  # low, medium, high
    status = Column(String, default='todo')  # todo, in_progress, done
    category_id = Column(Integer, ForeignKey('categories.id'))
    calendar_event_id = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="tasks")
    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")


class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    color = Column(String, default='#3498db')
    
    # Relationships
    tasks = relationship("Task", back_populates="category")


class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationships
    tasks = relationship("Task", secondary=task_tags, back_populates="tags")


# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./database/jarvis.db')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
