"""Orchestrator (ATHENA): Coordinates all agents in pipeline.

Pipeline:
1. Extractor: PDF/Markdown → structured text
2. Classificador: text → taxonomy
3. Destilador: text + taxonomy → atomic notes
4. Conector: notes → semantic links

Validates at each step. Returns complete result.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from cerebrum.core.extractor import Extractor
from cerebrum.core.classificador import ClassificadorAgent
from cerebrum.core.destilador import DestiladorAgent
from cerebrum.core.conector import ConectorAgent
from cerebrum.services.llm_service import LLMService


class ProcessingResult:
    """Complete processing result."""

    def __init__(self):
        self.success = False
        self.stages = {}
        self.literature_note = None
        self.permanent_notes = []
        self.links_created = 0
        self.errors = []
        self.warnings = []
        self.duration_seconds = 0
        self.stats = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for JSON serialization."""
        return {
            'success': self.success,
            'stages': self.stages,
            'literature_note': {
                'title': self.literature_note.metadata.title if self.literature_note else None,
                'id': self.literature_note.metadata.id if self.literature_note else None
            },
            'permanent_notes_count': len(self.permanent_notes),
            'permanent_notes': [
                {
                    'title': n.metadata.title,
                    'id': n.metadata.id,
                    'domain': n.metadata.domain,
                    'type': n.metadata.zk_permanent_note_type
                } for n in self.permanent_notes
            ],
            'links_created': self.links_created,
            'errors': self.errors,
            'warnings': self.warnings,
            'duration_seconds': self.duration_seconds,
            'stats': self.stats
        }


class Orchestrator:
    """ATHENA - Orchestrates the complete knowledge refinement pipeline."""

    def __init__(
        self,
        llm_service: LLMService,
        vault_path: Path,
        verbose: bool = False
    ):
        self.llm = llm_service
        self.vault_path = vault_path
        self.verbose = verbose

        # Initialize agents
        self.extractor = Extractor()
        self.classificador = ClassificadorAgent(llm_service)
        self.destilador = DestiladorAgent(llm_service, vault_path)
        self.conector = ConectorAgent(llm_service, vault_path)

    def process(self, file_path: Path) -> ProcessingResult:
        """
        Process file through complete pipeline.

        Args:
            file_path: Path to PDF, Markdown, or text file

        Returns:
            ProcessingResult with all generated notes and stats
        """

        result = ProcessingResult()
        start_time = datetime.now()

        try:
            # Stage 1: Extraction
            if self.verbose:
                print(f"📄 Stage 1: Extracting content from {file_path.name}...")

            extraction = self._run_extraction(file_path)
            result.stages['extraction'] = extraction

            if not extraction['validation']['passed']:
                result.errors.append("Extraction validation failed")
                return result

            # Stage 2: Classification
            if self.verbose:
                print("🏷️  Stage 2: Classifying content...")

            classification = self._run_classification(
                extraction['raw_text'],
                extraction['metadata']
            )
            result.stages['classification'] = classification

            if not classification['validation']['passed']:
                result.warnings.append("Classification has issues (continuing anyway)")

            # Stage 3: Destillation
            if self.verbose:
                print("⚗️  Stage 3: Destilling into atomic notes...")

            destillation = self._run_destillation(
                extraction['raw_text'],
                extraction['metadata'],
                classification
            )
            result.stages['destillation'] = destillation

            if not destillation['validation']['passed']:
                result.errors.append("Destillation validation failed")
                return result

            result.literature_note = destillation['literature_note']
            result.permanent_notes = destillation['permanent_notes']

            # Stage 4: Connection
            if self.verbose:
                print("🔗 Stage 4: Creating semantic connections...")

            connection = self._run_connection(
                destillation['permanent_notes']
            )
            result.stages['connection'] = connection

            result.links_created = connection['links_created']

            # Stage 5: Save to vault
            if self.verbose:
                print("💾 Stage 5: Saving to vault...")

            save_result = self.destilador.save_notes(
                result.literature_note,
                result.permanent_notes
            )

            # Update links in vault
            self.conector.update_vault_links(result.permanent_notes)

            result.stages['save'] = save_result

            # Calculate duration
            end_time = datetime.now()
            result.duration_seconds = (end_time - start_time).total_seconds()

            # Compile stats
            result.stats = {
                'source_file': str(file_path),
                'source_type': extraction['metadata']['source_type'],
                'words_processed': extraction['stats']['word_count'],
                'notes_created': 1 + len(result.permanent_notes),  # lit + perm
                'literature_notes': 1,
                'permanent_notes': len(result.permanent_notes),
                'links_created': result.links_created,
                'avg_links_per_note': connection['avg_links_per_note'],
                'orphan_rate': connection['orphan_rate'],
                'processing_time': result.duration_seconds,
                'validation_passed': all(
                    s.get('validation', {}).get('passed', True)
                    for s in result.stages.values()
                    if isinstance(s, dict)
                )
            }

            result.success = len(result.errors) == 0

            if self.verbose:
                self._print_summary(result)

            return result

        except Exception as e:
            result.errors.append(f"Pipeline error: {str(e)}")
            result.success = False

            if self.verbose:
                print(f"❌ Error: {str(e)}")

            return result

    def _run_extraction(self, file_path: Path) -> Dict[str, Any]:
        """Run extraction stage."""

        extraction_result = self.extractor.extract(file_path)

        # Validate
        validation = self.extractor.validate_extraction(extraction_result)

        return {
            'raw_text': extraction_result.raw_text,
            'metadata': extraction_result.metadata,
            'structure': extraction_result.structure,
            'stats': extraction_result.stats,
            'validation': validation
        }

    def _run_classification(
        self,
        raw_text: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run classification stage."""

        classification = self.classificador.classify(raw_text, metadata)

        # Validate
        validation = self.classificador.validate_classification(classification)

        return {
            **classification,
            'validation': validation
        }

    def _run_destillation(
        self,
        raw_text: str,
        metadata: Dict[str, Any],
        classification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run destillation stage."""

        destillation_result = self.destilador.destilate(
            raw_text, metadata, classification
        )

        return destillation_result

    def _run_connection(self, permanent_notes: List) -> Dict[str, Any]:
        """Run connection stage."""

        connection_result = self.conector.connect_notes(permanent_notes)

        return connection_result

    def _print_summary(self, result: ProcessingResult):
        """Print processing summary."""

        print("\n" + "="*60)
        print("📊 PROCESSING SUMMARY")
        print("="*60)

        if result.success:
            print("✅ Status: SUCCESS")
        else:
            print("❌ Status: FAILED")

        print(f"\n📝 Notes Created:")
        print(f"   Literature notes: 1")
        print(f"   Permanent notes: {len(result.permanent_notes)}")
        print(f"   Total: {1 + len(result.permanent_notes)}")

        print(f"\n🔗 Connections:")
        print(f"   Links created: {result.links_created}")
        print(f"   Avg links/note: {result.stats.get('avg_links_per_note', 0):.1f}")
        print(f"   Orphan rate: {result.stats.get('orphan_rate', 0):.1%}")

        print(f"\n⏱️  Performance:")
        print(f"   Total time: {result.duration_seconds:.1f}s")
        print(f"   Words processed: {result.stats.get('words_processed', 0):,}")

        if result.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in result.warnings:
                print(f"   - {warning}")

        if result.errors:
            print(f"\n❌ Errors:")
            for error in result.errors:
                print(f"   - {error}")

        print("\n" + "="*60)

    def batch_process(
        self,
        file_paths: List[Path]
    ) -> List[ProcessingResult]:
        """Process multiple files in batch."""

        results = []

        for i, file_path in enumerate(file_paths, 1):
            if self.verbose:
                print(f"\n{'='*60}")
                print(f"Processing {i}/{len(file_paths)}: {file_path.name}")
                print(f"{'='*60}\n")

            result = self.process(file_path)
            results.append(result)

        # Batch summary
        if self.verbose:
            self._print_batch_summary(results)

        return results

    def _print_batch_summary(self, results: List[ProcessingResult]):
        """Print batch processing summary."""

        total = len(results)
        succeeded = sum(1 for r in results if r.success)
        failed = total - succeeded

        total_notes = sum(1 + len(r.permanent_notes) for r in results)
        total_links = sum(r.links_created for r in results)
        total_time = sum(r.duration_seconds for r in results)

        print("\n" + "="*60)
        print("📊 BATCH SUMMARY")
        print("="*60)

        print(f"\nFiles processed: {total}")
        print(f"  ✅ Succeeded: {succeeded}")
        print(f"  ❌ Failed: {failed}")

        print(f"\nNotes created: {total_notes}")
        print(f"Links created: {total_links}")

        print(f"\nTotal time: {total_time:.1f}s")
        print(f"Avg time per file: {total_time/total:.1f}s")

        print("\n" + "="*60)

    def process_directory(
        self,
        directory: Path,
        pattern: str = "*.pdf"
    ) -> List[ProcessingResult]:
        """Process all matching files in directory."""

        files = list(directory.glob(pattern))

        if self.verbose:
            print(f"Found {len(files)} files matching '{pattern}'")

        return self.batch_process(files)
