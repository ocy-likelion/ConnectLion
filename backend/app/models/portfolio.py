from sqlalchemy import Column, String, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)
    skills = Column(JSON)  # Store as JSON array
    files = Column(JSON)   # Store S3 file references
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 