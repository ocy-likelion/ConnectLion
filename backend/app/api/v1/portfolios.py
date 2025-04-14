from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.portfolio import Portfolio
from app.models.user import User
from typing import List, Optional
from pydantic import BaseModel
from app.api.v1.deps import get_current_user

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

class PortfolioBase(BaseModel):
    title: str
    description: str
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    image_url: Optional[str] = None

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(PortfolioBase):
    pass

class PortfolioResponse(PortfolioBase):
    id: str
    user_id: str
    created_at: str
    updated_at: Optional[str]

    class Config:
        from_attributes = True

@router.post("", response_model=PortfolioResponse)
async def create_portfolio(
    portfolio: PortfolioCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    새로운 포트폴리오를 생성하는 API
    
    - **portfolio**: 생성할 포트폴리오 정보
        - title: 포트폴리오 제목
        - description: 포트폴리오 설명
        - github_url: GitHub 저장소 URL (선택)
        - demo_url: 데모 사이트 URL (선택)
        - image_url: 이미지 URL (선택)
    
    Returns:
        - PortfolioResponse: 생성된 포트폴리오 정보
    
    Raises:
        - **401**: 인증되지 않은 사용자
    """
    db_portfolio = Portfolio(**portfolio.dict(), user_id=current_user.id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

@router.get("", response_model=List[PortfolioResponse])
async def get_portfolios(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    포트폴리오 목록을 조회하는 API
    
    - **skip**: 건너뛸 레코드 수 (페이지네이션)
    - **limit**: 가져올 레코드 수 (페이지네이션)
    
    Returns:
        - List[PortfolioResponse]: 포트폴리오 목록
    """
    portfolios = db.query(Portfolio).offset(skip).limit(limit).all()
    return portfolios

@router.get("/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(
    portfolio_id: str,
    db: Session = Depends(get_db)
):
    """
    특정 포트폴리오를 조회하는 API
    
    - **portfolio_id**: 조회할 포트폴리오의 ID
    
    Returns:
        - PortfolioResponse: 포트폴리오 정보
    
    Raises:
        - **404**: 포트폴리오를 찾을 수 없음
    """
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
    portfolio: PortfolioUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    포트폴리오를 수정하는 API
    
    - **portfolio_id**: 수정할 포트폴리오의 ID
    - **portfolio**: 수정할 포트폴리오 정보
        - title: 포트폴리오 제목
        - description: 포트폴리오 설명
        - github_url: GitHub 저장소 URL (선택)
        - demo_url: 데모 사이트 URL (선택)
        - image_url: 이미지 URL (선택)
    
    Returns:
        - PortfolioResponse: 수정된 포트폴리오 정보
    
    Raises:
        - **401**: 인증되지 않은 사용자
        - **403**: 권한 없음 (다른 사용자의 포트폴리오)
        - **404**: 포트폴리오를 찾을 수 없음
    """
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not db_portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    if db_portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    for key, value in portfolio.dict().items():
        setattr(db_portfolio, key, value)
    
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_portfolio(
    portfolio_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    포트폴리오를 삭제하는 API
    
    - **portfolio_id**: 삭제할 포트폴리오의 ID
    
    Returns:
        - 204 No Content
    
    Raises:
        - **401**: 인증되지 않은 사용자
        - **403**: 권한 없음 (다른 사용자의 포트폴리오)
        - **404**: 포트폴리오를 찾을 수 없음
    """
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not db_portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    if db_portfolio.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(db_portfolio)
    db.commit()
    return None 