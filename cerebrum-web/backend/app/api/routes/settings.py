"""Settings Routes - Configure your Cerebrum"""

from fastapi import APIRouter
from app.models.response import Settings
from app.models.request import SettingsUpdate

router = APIRouter()

# Simple in-memory settings (could be persisted later)
_settings = Settings()


@router.get("/", response_model=Settings)
async def get_settings():
    """Get current settings"""
    return _settings


@router.put("/", response_model=Settings)
async def update_settings(updates: SettingsUpdate):
    """Update settings"""

    global _settings

    # Update only provided fields
    if updates.vault_path is not None:
        _settings.vault_path = updates.vault_path

    if updates.llm_provider is not None:
        _settings.llm_provider = updates.llm_provider

    if updates.llm_model is not None:
        _settings.llm_model = updates.llm_model

    if updates.auto_create_mocs is not None:
        _settings.auto_create_mocs = updates.auto_create_mocs

    if updates.auto_connect is not None:
        _settings.auto_connect = updates.auto_connect

    return _settings
