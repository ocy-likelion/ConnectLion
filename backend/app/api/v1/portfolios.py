from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.portfolio import Portfolio
from app.models.user import User
from typing import List, Optional
from pydantic import BaseModel
from app.api.v1.deps import get_current_user

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

class PortfolioCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    skills: Optional[List[str]] = None
    files: Optional[List[str]] = None

class PortfolioResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    category: Optional[str]
    skills: Optional[List[str]]
    files: Optional[List[str]]
    user_id: str
    created_at: str
    updated_at: Optional[str]

    class Config:
        from_attributes = True

@router.post("/", response_model=PortfolioResponse)
async def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "GRADUATE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only graduates can create portfolios"
        )
    
    db_portfolio = Portfolio(
        user_id=current_user.id,
        **portfolio.dict()
    )
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

@router.get("/", response_model=List[PortfolioResponse])
async def get_portfolios(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Portfolio)
    if category:
        query = query.filter(Portfolio.category == category)
    portfolios = query.offset(skip).limit(limit).all()
    return portfolios

@router.get("/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(
    portfolio_id: str,
    db: Session = Depends(get_db)
):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    return portfolio

@router.put("/{portfolio_id}", response_model=PortfolioResponse)
async def update_portfolio(
    portfolio_id: str,
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not db_portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    if db_portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this portfolio"
        )
    
    for key, value in portfolio.dict().items():
        setattr(db_portfolio, key, value)
    
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

@router.delete("/{portfolio_id}")
async def delete_portfolio(
    portfolio_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not db_portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    if db_portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this portfolio"
        )
    
    db.delete(db_portfolio)
    db.commit()
    return {"message": "Portfolio deleted successfully"} 