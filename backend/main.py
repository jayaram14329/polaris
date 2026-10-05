import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.sample_seed import seed_database
from backend.routers import (
    auth_routes,
    repository_routes,
    station_routes,
    search_routes,
    rag_routes,
    outreach_routes,
    academy_routes,
    admin_routes
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Integrated Polar Science Outreach, Knowledge Repository and Media Dissemination Portal (SIH26063 - MoES/NCPOR)"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event: Initialize & seed database
@app.on_event("startup")
def on_startup():
    print("POLARIS Backend Starting Up...")
    seed_database()
    print("POLARIS Backend Ready to Serve.")

# Mount API Routers
app.include_router(auth_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(repository_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(station_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(search_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(rag_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(outreach_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(academy_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin_routes.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {
        "system": "POLARIS",
        "description": "Polar Knowledge & Outreach Intelligence System",
        "problem_statement": "SIH26063",
        "organization": "Ministry of Earth Sciences (MoES) / NCPOR",
        "status": "Operational",
        "api_docs": "/docs",
        "version": settings.VERSION
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "POLARIS Backend API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
