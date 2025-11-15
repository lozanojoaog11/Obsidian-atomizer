"""Processor Service - Integrates with existing Cerebrum pipeline"""

import sys
from pathlib import Path
from typing import Dict, Any, Callable
import uuid

# Add parent directory to path to import cerebrum
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from cerebrum.core.orchestrator import Orchestrator
from cerebrum.services.llm_service import LLMService


class ProcessorService:
    """Simple service that wraps Cerebrum orchestrator"""

    def __init__(self, vault_path: Path, verbose: bool = False):
        self.vault_path = vault_path
        self.verbose = verbose
        self.llm = LLMService.create_default()
        self.orchestrator = Orchestrator(self.llm, vault_path, verbose=verbose)
        self.jobs: Dict[str, Dict[str, Any]] = {}  # In-memory job storage

    def process_file(
        self,
        file_path: Path,
        callback: Callable[[str, Dict[str, Any]], None] = None
    ) -> str:
        """
        Process a file and return job_id

        Args:
            file_path: Path to file to process
            callback: Optional callback for progress updates

        Returns:
            job_id: Unique job identifier
        """
        job_id = str(uuid.uuid4())

        # Store job
        self.jobs[job_id] = {
            'status': 'processing',
            'stage': 'starting',
            'progress': 0.0,
            'result': None
        }

        try:
            # Update: stage 1
            if callback:
                callback(job_id, {'stage': 'extraction', 'progress': 0.17})

            # Process using existing Cerebrum pipeline
            result = self.orchestrator.process(file_path)

            # Convert to simple format
            simple_result = {
                'job_id': job_id,
                'success': result.success,
                'literature_note': {
                    'id': result.literature_note.metadata.id,
                    'title': result.literature_note.metadata.title,
                    'domain': result.literature_note.metadata.domain,
                    'type': 'literature'
                } if result.literature_note else None,
                'permanent_notes': [
                    {
                        'id': n.metadata.id,
                        'title': n.metadata.title,
                        'domain': n.metadata.domain,
                        'type': n.metadata.zk_permanent_note_type
                    } for n in result.permanent_notes
                ],
                'mocs_created': [
                    {
                        'id': m.metadata.id,
                        'title': m.metadata.title,
                        'note_count': m.metadata.moc_note_count,
                        'status': m.metadata.status
                    } for m in result.mocs_created
                ],
                'mocs_updated': [
                    {
                        'id': m.metadata.id,
                        'title': m.metadata.title,
                        'note_count': m.metadata.moc_note_count,
                        'status': m.metadata.status
                    } for m in result.mocs_updated
                ],
                'links_created': result.links_created,
                'duration_seconds': result.duration_seconds,
                'errors': result.errors
            }

            # Update job with result
            self.jobs[job_id] = {
                'status': 'completed',
                'stage': 'complete',
                'progress': 1.0,
                'result': simple_result
            }

            if callback:
                callback(job_id, {'stage': 'complete', 'progress': 1.0})

        except Exception as e:
            self.jobs[job_id] = {
                'status': 'failed',
                'stage': 'error',
                'progress': 0.0,
                'result': {
                    'job_id': job_id,
                    'success': False,
                    'errors': [str(e)]
                }
            }

            if callback:
                callback(job_id, {'stage': 'error', 'error': str(e)})

        return job_id

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of a processing job"""
        return self.jobs.get(job_id, {
            'status': 'not_found',
            'stage': None,
            'progress': 0.0,
            'result': None
        })

    def get_vault_stats(self) -> Dict[str, Any]:
        """Get vault statistics"""
        # Simple implementation - count files
        permanent_dir = self.vault_path / "03-Permanent"
        moc_dir = self.vault_path / "04-MOCs"

        permanent_count = len(list(permanent_dir.glob("*.md"))) if permanent_dir.exists() else 0
        moc_count = len(list(moc_dir.glob("*.md"))) if moc_dir.exists() else 0

        return {
            'total_notes': permanent_count + moc_count,
            'permanent_notes': permanent_count,
            'literature_notes': 0,  # Could count if needed
            'mocs': moc_count,
            'total_connections': 0  # Could calculate if needed
        }


# Global instance
_processor: ProcessorService = None


def get_processor(vault_path: Path = None) -> ProcessorService:
    """Get or create processor instance"""
    global _processor

    if _processor is None:
        if vault_path is None:
            vault_path = Path.cwd() / "vault"
        _processor = ProcessorService(vault_path)

    return _processor
