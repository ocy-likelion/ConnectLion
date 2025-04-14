from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class CompanyProfile(Base):
    __tablename__ = "company_profiles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    company_name = Column(String, nullable=False)
    industry = Column(String)
    description = Column(String)
    location = Column(String)
    website = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 