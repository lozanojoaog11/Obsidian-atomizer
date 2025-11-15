"""
Request Models - Pydantic schemas for API inputs
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class ProcessingOptions(BaseModel):
    """Options for processing a document"""

    verbose: bool = Field(default=False, description="Show detailed processing steps")
    create_mocs: bool = Field(default=True, description="Auto-create Maps of Content")
    create_connections: bool = Field(default=True, description="Generate semantic connections")
    min_connections: int = Field(default=4, ge=0, le=10, description="Minimum connections per note")
    max_connections: int = Field(default=8, ge=0, le=15, description="Maximum connections per note")


class ProcessRequest(BaseModel):
    """Request to process a document"""

    options: Optional[ProcessingOptions] = Field(default_factory=ProcessingOptions)


class SettingsUpdate(BaseModel):
    """Update application settings"""

    vault_path: Optional[str] = Field(None, description="Path to Obsidian vault")
    llm_provider: Optional[str] = Field(None, description="LLM provider (ollama or gemini)")
    llm_model: Optional[str] = Field(None, description="LLM model name")
    auto_create_mocs: Optional[bool] = Field(None, description="Auto-create MOCs")
    auto_connect: Optional[bool] = Field(None, description="Auto-generate connections")
