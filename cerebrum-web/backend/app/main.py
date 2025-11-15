"""
Cerebrum Web API - FastAPI Backend
Beautiful, minimalist API for knowledge refinement
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.api.routes import process, vault, settings
from app.api.websocket import websocket_endpoint

# Create FastAPI app
app = FastAPI(
    title="Cerebrum API",
    description="It just works, beautifully ✨",
    version="0.5.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware (allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(process.router, prefix="/api", tags=["process"])
app.include_router(vault.router, prefix="/api/vault", tags=["vault"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])

# WebSocket endpoint
app.add_websocket_route("/ws/process/{job_id}", websocket_endpoint)


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "app": "Cerebrum API",
        "version": "0.5.0",
        "status": "running",
        "message": "It just works, beautifully ✨"
    }


@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.5.0"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
