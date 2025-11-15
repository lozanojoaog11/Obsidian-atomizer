"""Vault Routes - Browse your knowledge"""

from fastapi import APIRouter, HTTPException
from pathlib import Path

from app.models.response import VaultStats
from app.services.processor import get_processor

router = APIRouter()


@router.get("/stats", response_model=VaultStats)
async def get_vault_stats():
    """Get vault statistics"""

    processor = get_processor()
    stats = processor.get_vault_stats()

    return VaultStats(**stats)


@router.get("/notes")
async def list_notes(folder: str = None):
    """List notes in vault"""

    processor = get_processor()
    vault_path = processor.vault_path

    # Default to permanent notes
    if folder is None:
        folder = "03-Permanent"

    notes_dir = vault_path / folder

    if not notes_dir.exists():
        return []

    notes = []
    for note_file in notes_dir.glob("*.md"):
        notes.append({
            'id': note_file.stem,
            'title': note_file.stem.replace('-', ' ').title(),
            'path': str(note_file.relative_to(vault_path))
        })

    return notes


@router.get("/notes/{note_id}")
async def get_note(note_id: str):
    """Get note content"""

    processor = get_processor()
    vault_path = processor.vault_path

    # Search for note in common folders
    for folder in ["03-Permanent", "04-MOCs", "02-Resources"]:
        note_path = vault_path / folder / f"{note_id}.md"
        if note_path.exists():
            content = note_path.read_text(encoding='utf-8')
            return {
                'id': note_id,
                'content': content,
                'path': str(note_path.relative_to(vault_path))
            }

    raise HTTPException(status_code=404, detail="Note not found")


@router.get("/mocs")
async def list_mocs():
    """List all MOCs"""

    processor = get_processor()
    vault_path = processor.vault_path
    moc_dir = vault_path / "04-MOCs"

    if not moc_dir.exists():
        return []

    mocs = []
    for moc_file in moc_dir.glob("*.md"):
        mocs.append({
            'id': moc_file.stem,
            'title': moc_file.stem.replace('-', ' ').title(),
            'path': str(moc_file.relative_to(vault_path))
        })

    return mocs
