"""Note model with complete frontmatter (BASB + LYT + Zettelkasten)."""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
import frontmatter
import re


@dataclass
class NoteMetadata:
    """Complete metadata combining all frameworks."""

    # === IDENTIFICATION ===
    id: str  # Timestamp-based unique ID
    title: str
    aliases: List[str] = field(default_factory=list)

    # === CLASSIFICATION ===
    type: str = "permanent"  # fleeting, literature, permanent, moc, project
    status: str = "seedling"  # seedling, budding, evergreen, crystallized

    # === TAXONOMY ===
    domain: Optional[str] = None
    subdomain: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    # === BASB ===
    basb_para_category: str = "Resources"
    basb_para_path: Optional[str] = None
    basb_progressive_summary_layer: int = 0
    basb_intermediate_packet: bool = False
    basb_projects_using: List[str] = field(default_factory=list)

    # === LYT ===
    lyt_mocs: List[str] = field(default_factory=list)
    lyt_fluid_frameworks: List[str] = field(default_factory=list)
    lyt_context: Optional[str] = None
    moc_note_count: int = 0  # For MOC notes: count of notes in this map

    # === ZETTELKASTEN ===
    zk_permanent_note_type: Optional[str] = None  # concept, principle, model, evidence
    zk_connections_count: int = 0
    zk_connections_quality: float = 0.0
    zk_centrality_score: float = 0.0
    zk_cluster_id: Optional[str] = None

    # === SOURCE ===
    source_type: Optional[str] = None
    source_title: Optional[str] = None
    source_authors: List[str] = field(default_factory=list)
    source_year: Optional[int] = None
    source_doi: Optional[str] = None
    source_url: Optional[str] = None

    # === MANAGEMENT ===
    created: str = field(default_factory=lambda: datetime.now().isoformat())
    modified: str = field(default_factory=lambda: datetime.now().isoformat())
    reviewed: int = 0
    last_reviewed: Optional[str] = None
    next_review: str = field(default_factory=lambda: (datetime.now() + timedelta(days=7)).isoformat())
    version: int = 1

    # === QUALITY ===
    confidence: float = 0.75
    completeness: float = 0.6
    importance: str = "medium"  # low, medium, high, critical
    evidence_strength: str = "medium"  # low, medium, high

    # === RELATIONS (managed by Connector) ===
    links_out: List[Dict[str, Any]] = field(default_factory=list)
    links_in: List[Dict[str, Any]] = field(default_factory=list)

    def to_frontmatter_dict(self) -> Dict[str, Any]:
        """Convert to frontmatter dict with proper structure."""
        return {
            'id': self.id,
            'title': self.title,
            'aliases': self.aliases,
            'type': self.type,
            'status': self.status,
            'domain': self.domain,
            'subdomain': self.subdomain,
            'tags': self.tags,
            'basb': {
                'para_category': self.basb_para_category,
                'para_path': self.basb_para_path,
                'progressive_summary': {
                    'layer': self.basb_progressive_summary_layer,
                    'last_summarized': None
                },
                'intermediate_packet': self.basb_intermediate_packet,
                'projects_using': self.basb_projects_using
            },
            'lyt': {
                'mocs': self.lyt_mocs,
                'fluid_frameworks': self.lyt_fluid_frameworks,
                'context': self.lyt_context,
                'moc_note_count': self.moc_note_count
            },
            'zettelkasten': {
                'permanent_note_type': self.zk_permanent_note_type,
                'connections_count': self.zk_connections_count,
                'connections_quality': self.zk_connections_quality,
                'centrality_score': self.zk_centrality_score,
                'cluster_id': self.zk_cluster_id
            },
            'source': {
                'type': self.source_type,
                'title': self.source_title,
                'authors': self.source_authors,
                'year': self.source_year,
                'doi': self.source_doi,
                'url': self.source_url
            },
            'created': self.created,
            'modified': self.modified,
            'reviewed': self.reviewed,
            'last_reviewed': self.last_reviewed,
            'next_review': self.next_review,
            'version': self.version,
            'confidence': self.confidence,
            'completeness': self.completeness,
            'importance': self.importance,
            'evidence_strength': self.evidence_strength,
            'links_out': self.links_out,
            'links_in': self.links_in
        }


@dataclass
class Note:
    """Complete note with frontmatter and content."""

    metadata: NoteMetadata
    content: str
    slug: str = ""
    file_path: Optional[Path] = None

    def __post_init__(self):
        """Generate slug if not provided."""
        if not self.slug:
            self.slug = self._slugify(self.metadata.title)

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert text to slug."""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_-]+', '-', text)
        text = re.sub(r'^-+|-+$', '', text)
        return text

    def to_markdown(self) -> str:
        """Convert to markdown with frontmatter."""
        post = frontmatter.Post(self.content)
        post.metadata = self.metadata.to_frontmatter_dict()
        return frontmatter.dumps(post)

    def save(self, base_path: Path):
        """Save note to file."""
        if not self.file_path:
            # Determine path based on BASB para
            if self.metadata.basb_para_path:
                note_dir = base_path / self.metadata.basb_para_path
            else:
                note_dir = base_path / "03-Permanent"

            note_dir.mkdir(parents=True, exist_ok=True)
            self.file_path = note_dir / f"{self.slug}.md"

        # Write file
        self.file_path.write_text(self.to_markdown(), encoding='utf-8')

        return self.file_path

    @classmethod
    def from_markdown(cls, markdown_text: str, file_path: Optional[Path] = None) -> 'Note':
        """Load note from markdown string."""
        post = frontmatter.loads(markdown_text)

        # Reconstruct metadata
        meta_dict = post.metadata

        # Flatten nested structures
        metadata = NoteMetadata(
            id=meta_dict.get('id', ''),
            title=meta_dict.get('title', ''),
            aliases=meta_dict.get('aliases', []),
            type=meta_dict.get('type', 'permanent'),
            status=meta_dict.get('status', 'seedling'),
            domain=meta_dict.get('domain'),
            subdomain=meta_dict.get('subdomain'),
            tags=meta_dict.get('tags', []),
            basb_para_category=meta_dict.get('basb', {}).get('para_category', 'Resources'),
            basb_para_path=meta_dict.get('basb', {}).get('para_path'),
            basb_progressive_summary_layer=meta_dict.get('basb', {}).get('progressive_summary', {}).get('layer', 0),
            basb_intermediate_packet=meta_dict.get('basb', {}).get('intermediate_packet', False),
            basb_projects_using=meta_dict.get('basb', {}).get('projects_using', []),
            lyt_mocs=meta_dict.get('lyt', {}).get('mocs', []),
            lyt_fluid_frameworks=meta_dict.get('lyt', {}).get('fluid_frameworks', []),
            lyt_context=meta_dict.get('lyt', {}).get('context'),
            moc_note_count=meta_dict.get('lyt', {}).get('moc_note_count', 0),
            zk_permanent_note_type=meta_dict.get('zettelkasten', {}).get('permanent_note_type'),
            zk_connections_count=meta_dict.get('zettelkasten', {}).get('connections_count', 0),
            zk_connections_quality=meta_dict.get('zettelkasten', {}).get('connections_quality', 0.0),
            zk_centrality_score=meta_dict.get('zettelkasten', {}).get('centrality_score', 0.0),
            zk_cluster_id=meta_dict.get('zettelkasten', {}).get('cluster_id'),
            source_type=meta_dict.get('source', {}).get('type'),
            source_title=meta_dict.get('source', {}).get('title'),
            source_authors=meta_dict.get('source', {}).get('authors', []),
            source_year=meta_dict.get('source', {}).get('year'),
            source_doi=meta_dict.get('source', {}).get('doi'),
            source_url=meta_dict.get('source', {}).get('url'),
            created=meta_dict.get('created', datetime.now().isoformat()),
            modified=meta_dict.get('modified', datetime.now().isoformat()),
            reviewed=meta_dict.get('reviewed', 0),
            last_reviewed=meta_dict.get('last_reviewed'),
            next_review=meta_dict.get('next_review', (datetime.now() + timedelta(days=7)).isoformat()),
            version=meta_dict.get('version', 1),
            confidence=meta_dict.get('confidence', 0.75),
            completeness=meta_dict.get('completeness', 0.6),
            importance=meta_dict.get('importance', 'medium'),
            evidence_strength=meta_dict.get('evidence_strength', 'medium'),
            links_out=meta_dict.get('links_out', []),
            links_in=meta_dict.get('links_in', [])
        )

        slug = cls._slugify(metadata.title)

        return cls(
            metadata=metadata,
            content=post.content,
            slug=slug,
            file_path=file_path
        )

    @classmethod
    def from_markdown_file(cls, file_path: Path) -> 'Note':
        """Load note from markdown file."""
        markdown_text = file_path.read_text(encoding='utf-8')
        return cls.from_markdown(markdown_text, file_path=file_path)

    def add_link(self, target_slug: str, link_type: str, confidence: float, context: str = ""):
        """Add outbound link."""
        link = {
            'target': target_slug,
            'type': link_type,
            'confidence': confidence,
            'context': context
        }

        # Avoid duplicates
        if not any(l['target'] == target_slug for l in self.metadata.links_out):
            self.metadata.links_out.append(link)
            self.metadata.zk_connections_count = len(self.metadata.links_out)

            # Update quality score (average confidence)
            if self.metadata.links_out:
                self.metadata.zk_connections_quality = sum(
                    l['confidence'] for l in self.metadata.links_out
                ) / len(self.metadata.links_out)

    def add_backlink(self, source_slug: str, link_type: str, confidence: float):
        """Add inbound link (backlink)."""
        link = {
            'source': source_slug,
            'type': link_type,
            'confidence': confidence
        }

        if not any(l['source'] == source_slug for l in self.metadata.links_in):
            self.metadata.links_in.append(link)
