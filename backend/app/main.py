from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.api.v1 import auth, users, portfolios, companies, scout_proposals

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(portfolios.router, prefix=settings.API_V1_STR)
app.include_router(companies.router, prefix=settings.API_V1_STR)
app.include_router(scout_proposals.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to TalentConnect API"} 