"""Response Models - Clean and simple"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class NoteInfo(BaseModel):
    """Basic note information"""
    id: str
    title: str
    domain: Optional[str] = None
    type: Optional[str] = None


class MOCInfo(BaseModel):
    """MOC information"""
    id: str
    title: str
    note_count: int
    status: str


class ProcessingResult(BaseModel):
    """Processing result - simple and clean"""
    job_id: str
    success: bool
    literature_note: Optional[NoteInfo] = None
    permanent_notes: List[NoteInfo] = []
    mocs_created: List[MOCInfo] = []
    mocs_updated: List[MOCInfo] = []
    links_created: int = 0
    duration_seconds: float = 0
    errors: List[str] = []


class JobStatus(BaseModel):
    """Job status for polling"""
    job_id: str
    status: str  # 'processing', 'completed', 'failed'
    stage: Optional[str] = None
    progress: float = 0.0
    result: Optional[ProcessingResult] = None


class VaultStats(BaseModel):
    """Vault statistics"""
    total_notes: int
    permanent_notes: int
    literature_notes: int
    mocs: int
    total_connections: int


class Settings(BaseModel):
    """Application settings"""
    vault_path: str = "./vault"
    llm_provider: str = "ollama"
    llm_model: str = "llama3.2"
    auto_create_mocs: bool = True
    auto_connect: bool = True
