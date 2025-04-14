from sqlalchemy import Column, String, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class ScoutProposal(Base):
    __tablename__ = "scout_proposals"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("users.id"), nullable=False)
    graduate_id = Column(String, ForeignKey("users.id"), nullable=False)
    status = Column(Enum('PENDING', 'ACCEPTED', 'REJECTED', name='proposal_status'), nullable=False)
    message = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 