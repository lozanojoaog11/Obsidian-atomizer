"""Conector: Semantic linking agent using embeddings.

Creates intelligent connections between notes:
- Semantic similarity (embeddings)
- Typed links (supports, extends, applies, prerequisite, contrasts, related)
- Zero orphans policy
- Target: 4-6 links per note

Zettelkasten principle: Notes gain value through connections.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import re
import json
from datetime import datetime

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from cerebrum.models.note import Note, NoteMetadata
from cerebrum.services.llm_service import LLMService


class ConectorAgent:
    """Creates semantic connections between notes."""

    def __init__(
        self,
        llm_service: LLMService,
        vault_path: Path,
        embeddings_path: Optional[Path] = None
    ):
        self.llm = llm_service
        self.vault_path = vault_path
        self.embeddings_path = embeddings_path or (vault_path / ".cerebrum" / "embeddings")

        # Initialize ChromaDB
        if CHROMADB_AVAILABLE:
            self.embeddings_path.mkdir(parents=True, exist_ok=True)
            self.chroma_client = chromadb.PersistentClient(
                path=str(self.embeddings_path),
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.chroma_client.get_or_create_collection(
                name="permanent_notes",
                metadata={"description": "Permanent notes for semantic search"}
            )
        else:
            self.chroma_client = None
            self.collection = None

    def connect_notes(
        self,
        new_notes: List[Note],
        existing_notes: Optional[List[Note]] = None
    ) -> Dict[str, Any]:
        """
        Create connections for new notes.

        Args:
            new_notes: Newly created notes to connect
            existing_notes: Optional list of existing vault notes

        Returns:
            Dict with:
                - links_created: Total links created
                - orphans: Notes with 0 links
                - avg_links: Average links per note
                - link_quality: Average confidence of links
        """

        # Load existing notes if not provided
        if existing_notes is None:
            existing_notes = self._load_existing_notes()

        # Add new notes to embeddings
        self._index_notes(new_notes)

        all_links = []
        orphans = []

        # Connect each new note
        for note in new_notes:
            links = self._find_connections_for_note(
                note, existing_notes + new_notes
            )

            if len(links) == 0:
                orphans.append(note.metadata.title)

            all_links.extend(links)

            # Update note with links
            self._update_note_links(note, links)

        # Bidirectional linking: update target notes
        self._create_bidirectional_links(all_links, existing_notes + new_notes)

        # Stats
        total_notes = len(new_notes)
        total_links = len(all_links)
        avg_links = total_links / total_notes if total_notes > 0 else 0
        avg_quality = sum(link['confidence'] for link in all_links) / total_links if total_links > 0 else 0

        return {
            'links_created': total_links,
            'orphans': orphans,
            'orphan_rate': len(orphans) / total_notes if total_notes > 0 else 0,
            'avg_links_per_note': avg_links,
            'link_quality': avg_quality,
            'validation_passed': len(orphans) == 0 and avg_links >= 3
        }

    def _load_existing_notes(self) -> List[Note]:
        """Load existing permanent notes from vault."""

        notes = []
        permanent_dir = self.vault_path / "03-Permanent"

        if not permanent_dir.exists():
            return notes

        for note_file in permanent_dir.rglob("*.md"):
            try:
                note = Note.from_markdown(note_file.read_text(encoding='utf-8'))
                notes.append(note)
            except Exception as e:
                # Skip malformed notes
                continue

        return notes

    def _index_notes(self, notes: List[Note]) -> None:
        """Add notes to embedding index."""

        if not self.collection:
            return  # ChromaDB not available

        for note in notes:
            # Create embedding text: title + definition + key content
            embedding_text = f"{note.metadata.title}\n\n{note.content[:1000]}"

            # Add to collection
            self.collection.add(
                ids=[note.metadata.id],
                documents=[embedding_text],
                metadatas=[{
                    'title': note.metadata.title,
                    'domain': note.metadata.domain or 'general',
                    'type': note.metadata.zk_permanent_note_type or 'concept'
                }]
            )

    def _find_connections_for_note(
        self,
        note: Note,
        all_notes: List[Note]
    ) -> List[Dict[str, Any]]:
        """Find semantic connections for a single note."""

        links = []

        # Strategy 1: Semantic similarity (embeddings)
        if self.collection:
            similar_notes = self._find_similar_by_embeddings(note, top_k=10)
            links.extend(similar_notes)

        # Strategy 2: LLM-based contextual linking
        if len(links) < 5:  # If embeddings didn't find enough
            llm_links = self._find_connections_via_llm(note, all_notes)
            links.extend(llm_links)

        # Strategy 3: Domain/tag-based linking
        domain_links = self._find_connections_by_domain(note, all_notes)
        links.extend(domain_links)

        # Deduplicate and rank
        links = self._deduplicate_links(links)

        # Take top 4-8 links
        links = sorted(links, key=lambda x: x['confidence'], reverse=True)[:8]

        return links

    def _find_similar_by_embeddings(
        self,
        note: Note,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """Find similar notes using embeddings."""

        if not self.collection:
            return []

        embedding_text = f"{note.metadata.title}\n\n{note.content[:1000]}"

        # Query
        results = self.collection.query(
            query_texts=[embedding_text],
            n_results=top_k,
            where={"type": {"$ne": "literature"}}  # Exclude literature notes
        )

        links = []
        if results and results['ids']:
            for i, note_id in enumerate(results['ids'][0]):
                if note_id == note.metadata.id:
                    continue  # Skip self

                distance = results['distances'][0][i] if 'distances' in results else 0.5
                confidence = 1.0 - distance  # Convert distance to confidence

                # Determine link type based on similarity
                link_type = self._infer_link_type(confidence)

                links.append({
                    'target': results['metadatas'][0][i]['title'],
                    'target_id': note_id,
                    'type': link_type,
                    'confidence': round(confidence, 2),
                    'context': f'Semantically similar ({confidence:.0%})',
                    'method': 'embeddings'
                })

        return links

    def _infer_link_type(self, confidence: float) -> str:
        """Infer link type based on confidence score."""

        if confidence > 0.85:
            return 'supports'  # Very similar, likely supports
        elif confidence > 0.75:
            return 'related'  # Related concept
        elif confidence > 0.65:
            return 'extends'  # Extends the idea
        else:
            return 'related'  # General relation

    def _find_connections_via_llm(
        self,
        note: Note,
        all_notes: List[Note],
        max_candidates: int = 20
    ) -> List[Dict[str, Any]]:
        """Use LLM to find contextual connections."""

        # Sample candidates (domain match + random)
        candidates = [n for n in all_notes if n.metadata.id != note.metadata.id]
        domain_matches = [n for n in candidates if n.metadata.domain == note.metadata.domain]
        others = [n for n in candidates if n.metadata.domain != note.metadata.domain]

        # Take top domain matches + some others
        candidates = domain_matches[:15] + others[:5]
        candidates = candidates[:max_candidates]

        if not candidates:
            return []

        # Build prompt
        candidate_list = "\n".join([
            f"{i+1}. [[{c.metadata.title}]] - {c.content[:150]}..."
            for i, c in enumerate(candidates)
        ])

        prompt = f"""You are an expert at creating Zettelkasten connections.

Source note:
**Title:** {note.metadata.title}
**Content:** {note.content[:800]}

Candidate notes to link to:
{candidate_list}

Identify 3-6 meaningful connections. For each:
1. Which note to link (by number)
2. Link type: supports/extends/applies/prerequisite/contrasts/related
3. Why the connection matters (brief context)
4. Confidence 0-1

Return JSON:
[
  {{
    "note_number": 1,
    "link_type": "supports",
    "context": "Provides evidence for this concept",
    "confidence": 0.85
  }}
]

Return ONLY valid JSON.
"""

        try:
            response = self.llm.generate(prompt, max_tokens=800)

            # Parse JSON
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                connections = json.loads(json_match.group())
            else:
                return []

            # Convert to link format
            links = []
            for conn in connections:
                note_idx = conn.get('note_number', 1) - 1
                if 0 <= note_idx < len(candidates):
                    target_note = candidates[note_idx]
                    links.append({
                        'target': target_note.metadata.title,
                        'target_id': target_note.metadata.id,
                        'type': conn.get('link_type', 'related'),
                        'confidence': conn.get('confidence', 0.7),
                        'context': conn.get('context', ''),
                        'method': 'llm'
                    })

            return links

        except Exception as e:
            return []

    def _find_connections_by_domain(
        self,
        note: Note,
        all_notes: List[Note]
    ) -> List[Dict[str, Any]]:
        """Find connections based on domain/tag overlap."""

        links = []

        for candidate in all_notes:
            if candidate.metadata.id == note.metadata.id:
                continue

            # Check domain match
            domain_match = candidate.metadata.domain == note.metadata.domain

            # Check tag overlap
            note_tags = set(note.metadata.tags)
            candidate_tags = set(candidate.metadata.tags)
            tag_overlap = len(note_tags & candidate_tags)

            if domain_match and tag_overlap >= 2:
                confidence = 0.6 + (tag_overlap * 0.05)  # Base 0.6, +0.05 per shared tag
                confidence = min(confidence, 0.85)  # Cap at 0.85

                links.append({
                    'target': candidate.metadata.title,
                    'target_id': candidate.metadata.id,
                    'type': 'related',
                    'confidence': round(confidence, 2),
                    'context': f'Same domain, {tag_overlap} shared tags',
                    'method': 'domain'
                })

        return links

    def _deduplicate_links(self, links: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate links, keeping highest confidence."""

        seen = {}
        for link in links:
            target = link['target_id']
            if target not in seen or link['confidence'] > seen[target]['confidence']:
                seen[target] = link

        return list(seen.values())

    def _update_note_links(self, note: Note, links: List[Dict[str, Any]]) -> None:
        """Update note content with links."""

        # Update metadata
        note.metadata.links_out = links
        note.metadata.zk_connections_count = len(links)
        note.metadata.zk_connections_quality = sum(l['confidence'] for l in links) / len(links) if links else 0

        # Update content - add links to "Conexões" section
        if "## 🌐 Conexões" in note.content:
            # Replace existing connections section
            pattern = r'(## 🌐 Conexões.*?)(---|\Z)'
            connections_text = self._render_connections(links)
            note.content = re.sub(
                pattern,
                f"## 🌐 Conexões\n\n{connections_text}\n\n---",
                note.content,
                flags=re.DOTALL
            )
        else:
            # Append connections section
            connections_text = self._render_connections(links)
            note.content += f"\n\n## 🌐 Conexões\n\n{connections_text}\n\n---\n"

    def _render_connections(self, links: List[Dict[str, Any]]) -> str:
        """Render connections section."""

        if not links:
            return "> [!info] No connections yet\n> Connections will be created by Conector agent."

        # Group by type
        by_type = {}
        for link in links:
            link_type = link['type']
            if link_type not in by_type:
                by_type[link_type] = []
            by_type[link_type].append(link)

        sections = []

        # Order: prerequisite, supports, extends, applies, related, contrasts
        type_order = ['prerequisite', 'supports', 'extends', 'applies', 'related', 'contrasts']
        type_headers = {
            'prerequisite': '### É Fundamentado Por (Prerequisites)',
            'supports': '### Fundamenta (Supports)',
            'extends': '### Estende (Extends)',
            'applies': '### Aplica-se Em (Applications)',
            'related': '### Relacionados (Related)',
            'contrasts': '### Contrasta Com (Contrasts)'
        }

        for link_type in type_order:
            if link_type in by_type:
                sections.append(type_headers[link_type])
                for link in by_type[link_type]:
                    conf_pct = int(link['confidence'] * 100)
                    sections.append(f"- [[{link['target']}]] ({conf_pct}%) - {link['context']}")
                sections.append("")  # Blank line

        return "\n".join(sections)

    def _create_bidirectional_links(
        self,
        all_links: List[Dict[str, Any]],
        all_notes: List[Note]
    ) -> None:
        """Create reverse links (links_in) for target notes."""

        # Group links by target
        by_target = {}
        for link in all_links:
            target_id = link['target_id']
            if target_id not in by_target:
                by_target[target_id] = []
            by_target[target_id].append(link)

        # Update target notes
        notes_by_id = {n.metadata.id: n for n in all_notes}

        for target_id, incoming_links in by_target.items():
            if target_id in notes_by_id:
                target_note = notes_by_id[target_id]

                # Add to links_in
                for link in incoming_links:
                    reverse_link = {
                        'source': link['target'],  # The note that linked here
                        'source_id': link.get('source_id', 'unknown'),
                        'type': self._reverse_link_type(link['type']),
                        'confidence': link['confidence']
                    }
                    target_note.metadata.links_in.append(reverse_link)

                # Update connection count
                target_note.metadata.zk_connections_count += len(incoming_links)

    def _reverse_link_type(self, link_type: str) -> str:
        """Get reverse of link type."""

        reverse_map = {
            'supports': 'supported_by',
            'extends': 'extended_by',
            'applies': 'applied_in',
            'prerequisite': 'required_for',
            'contrasts': 'contrasts',
            'related': 'related'
        }

        return reverse_map.get(link_type, 'related')

    def update_vault_links(self, notes: List[Note]) -> Dict[str, Any]:
        """Save updated notes back to vault."""

        updated_files = []

        for note in notes:
            note_path = self._find_note_path(note)
            if note_path and note_path.exists():
                note_path.write_text(note.to_markdown(), encoding='utf-8')
                updated_files.append(str(note_path))

        return {
            'updated_count': len(updated_files),
            'files': updated_files
        }

    def _find_note_path(self, note: Note) -> Optional[Path]:
        """Find path to note file in vault."""

        # Check 03-Permanent first
        permanent_dir = self.vault_path / "03-Permanent"

        if permanent_dir.exists():
            for note_file in permanent_dir.rglob("*.md"):
                if note_file.stem in [note.metadata.title, note.metadata.id]:
                    return note_file

        return None
