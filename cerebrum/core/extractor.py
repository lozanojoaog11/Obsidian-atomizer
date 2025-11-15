"""Extractor: Converts PDF/Markdown/Text to structured data.

Handles:
- PDF extraction with metadata
- Markdown parsing
- Text normalization
- Structure detection (sections, headings)
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
import re
from datetime import datetime


class ExtractionResult:
    """Result of extraction process."""

    def __init__(
        self,
        raw_text: str,
        metadata: Dict[str, Any],
        structure: Dict[str, Any],
        stats: Dict[str, int]
    ):
        self.raw_text = raw_text
        self.metadata = metadata
        self.structure = structure
        self.stats = stats
        self.success = True
        self.error = None


class ExtractionError(Exception):
    """Extraction failed."""
    pass


class Extractor:
    """Extracts and structures content from various file types."""

    def __init__(self):
        self.supported_types = {'.pdf', '.md', '.txt', '.markdown'}

    def extract(self, file_path: Path) -> ExtractionResult:
        """
        Extract content from file.

        Args:
            file_path: Path to file

        Returns:
            ExtractionResult with text, metadata, structure

        Raises:
            ExtractionError: If extraction fails
        """
        if not file_path.exists():
            raise ExtractionError(f"File not found: {file_path}")

        suffix = file_path.suffix.lower()

        if suffix not in self.supported_types:
            raise ExtractionError(
                f"Unsupported file type: {suffix}. "
                f"Supported: {self.supported_types}"
            )

        # Route to appropriate extractor
        if suffix == '.pdf':
            return self._extract_pdf(file_path)
        elif suffix in {'.md', '.markdown'}:
            return self._extract_markdown(file_path)
        elif suffix == '.txt':
            return self._extract_text(file_path)

    def _extract_pdf(self, file_path: Path) -> ExtractionResult:
        """Extract from PDF with metadata."""
        try:
            from pypdf import PdfReader
        except ImportError:
            raise ExtractionError(
                "pypdf not installed. Install with: pip install pypdf"
            )

        try:
            reader = PdfReader(file_path)

            # Extract text from all pages
            text_parts = []
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

            raw_text = "\n\n".join(text_parts)

            # Extract metadata
            pdf_meta = reader.metadata if reader.metadata else {}

            metadata = {
                'source_type': 'pdf',
                'title': self._extract_title_from_text(raw_text) or pdf_meta.get('/Title', file_path.stem),
                'authors': self._extract_authors_from_text(raw_text),
                'pages': len(reader.pages),
                'file_name': file_path.name,
                'file_size': file_path.stat().st_size,
                'extracted_at': datetime.now().isoformat()
            }

            # Detect structure
            structure = self._analyze_structure(raw_text)

            # Stats
            stats = {
                'word_count': len(raw_text.split()),
                'char_count': len(raw_text),
                'pages': len(reader.pages),
                'sections': len(structure['sections'])
            }

            # Normalize text
            normalized_text = self._normalize_text(raw_text)

            return ExtractionResult(
                raw_text=normalized_text,
                metadata=metadata,
                structure=structure,
                stats=stats
            )

        except Exception as e:
            raise ExtractionError(f"PDF extraction failed: {str(e)}")

    def _extract_markdown(self, file_path: Path) -> ExtractionResult:
        """Extract from Markdown file."""
        try:
            text = file_path.read_text(encoding='utf-8')

            # Check if has frontmatter
            has_frontmatter = text.startswith('---')

            if has_frontmatter:
                # Parse with frontmatter
                import frontmatter
                post = frontmatter.loads(text)
                raw_text = post.content
                fm_metadata = post.metadata
            else:
                raw_text = text
                fm_metadata = {}

            metadata = {
                'source_type': 'markdown',
                'title': fm_metadata.get('title') or self._extract_title_from_text(raw_text) or file_path.stem,
                'authors': fm_metadata.get('authors', []),
                'file_name': file_path.name,
                'file_size': file_path.stat().st_size,
                'extracted_at': datetime.now().isoformat(),
                **fm_metadata  # Include all frontmatter
            }

            structure = self._analyze_structure(raw_text)

            stats = {
                'word_count': len(raw_text.split()),
                'char_count': len(raw_text),
                'sections': len(structure['sections'])
            }

            normalized_text = self._normalize_text(raw_text)

            return ExtractionResult(
                raw_text=normalized_text,
                metadata=metadata,
                structure=structure,
                stats=stats
            )

        except Exception as e:
            raise ExtractionError(f"Markdown extraction failed: {str(e)}")

    def _extract_text(self, file_path: Path) -> ExtractionResult:
        """Extract from plain text file."""
        try:
            text = file_path.read_text(encoding='utf-8')

            metadata = {
                'source_type': 'text',
                'title': self._extract_title_from_text(text) or file_path.stem,
                'file_name': file_path.name,
                'file_size': file_path.stat().st_size,
                'extracted_at': datetime.now().isoformat()
            }

            structure = self._analyze_structure(text)

            stats = {
                'word_count': len(text.split()),
                'char_count': len(text),
                'sections': len(structure['sections'])
            }

            normalized_text = self._normalize_text(text)

            return ExtractionResult(
                raw_text=normalized_text,
                metadata=metadata,
                structure=structure,
                stats=stats
            )

        except Exception as e:
            raise ExtractionError(f"Text extraction failed: {str(e)}")

    def _normalize_text(self, text: str) -> str:
        """Normalize text (line endings, spacing, etc.)."""
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')

        # Remove excessive blank lines (max 2 consecutive)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Remove leading/trailing whitespace
        text = text.strip()

        return text

    def _analyze_structure(self, text: str) -> Dict[str, Any]:
        """Detect document structure (sections, headings)."""
        sections = []
        headings = []

        # Detect markdown headings
        lines = text.split('\n')
        current_pos = 0

        for i, line in enumerate(lines):
            # Heading detection
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()

                headings.append({
                    'level': level,
                    'title': title,
                    'line': i,
                    'position': current_pos
                })

                # If top-level heading, consider it a section
                if level <= 2:
                    sections.append({
                        'title': title,
                        'start': current_pos,
                        'end': None,  # Will be filled by next section
                        'line': i
                    })

            current_pos += len(line) + 1  # +1 for newline

        # Fill end positions for sections
        for i in range(len(sections) - 1):
            sections[i]['end'] = sections[i + 1]['start']

        if sections:
            sections[-1]['end'] = len(text)

        return {
            'sections': sections,
            'headings': headings,
            'has_structure': len(sections) > 0
        }

    def _extract_title_from_text(self, text: str) -> Optional[str]:
        """Try to extract title from text content."""
        lines = text.split('\n')

        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()

            # Markdown heading
            heading_match = re.match(r'^#{1,2}\s+(.+)$', line)
            if heading_match:
                return heading_match.group(1).strip()

            # First non-empty line that's not too long
            if line and len(line) < 200 and not line.startswith('['):
                # Remove common prefixes
                title = re.sub(r'^(Title:|Abstract:)\s*', '', line, flags=re.IGNORECASE)
                if title:
                    return title.strip()

        return None

    def _extract_authors_from_text(self, text: str) -> List[str]:
        """Try to extract author names from text."""
        authors = []

        # Look for common patterns in first 2000 chars
        header = text[:2000]

        # Pattern: "Authors: Name1, Name2"
        author_match = re.search(r'Authors?:\s*([^\n]+)', header, re.IGNORECASE)
        if author_match:
            author_text = author_match.group(1)
            # Split by common delimiters
            names = re.split(r'[,;&]|\sand\s', author_text)
            authors = [n.strip() for n in names if n.strip()]

        return authors

    def validate_extraction(self, result: ExtractionResult) -> Dict[str, Any]:
        """Validate extraction result."""
        checks = {}

        # Check 1: Text not empty
        checks['text_not_empty'] = {
            'passed': len(result.raw_text) > 100,
            'message': 'Text should be >100 characters',
            'value': len(result.raw_text)
        }

        # Check 2: Metadata has required fields
        required_fields = ['source_type', 'title']
        checks['metadata_complete'] = {
            'passed': all(f in result.metadata for f in required_fields),
            'message': f'Metadata should contain: {required_fields}',
            'value': list(result.metadata.keys())
        }

        # Check 3: Text is valid UTF-8
        try:
            result.raw_text.encode('utf-8')
            checks['encoding_valid'] = {
                'passed': True,
                'message': 'UTF-8 encoding valid'
            }
        except UnicodeEncodeError:
            checks['encoding_valid'] = {
                'passed': False,
                'message': 'Encoding error detected'
            }

        # Check 4: Reasonable word count
        wc = result.stats['word_count']
        checks['word_count_reasonable'] = {
            'passed': 50 < wc < 500000,
            'message': 'Word count should be 50-500,000',
            'value': wc
        }

        all_passed = all(c['passed'] for c in checks.values())

        return {
            'passed': all_passed,
            'checks': checks
        }
