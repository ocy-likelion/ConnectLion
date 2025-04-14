from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user import User
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.api.v1.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    profile: Optional[dict] = None
    created_at: str
    updated_at: Optional[str]

    class Config:
        from_attributes = True

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.get("/graduates", response_model=List[UserResponse])
async def get_graduates(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    graduates = db.query(User).filter(User.role == "GRADUATE").offset(skip).limit(limit).all()
    return graduates

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user 