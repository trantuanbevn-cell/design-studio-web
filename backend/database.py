"""
Database models and initialization
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///./design_studio.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    credits = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    filename = Column(String)
    file_path = Column(String)
    scene_info = Column(Text)  # JSON
    created_at = Column(DateTime, default=datetime.utcnow)

class Render(Base):
    __tablename__ = "renders"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    prompt = Column(Text)
    output_path = Column(String)
    style = Column(String)
    resolution = Column(String)
    cost = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# Session
Session = SessionLocal

def init_db():
    """Initialize database"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized")
