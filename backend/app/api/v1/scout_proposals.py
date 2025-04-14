from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.scout_proposal import ScoutProposal
from app.models.user import User
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.api.v1.deps import get_current_user

router = APIRouter(prefix="/scout-proposals", tags=["scout-proposals"])

class ScoutProposalCreate(BaseModel):
    graduate_id: str
    message: Optional[str] = None

class ScoutProposalResponse(BaseModel):
    id: str
    company_id: str
    graduate_id: str
    status: str
    message: Optional[str]
    created_at: str
    updated_at: Optional[str]

    class Config:
        from_attributes = True

@router.post("/", response_model=ScoutProposalResponse)
async def create_scout_proposal(
    proposal: ScoutProposalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "COMPANY":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only companies can create scout proposals"
        )
    
    # Check if graduate exists
    graduate = db.query(User).filter(
        User.id == proposal.graduate_id,
        User.role == "GRADUATE"
    ).first()
    if not graduate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Graduate not found"
        )
    
    # Check if proposal already exists
    existing_proposal = db.query(ScoutProposal).filter(
        ScoutProposal.company_id == current_user.id,
        ScoutProposal.graduate_id == proposal.graduate_id,
        ScoutProposal.status == "PENDING"
    ).first()
    if existing_proposal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A pending proposal already exists for this graduate"
        )
    
    db_proposal = ScoutProposal(
        company_id=current_user.id,
        graduate_id=proposal.graduate_id,
        message=proposal.message,
        status="PENDING"
    )
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal

@router.get("/received", response_model=List[ScoutProposalResponse])
async def get_received_proposals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "GRADUATE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only graduates can view received proposals"
        )
    
    proposals = db.query(ScoutProposal).filter(
        ScoutProposal.graduate_id == current_user.id
    ).all()
    return proposals

@router.get("/sent", response_model=List[ScoutProposalResponse])
async def get_sent_proposals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "COMPANY":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only companies can view sent proposals"
        )
    
    proposals = db.query(ScoutProposal).filter(
        ScoutProposal.company_id == current_user.id
    ).all()
    return proposals

@router.put("/{proposal_id}/status")
async def update_proposal_status(
    proposal_id: str,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if status not in ["ACCEPTED", "REJECTED"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status"
        )
    
    proposal = db.query(ScoutProposal).filter(ScoutProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found"
        )
    
    if current_user.role == "GRADUATE":
        if proposal.graduate_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this proposal"
            )
    elif current_user.role == "COMPANY":
        if proposal.company_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this proposal"
            )
    
    proposal.status = status
    proposal.updated_at = datetime.utcnow()
    db.commit()
    return {"message": f"Proposal {status.lower()} successfully"} 