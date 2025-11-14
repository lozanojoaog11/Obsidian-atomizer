"""MOC Agent: Automatically creates and maintains Maps of Content.

Implements LYT (Linking Your Thinking) framework:
- Creates MOC notes for knowledge domains
- Updates existing MOCs when new notes added
- Organizes atomic notes into navigable maps

Core responsibility: Transform suggested MOCs into actual MOC notes
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import re
from datetime import datetime

from cerebrum.models.note import Note, NoteMetadata


class MOCAgent:
    """Creates and maintains Maps of Content (MOCs) automatically."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.mocs_path = vault_path / '04-MOCs'

        # Ensure MOCs directory exists
        self.mocs_path.mkdir(parents=True, exist_ok=True)

    def create_or_update_mocs(
        self,
        permanent_notes: List[Note],
        classification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create or update MOCs for permanent notes.

        Args:
            permanent_notes: List of permanent notes from current processing
            classification: Classification result with suggested MOC names

        Returns:
            Dict with:
                - mocs_created: List[Note] (newly created MOCs)
                - mocs_updated: List[Note] (updated existing MOCs)
                - stats: Processing statistics
        """

        suggested_mocs = classification.get('lyt_mocs', [])

        mocs_created = []
        mocs_updated = []

        for moc_name in suggested_mocs:
            # Get relevant notes for this MOC
            # For v0.4: All permanent notes from same source belong to same MOC
            relevant_notes = permanent_notes

            if len(relevant_notes) < 3:
                # Skip MOCs with too few notes (not worth creating)
                continue

            # Check if MOC exists
            existing_moc = self._find_existing_moc(moc_name)

            if existing_moc:
                # Update existing MOC
                updated_moc = self._update_moc(existing_moc, relevant_notes)
                mocs_updated.append(updated_moc)
            else:
                # Create new MOC
                new_moc = self._create_moc(
                    moc_name, relevant_notes, classification
                )
                mocs_created.append(new_moc)

        return {
            'mocs_created': mocs_created,
            'mocs_updated': mocs_updated,
            'stats': {
                'mocs_created_count': len(mocs_created),
                'mocs_updated_count': len(mocs_updated),
                'total_notes_mapped': len(permanent_notes) * len(suggested_mocs)
            }
        }

    def _find_existing_moc(self, moc_name: str) -> Optional[Note]:
        """Find existing MOC by name."""

        moc_id = self._slugify(moc_name)
        moc_file = self.mocs_path / f"{moc_id}.md"

        if moc_file.exists():
            return self._load_moc(moc_file)

        return None

    def _create_moc(
        self,
        moc_name: str,
        notes: List[Note],
        classification: Dict[str, Any]
    ) -> Note:
        """Create new MOC note."""

        moc_id = self._slugify(moc_name)

        # Create MOC metadata
        metadata = NoteMetadata(
            id=moc_id,
            title=moc_name,
            type='moc',
            status='seedling',
            domain=classification.get('domain'),
            subdomain=classification.get('subdomain'),
            tags=['lyt/moc', f"domain/{classification.get('domain')}"],
            moc_note_count=len(notes),
            created=datetime.now().isoformat(),
            modified=datetime.now().isoformat()
        )

        # Render MOC body
        body = self._render_moc_template(moc_name, notes, classification)

        moc_note = Note(metadata=metadata, content=body)
        moc_note.file_path = self.mocs_path / f"{moc_id}.md"

        return moc_note

    def _update_moc(
        self,
        existing_moc: Note,
        new_notes: List[Note]
    ) -> Note:
        """Update existing MOC with new notes."""

        # Parse existing note links from MOC
        existing_links = self._extract_note_links(existing_moc.content)

        # Add new notes (avoid duplicates)
        new_note_titles = [n.metadata.title for n in new_notes]
        combined_titles = list(set(existing_links + new_note_titles))
        combined_titles.sort()  # Alphabetical order

        # Update note count in metadata
        existing_moc.metadata.moc_note_count = len(combined_titles)
        existing_moc.metadata.modified = datetime.now().isoformat()

        # Update status based on note count
        if len(combined_titles) >= 15:
            existing_moc.metadata.status = 'evergreen'
        elif len(combined_titles) >= 8:
            existing_moc.metadata.status = 'budding'

        # Update MOC content with new note list
        existing_moc.content = self._update_moc_note_list(
            existing_moc.content,
            combined_titles,
            len(existing_links)  # Original count
        )

        # Update status emoji in content
        status_emoji = self._get_status_emoji(existing_moc.metadata.status)
        existing_moc.content = re.sub(
            r'> \*\*Status:\*\* [🌱🌿🌳] \w+',
            f'> **Status:** {status_emoji} {existing_moc.metadata.status.title()}',
            existing_moc.content
        )

        return existing_moc

    def _render_moc_template(
        self,
        moc_name: str,
        notes: List[Note],
        classification: Dict[str, Any]
    ) -> str:
        """Render MOC template with Apple + Epistemic design."""

        domain = classification.get('domain', 'general')
        subdomain = classification.get('subdomain', '')
        note_count = len(notes)

        # Create note list
        note_list = '\n'.join(
            f"- [[{note.metadata.title}]]"
            for note in sorted(notes, key=lambda n: n.metadata.title)
        )

        # Domain description
        domain_path = f"{domain} / {subdomain}" if subdomain else domain

        today = datetime.now().strftime('%Y-%m-%d')

        return f"""# 🗺️ {moc_name}

> [!abstract] Map of Content
> **Domain:** {domain_path}
> **Status:** 🌱 Seedling ({note_count} notes)
> **Purpose:** Navigate and synthesize knowledge in this area

---

## 🎯 What Is This Map About?

> [!question] Core Questions
> - What is the central theme connecting these notes?
> - Why did these ideas cluster together?
> - What journey does this map enable?

This map organizes knowledge in the **{domain}** domain{f', specifically focusing on **{subdomain}**' if subdomain else ''}. It serves as an entry point to navigate atomic concepts and discover connections between ideas.

The notes below represent distilled insights from various sources, organized for easy exploration and synthesis.

---

## 🗺️ The Landscape

> [!tip] Navigate this knowledge domain
> Below are atomic notes organized alphabetically

### Core Concepts

{note_list}

### Related Maps

> [!info] Connected MOCs
> Add links to related maps as you discover them

- `[[]]` - Related map

---

## 💡 Why Does This Matter?

> [!question] Significance
> - What problems does this knowledge solve?
> - What projects could benefit from this?
> - What becomes possible with this understanding?

**Your answer:**
-

---

## 🔬 Synthesis & Insights

> [!tip] Emergent patterns across these notes
> As you review notes in this map, capture emerging insights:

**Patterns I've noticed:**
-

**Connections to other maps:**
-

**Surprising insights:**
-

**Key themes:**
-

---

## 📋 Curated Paths

> [!example] Suggested reading sequences
> Different paths through this knowledge for different goals

**For beginners:**
1. Start: `[[]]`
2. Then: `[[]]`
3. Finally: `[[]]`

**For deep dive:**
-

**For practical application:**
-

---

## ❓ Open Questions

> [!question] To explore further
> - [ ] What's missing from this map?
> - [ ] What contradictions exist between notes?
> - [ ] What experiments could test these ideas?
> - [ ] How does this connect to other domains?

**Personal questions:**
-

---

## 🔄 Evolution

> [!info] Map Status
> **Current:** 🌱 Seedling
>
> **Progress toward Evergreen:**
> - [{'x' if note_count >= 5 else ' '}] ≥5 notes mapped (Currently: {note_count})
> - [ ] ≥3 curated paths created
> - [ ] ≥2 synthesis insights captured
> - [ ] Used in at least 1 project

**Update History:**
- {today}: Created with {note_count} notes

---

## 💭 Personal Notes

> [!tip] Your unique perspective on this domain

**Why I care about this:**


**How I've used this map:**


**Projects that drew from this:**


---

**Meta:** This MOC is auto-maintained by Cerebrum · [LYT Framework](https://www.linkingyourthinking.com/)
"""

    def _update_moc_note_list(
        self,
        existing_content: str,
        note_titles: List[str],
        original_count: int
    ) -> str:
        """Update the note list in MOC while preserving manual edits."""

        # Build new note list
        new_note_list = '\n'.join(f"- [[{title}]]" for title in note_titles)

        # Find and replace Core Concepts section
        pattern = r'(### Core Concepts\s*\n\n)(.*?)(\n\n###|\n\n---)'

        def replacer(match):
            return match.group(1) + new_note_list + match.group(3)

        updated = re.sub(pattern, replacer, existing_content, flags=re.DOTALL)

        # Update note count in abstract
        new_count = len(note_titles)
        updated = re.sub(
            r'> \*\*Status:\*\* ([🌱🌿🌳]) (\w+) \(\d+ notes\)',
            f'> **Status:** \\1 \\2 ({new_count} notes)',
            updated
        )

        # Add update entry to Evolution history
        today = datetime.now().strftime('%Y-%m-%d')
        notes_added = new_count - original_count

        history_pattern = r'(\*\*Update History:\*\*\n)(.*?)(\n\n---)'

        def add_history(match):
            existing_history = match.group(2)
            new_entry = f"- {today}: Added {notes_added} new notes (total: {new_count})"
            return match.group(1) + existing_history + '\n' + new_entry + match.group(3)

        updated = re.sub(history_pattern, add_history, updated, flags=re.DOTALL)

        # Update progress checklist
        updated = re.sub(
            r'- \[[ x]\] ≥5 notes mapped \(Currently: \d+\)',
            f"- [{'x' if new_count >= 5 else ' '}] ≥5 notes mapped (Currently: {new_count})",
            updated
        )

        return updated

    def _extract_note_links(self, content: str) -> List[str]:
        """Extract all note links from MOC content."""

        # Find all [[Note Title]] links
        links = re.findall(r'\[\[([^\]]+)\]\]', content)

        # Filter out empty links and clean up
        links = [link.strip() for link in links if link.strip()]

        return links

    def _load_moc(self, moc_file: Path) -> Note:
        """Load existing MOC from file."""

        content = moc_file.read_text(encoding='utf-8')

        # Parse frontmatter and content
        # Simple parsing - assumes frontmatter is YAML between --- markers
        frontmatter_match = re.search(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)

        if frontmatter_match:
            # Parse frontmatter (simplified - just extract key fields)
            fm_text = frontmatter_match.group(1)
            body = frontmatter_match.group(2)

            # Extract metadata fields
            title_match = re.search(r'title: (.+)', fm_text)
            status_match = re.search(r'status: (.+)', fm_text)
            domain_match = re.search(r'domain: (.+)', fm_text)

            metadata = NoteMetadata(
                id=moc_file.stem,
                title=title_match.group(1) if title_match else moc_file.stem,
                type='moc',
                status=status_match.group(1) if status_match else 'seedling',
                domain=domain_match.group(1) if domain_match else 'general'
            )
        else:
            # No frontmatter, use defaults
            metadata = NoteMetadata(
                id=moc_file.stem,
                title=moc_file.stem.replace('-', ' ').title(),
                type='moc',
                status='seedling'
            )
            body = content

        note = Note(metadata=metadata, content=body)
        note.file_path = moc_file

        return note

    def save_moc(self, moc: Note) -> Dict[str, Any]:
        """Save MOC note to vault."""

        # Build frontmatter
        frontmatter = self._build_frontmatter(moc.metadata)

        # Complete content
        full_content = f"---\n{frontmatter}\n---\n{moc.content}"

        # Write to file
        moc.file_path.write_text(full_content, encoding='utf-8')

        return {
            'success': True,
            'file_path': str(moc.file_path),
            'note_id': moc.metadata.id
        }

    def _build_frontmatter(self, metadata: NoteMetadata) -> str:
        """Build YAML frontmatter for MOC."""

        lines = []
        lines.append(f"id: {metadata.id}")
        lines.append(f"title: {metadata.title}")
        lines.append(f"type: {metadata.type}")
        lines.append(f"status: {metadata.status}")

        if metadata.domain:
            lines.append(f"domain: {metadata.domain}")

        if metadata.subdomain:
            lines.append(f"subdomain: {metadata.subdomain}")

        if metadata.tags:
            tags_str = '[' + ', '.join(metadata.tags) + ']'
            lines.append(f"tags: {tags_str}")

        if hasattr(metadata, 'moc_note_count'):
            lines.append(f"moc_note_count: {metadata.moc_note_count}")

        lines.append(f"created: {metadata.created}")

        if hasattr(metadata, 'modified'):
            lines.append(f"modified: {metadata.modified}")

        return '\n'.join(lines)

    def _slugify(self, text: str) -> str:
        """Convert text to slug (lowercase, hyphens)."""

        # Convert to lowercase
        text = text.lower()

        # Replace spaces and special chars with hyphens
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_]+', '-', text)
        text = re.sub(r'-+', '-', text)

        # Remove leading/trailing hyphens
        text = text.strip('-')

        return text

    def _get_status_emoji(self, status: str) -> str:
        """Get emoji for status."""

        status_map = {
            'seedling': '🌱',
            'budding': '🌿',
            'evergreen': '🌳'
        }

        return status_map.get(status, '🌱')

    def validate_moc(self, moc: Note) -> Dict[str, Any]:
        """Validate MOC quality."""

        checks = {}

        # Check 1: Has title
        checks['has_title'] = {
            'passed': moc.metadata.title is not None and len(moc.metadata.title) > 0,
            'message': 'MOC should have a title',
            'value': moc.metadata.title
        }

        # Check 2: Has domain
        checks['has_domain'] = {
            'passed': moc.metadata.domain is not None,
            'message': 'MOC should have a domain',
            'value': moc.metadata.domain
        }

        # Check 3: Minimum notes
        note_count = getattr(moc.metadata, 'moc_note_count', 0)
        checks['min_notes'] = {
            'passed': note_count >= 3,
            'message': 'MOC should have at least 3 notes',
            'value': note_count
        }

        # Check 4: Has status
        checks['has_status'] = {
            'passed': moc.metadata.status in ['seedling', 'budding', 'evergreen'],
            'message': 'MOC should have valid status',
            'value': moc.metadata.status
        }

        # Check 5: Has note links in content
        note_links = len(self._extract_note_links(moc.content))
        checks['has_links'] = {
            'passed': note_links >= 3,
            'message': 'MOC should have at least 3 note links',
            'value': note_links
        }

        all_passed = all(c['passed'] for c in checks.values())

        return {
            'passed': all_passed,
            'checks': checks,
            'summary': f"{'✅ PASSED' if all_passed else '❌ FAILED'}: {sum(c['passed'] for c in checks.values())}/{len(checks)} checks"
        }
