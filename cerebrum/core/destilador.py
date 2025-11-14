"""Destilador: LLM-based knowledge atomizer.

Transforms raw extracted text into atomic notes following:
- BASB: Resources placement, Progressive Summarization Layer 0
- LYT: MOC assignment
- Zettelkasten: Atomic concept extraction, permanent notes

Core responsibility: 1 source → 1 literature note + 5-15 permanent notes
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import uuid
from datetime import datetime, timedelta
import re

from cerebrum.models.note import Note, NoteMetadata
from cerebrum.services.llm_service import LLMService


class DestiladorAgent:
    """Atomizes content into perfect permanent notes."""

    def __init__(self, llm_service: LLMService, vault_path: Path):
        self.llm = llm_service
        self.vault_path = vault_path

    def destilate(
        self,
        raw_text: str,
        metadata: Dict[str, Any],
        classification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Destilate source into atomic notes.

        Args:
            raw_text: Extracted text from source
            metadata: Extraction metadata
            classification: Classification result (domain, BASB path, MOCs, etc.)

        Returns:
            Dict with:
                - literature_note: Literature note
                - permanent_notes: List[Note] (5-15 atomic concepts)
                - stats: Processing statistics
        """

        # Step 1: Create literature note (source note)
        literature_note = self._create_literature_note(
            raw_text, metadata, classification
        )

        # Step 2: Extract atomic concepts via LLM
        concepts = self._extract_atomic_concepts(
            raw_text, metadata, classification
        )

        # Step 3: Create permanent note for each concept
        permanent_notes = []
        for concept in concepts:
            perm_note = self._create_permanent_note(
                concept, literature_note, classification
            )
            permanent_notes.append(perm_note)

        # Step 3.5: Update literature note with links to permanent notes
        self._update_literature_note_with_links(literature_note, permanent_notes)

        # Step 4: Validate results
        validation = self._validate_destillation(
            literature_note, permanent_notes
        )

        return {
            'literature_note': literature_note,
            'permanent_notes': permanent_notes,
            'stats': {
                'concepts_extracted': len(concepts),
                'permanent_notes_created': len(permanent_notes),
                'avg_note_size': sum(len(n.content) for n in permanent_notes) / len(permanent_notes),
                'validation_passed': validation['passed']
            },
            'validation': validation
        }

    def _create_literature_note(
        self,
        raw_text: str,
        metadata: Dict[str, Any],
        classification: Dict[str, Any]
    ) -> Note:
        """Create literature note (source note)."""

        # Generate unique ID (timestamp + UUID to prevent collisions)
        note_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"

        # Extract bibliographic info
        source_type = metadata.get('source_type', 'unknown')
        title = metadata.get('title', 'Untitled')
        authors = metadata.get('authors', [])

        # Create frontmatter
        lit_metadata = NoteMetadata(
            id=note_id,
            title=title,
            type='literature',
            status='seedling',
            domain=classification.get('domain'),
            subdomain=classification.get('subdomain'),
            tags=classification.get('tags', []),
            basb_para_category='Resources',
            basb_para_path=classification.get('basb_para_path'),
            basb_progressive_summary_layer=0,
            lyt_mocs=classification.get('lyt_mocs', []),
            source_type=source_type,
            source_title=title,
            source_authors=authors,
            created=datetime.now().isoformat(),
            next_review=(datetime.now() + timedelta(days=30)).isoformat()
        )

        # Create body using template
        body = self._render_literature_template(
            raw_text, metadata, classification
        )

        return Note(metadata=lit_metadata, content=body)

    def _render_literature_template(
        self,
        raw_text: str,
        metadata: Dict[str, Any],
        classification: Dict[str, Any]
    ) -> str:
        """Render literature note body."""

        title = metadata.get('title', 'Untitled')
        authors = metadata.get('authors', [])
        authors_str = ', '.join(authors) if authors else 'Unknown'

        # Extract first 1000 chars as preview
        preview = raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text

        return f"""# 📚 {title}

> [!info] Bibliographic Info
> **Authors:** {authors_str}
> **Source Type:** {metadata.get('source_type', 'unknown')}
> **File:** {metadata.get('file_name', 'unknown')}

---

## 📋 Summary (Layer 0 - Raw Capture)

{preview}

---

## 💎 Key Concepts

See permanent notes created from this source:

{{{{list_of_permanent_notes}}}}

---

## 📝 Raw Content

{raw_text}

---

**Progressive Summarization:**
- Layer 0: ✅ Complete (raw capture)
- Layer 1: ⏳ Todo (when first used - bold 10-20%)
- Layer 2: ⏳ Todo (when critical - highlight 10-20% of bold)
- Layer 3: ⏳ Todo (executive summary)
"""

    def _update_literature_note_with_links(
        self,
        literature_note: Note,
        permanent_notes: List[Note]
    ) -> None:
        """Update literature note by replacing placeholder with actual links to permanent notes."""

        # Build list of links
        links_list = []
        for note in permanent_notes:
            links_list.append(f"- [[{note.metadata.title}]]")

        links_text = "\n".join(links_list)

        # Replace placeholder
        literature_note.content = literature_note.content.replace(
            "{{{{list_of_permanent_notes}}}}",
            links_text
        )

    def _extract_atomic_concepts(
        self,
        raw_text: str,
        metadata: Dict[str, Any],
        classification: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract 5-15 atomic concepts using LLM."""

        prompt = f"""You are an expert knowledge curator following Zettelkasten principles.

Extract 5-15 ATOMIC concepts from this text. Each concept must be:
1. **Atomic**: One clear idea that stands alone
2. **Autonomous**: Makes sense without the source
3. **Valuable**: Worth remembering long-term
4. **Specific**: Concrete, not vague

Source title: {metadata.get('title', 'Unknown')}
Domain: {classification.get('domain', 'general')}

Text:
{raw_text[:4000]}

For each concept, provide:
1. **title**: Clear, descriptive title (3-8 words)
2. **definition**: One-sentence atomic definition
3. **explanation**: 2-3 paragraphs explaining the concept
4. **why_matters**: Why this concept is important
5. **applications**: 2-3 practical applications
6. **connections**: Related concepts (we'll link later)
7. **concept_type**: concept/principle/model/evidence/mechanism

Return as JSON array:
[
  {{
    "title": "Concept Title",
    "definition": "One-sentence definition",
    "explanation": "Detailed explanation...",
    "why_matters": "Why it matters...",
    "applications": ["App 1", "App 2"],
    "connections": ["Related concept 1", "Related concept 2"],
    "concept_type": "concept"
  }}
]

Return ONLY valid JSON, no other text.
"""

        response = self.llm.generate(prompt, max_tokens=3000)

        # Parse JSON response
        try:
            # Extract JSON from response (in case LLM adds extra text)
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                concepts = json.loads(json_match.group())
            else:
                concepts = json.loads(response)

            # Validate we got 5-15 concepts
            if len(concepts) < 5:
                # Too few, ask for more
                return self._extract_atomic_concepts_retry(raw_text, metadata, classification)
            elif len(concepts) > 15:
                # Too many, take top 15
                concepts = concepts[:15]

            return concepts

        except json.JSONDecodeError as e:
            # Fallback: create minimal concepts
            return self._fallback_concept_extraction(raw_text, metadata)

    def _extract_atomic_concepts_retry(
        self,
        raw_text: str,
        metadata: Dict[str, Any],
        classification: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Retry concept extraction with more explicit prompt."""

        prompt = f"""Extract MORE concepts. Aim for 8-12 atomic concepts.

Break down the text into granular, specific concepts. Don't be too general.

Text:
{raw_text[:4000]}

Return JSON array of concepts (same format as before).
"""

        response = self.llm.generate(prompt, max_tokens=3000)

        try:
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                concepts = json.loads(json_match.group())
            else:
                concepts = json.loads(response)
            return concepts[:15]  # Cap at 15
        except:
            return self._fallback_concept_extraction(raw_text, metadata)

    def _fallback_concept_extraction(
        self,
        raw_text: str,
        metadata: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Fallback: create basic concepts from headings/structure."""

        concepts = []

        # Extract headings as concepts
        lines = raw_text.split('\n')
        for line in lines:
            heading_match = re.match(r'^#{1,3}\s+(.+)$', line)
            if heading_match:
                title = heading_match.group(1).strip()
                if len(title) > 5 and len(title) < 100:
                    concepts.append({
                        'title': title,
                        'definition': f'Concept related to {title}',
                        'explanation': f'Details about {title} from source.',
                        'why_matters': 'Part of core content',
                        'applications': ['To be expanded'],
                        'connections': [],
                        'concept_type': 'concept'
                    })

        # If still too few, create generic ones
        if len(concepts) < 5:
            concepts.append({
                'title': metadata.get('title', 'Main Topic'),
                'definition': 'Core topic of the source',
                'explanation': raw_text[:500],
                'why_matters': 'Central theme',
                'applications': ['To be explored'],
                'connections': [],
                'concept_type': 'concept'
            })

        return concepts[:15]

    def _create_permanent_note(
        self,
        concept: Dict[str, Any],
        literature_note: Note,
        classification: Dict[str, Any]
    ) -> Note:
        """Create one permanent note from concept."""

        # Generate unique ID (timestamp + UUID to prevent collisions)
        note_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"

        # Create metadata
        perm_metadata = NoteMetadata(
            id=note_id,
            title=concept['title'],
            aliases=[],
            type='permanent',
            status='seedling',
            domain=classification.get('domain'),
            subdomain=classification.get('subdomain'),
            tags=classification.get('tags', []),
            basb_para_category='Resources',
            basb_para_path=classification.get('basb_para_path'),
            basb_progressive_summary_layer=0,
            basb_intermediate_packet=False,
            lyt_mocs=classification.get('lyt_mocs', []),
            lyt_fluid_frameworks=[],
            zk_permanent_note_type=concept.get('concept_type', 'concept'),
            zk_connections_count=0,
            zk_connections_quality=0.0,
            source_type=literature_note.metadata.source_type,
            source_title=literature_note.metadata.source_title,
            source_authors=literature_note.metadata.source_authors,
            created=datetime.now().isoformat(),
            reviewed=0,
            next_review=(datetime.now() + timedelta(days=7)).isoformat(),
            confidence=0.75,
            completeness=0.60
        )

        # Create body
        body = self._render_permanent_template(concept, literature_note)

        return Note(metadata=perm_metadata, content=body)

    def _render_permanent_template(
        self,
        concept: Dict[str, Any],
        literature_note: Note
    ) -> str:
        """Render permanent note body."""

        applications_str = '\n'.join(f'- {app}' for app in concept.get('applications', []))
        connections_str = '\n'.join(f'- [[{conn}]]' for conn in concept.get('connections', []))

        return f"""# {concept['title']}

> [!abstract] Atomic Definition
> **{concept['definition']}**
>
> *Progressive Summarization Layer 0 (raw capture)*

---

## 🎯 Essência do Conceito

{concept.get('explanation', 'To be expanded')}

---

## 💡 Por Que Importa?

{concept.get('why_matters', 'Significance to be elaborated')}

---

## 🔬 Aplicações

{applications_str if applications_str else '- To be identified'}

---

## 🌐 Conexões

> [!tip] Related Concepts
> These connections will be refined by the Conector agent.

{connections_str if connections_str else '- To be linked'}

---

## 📚 Fonte

From: [[{literature_note.metadata.title}]]

---

## ❓ Questões Abertas

> [!question] To Explore
> - [ ] How does this connect to other domains?
> - [ ] What are counter-examples or limitations?
> - [ ] Are there practical experiments to validate?

---

**Status:** 🌱 Seedling (new, needs review and linking)
**Próxima Revisão:** {datetime.now() + timedelta(days=7):%Y-%m-%d}
**Confiança:** 75% | **Completude:** 60%
"""

    def _validate_destillation(
        self,
        literature_note: Note,
        permanent_notes: List[Note]
    ) -> Dict[str, Any]:
        """Validate destillation results."""

        checks = {}

        # Check 1: Right number of permanent notes (5-15)
        checks['concept_count'] = {
            'passed': 5 <= len(permanent_notes) <= 15,
            'message': 'Should create 5-15 permanent notes',
            'value': len(permanent_notes)
        }

        # Check 2: Each permanent note has content
        min_content_length = 200
        content_checks = [len(n.content) > min_content_length for n in permanent_notes]
        checks['content_not_empty'] = {
            'passed': all(content_checks),
            'message': f'Each note should have >{min_content_length} chars',
            'value': f'{sum(content_checks)}/{len(permanent_notes)} passed'
        }

        # Check 3: Literature note exists and has content
        checks['literature_note_valid'] = {
            'passed': literature_note is not None and len(literature_note.content) > 500,
            'message': 'Literature note should exist with >500 chars',
            'value': len(literature_note.content) if literature_note else 0
        }

        # Check 4: All notes have proper metadata
        metadata_checks = []
        for note in permanent_notes:
            has_required = all([
                note.metadata.title,
                note.metadata.domain,
                note.metadata.basb_para_path,
                len(note.metadata.tags) > 0
            ])
            metadata_checks.append(has_required)

        checks['metadata_complete'] = {
            'passed': all(metadata_checks),
            'message': 'All notes should have complete metadata',
            'value': f'{sum(metadata_checks)}/{len(permanent_notes)} passed'
        }

        # Check 5: Notes are atomic (title < 100 chars)
        atomic_checks = [len(n.metadata.title) < 100 for n in permanent_notes]
        checks['notes_atomic'] = {
            'passed': all(atomic_checks),
            'message': 'Note titles should be concise (<100 chars)',
            'value': f'{sum(atomic_checks)}/{len(permanent_notes)} passed'
        }

        all_passed = all(c['passed'] for c in checks.values())

        return {
            'passed': all_passed,
            'checks': checks,
            'summary': f"{'✅ PASSED' if all_passed else '❌ FAILED'}: {sum(c['passed'] for c in checks.values())}/{len(checks)} checks"
        }

    def save_notes(
        self,
        literature_note: Note,
        permanent_notes: List[Note]
    ) -> Dict[str, Any]:
        """Save all notes to vault."""

        saved_files = []

        # Save literature note
        lit_path = self._get_note_path(literature_note, is_literature=True)
        lit_path.parent.mkdir(parents=True, exist_ok=True)
        lit_path.write_text(literature_note.to_markdown(), encoding='utf-8')
        saved_files.append(str(lit_path))

        # Save permanent notes
        for perm_note in permanent_notes:
            perm_path = self._get_note_path(perm_note, is_literature=False)
            perm_path.parent.mkdir(parents=True, exist_ok=True)
            perm_path.write_text(perm_note.to_markdown(), encoding='utf-8')
            saved_files.append(str(perm_path))

        return {
            'saved_count': len(saved_files),
            'files': saved_files,
            'literature_note_path': str(lit_path),
            'permanent_notes_dir': str(perm_path.parent)
        }

    def _get_note_path(self, note: Note, is_literature: bool) -> Path:
        """Get file path for note based on type."""

        if is_literature:
            # Literature notes go to 02-Literature/
            base_dir = self.vault_path / "02-Literature"

            if note.metadata.source_type == 'academic_paper':
                subdir = base_dir / "papers"
            elif note.metadata.source_type == 'book':
                subdir = base_dir / "books"
            else:
                subdir = base_dir / "articles"

            filename = self._sanitize_filename(note.metadata.title) + ".md"
            return subdir / filename

        else:
            # Permanent notes go to 03-Permanent/
            base_dir = self.vault_path / "03-Permanent"

            # Organize by concept type
            concept_type = note.metadata.zk_permanent_note_type or 'concepts'
            subdir = base_dir / f"{concept_type}s"

            filename = self._sanitize_filename(note.metadata.title) + ".md"
            return subdir / filename

    def _sanitize_filename(self, title: str) -> str:
        """Sanitize title for filename."""
        # Remove invalid chars
        sanitized = re.sub(r'[<>:"/\\|?*]', '', title)
        # Replace spaces with hyphens
        sanitized = sanitized.replace(' ', '-')
        # Limit length
        sanitized = sanitized[:100]
        return sanitized
