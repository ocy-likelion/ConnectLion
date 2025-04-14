from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.company import CompanyProfile
from app.models.user import User
from typing import List, Optional
from pydantic import BaseModel
from app.api.v1.deps import get_current_user

router = APIRouter(prefix="/companies", tags=["companies"])

class CompanyProfileCreate(BaseModel):
    company_name: str
    industry: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None

class CompanyProfileResponse(BaseModel):
    id: str
    company_name: str
    industry: Optional[str]
    description: Optional[str]
    location: Optional[str]
    website: Optional[str]
    user_id: str
    created_at: str
    updated_at: Optional[str]

    class Config:
        from_attributes = True

@router.post("/", response_model=CompanyProfileResponse)
async def create_company_profile(
    profile: CompanyProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "COMPANY":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only companies can create company profiles"
        )
    
    # Check if profile already exists
    existing_profile = db.query(CompanyProfile).filter(CompanyProfile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company profile already exists"
        )
    
    db_profile = CompanyProfile(
        user_id=current_user.id,
        **profile.dict()
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/", response_model=List[CompanyProfileResponse])
async def get_company_profiles(
    skip: int = 0,
    limit: int = 10,
    industry: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(CompanyProfile)
    if industry:
        query = query.filter(CompanyProfile.industry == industry)
    profiles = query.offset(skip).limit(limit).all()
    return profiles

@router.get("/{profile_id}", response_model=CompanyProfileResponse)
async def get_company_profile(
    profile_id: str,
    db: Session = Depends(get_db)
):
    profile = db.query(CompanyProfile).filter(CompanyProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company profile not found"
        )
    return profile

@router.put("/{profile_id}", response_model=CompanyProfileResponse)
async def update_company_profile(
    profile_id: str,
    profile: CompanyProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_profile = db.query(CompanyProfile).filter(CompanyProfile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company profile not found"
        )
    
    if db_profile.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this profile"
        )
    
    for key, value in profile.dict().items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.delete("/{profile_id}")
async def delete_company_profile(
    profile_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_profile = db.query(CompanyProfile).filter(CompanyProfile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company profile not found"
        )
    
    if db_profile.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this profile"
        )
    
    db.delete(db_profile)
    db.commit()
    return {"message": "Company profile deleted successfully"} 