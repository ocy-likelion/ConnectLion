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
    """
    현재 로그인한 사용자의 정보를 조회하는 API
    
    Returns:
        - UserResponse: 사용자 정보
    
    Raises:
        - **401**: 인증되지 않은 사용자
    """
    return current_user

@router.get("/graduates", response_model=List[UserResponse])
async def get_graduates(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    졸업생 목록을 조회하는 API
    
    - **skip**: 건너뛸 레코드 수 (페이지네이션)
    - **limit**: 가져올 레코드 수 (페이지네이션)
    
    Returns:
        - List[UserResponse]: 졸업생 목록
    """
    graduates = db.query(User).filter(User.role == "GRADUATE").offset(skip).limit(limit).all()
    return graduates

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    특정 사용자의 정보를 조회하는 API
    
    - **user_id**: 조회할 사용자의 ID
    
    Returns:
        - UserResponse: 사용자 정보
    
    Raises:
        - **404**: 사용자를 찾을 수 없음
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user 