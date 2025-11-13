"""
Distiller Agent - Atomizes knowledge from raw text into structured notes.
"""

from pathlib import Path
from typing import List, Dict, Any
import frontmatter
from datetime import datetime

from cerebrum.agents.base import BaseAgent
from cerebrum.intelligence.llm import LLMService
from cerebrum.vault.parser import MarkdownParser
from cerebrum.utils.templates import TemplateEngine


class Note:
    """Represents an atomic note."""

    def __init__(self, title: str, content: str, metadata: Dict[str, Any], file_path: Path):
        self.title = title
        self.content = content
        self.metadata = metadata
        self.file_path = file_path

    def to_markdown(self) -> str:
        """Convert to markdown with frontmatter."""
        post = frontmatter.Post(self.content)
        post.metadata = self.metadata
        return frontmatter.dumps(post)

    def save(self):
        """Save note to file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(self.to_markdown(), encoding='utf-8')


class DistillerAgent(BaseAgent):
    """
    Distills raw knowledge into atomic notes.

    Workflow:
    1. Parse input (PDF, Markdown, text)
    2. Use LLM to identify key concepts
    3. Generate atomic notes for each concept
    4. Apply templates
    5. Save to vault
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.llm = LLMService(config['llm'])
        self.parser = MarkdownParser()
        self.template_engine = TemplateEngine(config)

    def process_file(self, file_path: Path, template: str = 'concept') -> List[Note]:
        """Process a single file and return atomic notes."""
        self.start_timer()

        # Read content
        if file_path.suffix == '.pdf':
            content = self._extract_pdf(file_path)
        else:
            content = file_path.read_text(encoding='utf-8')

        # Extract concepts
        concepts = self._identify_concepts(content)

        # Generate notes
        notes = []
        for i, concept_data in enumerate(concepts):
            note = self._create_note(
                concept_data=concept_data,
                source_content=content,
                source_file=file_path.name,
                template=template,
                index=i
            )
            note.save()
            notes.append(note)

        self.stop_timer()
        return notes

    def _extract_pdf(self, file_path: Path) -> str:
        """Extract text from PDF."""
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
            return text
        except ImportError:
            raise ImportError("Install pypdf to process PDFs: pip install pypdf")

    def _identify_concepts(self, content: str) -> List[Dict[str, Any]]:
        """Use LLM to identify key concepts in the content."""

        prompt = f"""Analyze the following text and identify 5-10 key atomic concepts.

For each concept, provide:
1. **title**: A clear, concise title (2-5 words)
2. **definition**: One-sentence definition
3. **context**: Why this concept matters (2-3 sentences)
4. **connections**: Potential connections to other concepts mentioned

Text to analyze:
---
{content[:8000]}
---

Respond in JSON format:
{{
  "concepts": [
    {{
      "title": "Concept Title",
      "definition": "One sentence definition",
      "context": "Explanation of importance",
      "connections": ["Related Concept 1", "Related Concept 2"]
    }}
  ]
}}
"""

        response = self.llm.generate(prompt, json_mode=True)

        # Parse JSON response
        import json
        try:
            data = json.loads(response)
            return data.get('concepts', [])
        except json.JSONDecodeError:
            # Fallback: simple extraction
            return self._fallback_extraction(content)

    def _fallback_extraction(self, content: str) -> List[Dict[str, Any]]:
        """Simple fallback if LLM fails."""
        # Extract headings as concepts
        lines = content.split('\n')
        concepts = []

        for line in lines:
            if line.startswith('#'):
                title = line.lstrip('#').strip()
                if title and len(title) < 100:
                    concepts.append({
                        'title': title,
                        'definition': 'Concept extracted from heading',
                        'context': '',
                        'connections': []
                    })

        return concepts[:10]  # Limit to 10

    def _create_note(
        self,
        concept_data: Dict[str, Any],
        source_content: str,
        source_file: str,
        template: str,
        index: int
    ) -> Note:
        """Create a note from concept data."""

        title = concept_data['title']

        # Generate slug
        slug = self._slugify(title)

        # Prepare metadata
        metadata = {
            'type': 'concept',
            'status': 'seedling',
            'created': datetime.now().isoformat(),
            'source': source_file,
            'tags': self.config['taxonomy'].get('tags', [])[:2],  # First 2 tags
            'confidence': 0.75,
        }

        # Generate content using template
        content = self._generate_content(concept_data, source_content, template)

        # Determine output path
        output_dir = Path(self.config['vault']['permanent'])
        file_path = output_dir / f"{slug}.md"

        return Note(
            title=title,
            content=content,
            metadata=metadata,
            file_path=file_path
        )

    def _generate_content(
        self,
        concept_data: Dict[str, Any],
        source_content: str,
        template: str
    ) -> str:
        """Generate note content using LLM and template."""

        prompt = f"""Write a concise, atomic note about: {concept_data['title']}

Definition: {concept_data['definition']}
Context: {concept_data.get('context', '')}

Source material (for reference):
{source_content[:3000]}

Create a note with these sections:
1. Brief definition (1-2 sentences)
2. Key insights (2-3 bullet points)
3. Connections to other concepts
4. Practical applications (if applicable)

Write in clear, concise Markdown. Use callouts for emphasis.
Use Portuguese (pt-BR).
"""

        content = self.llm.generate(prompt, temperature=0.4)

        # Ensure title is present
        if not content.startswith('#'):
            content = f"# {concept_data['title']}\n\n{content}"

        return content

    def _slugify(self, text: str) -> str:
        """Convert text to slug."""
        import re
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_-]+', '-', text)
        text = re.sub(r'^-+|-+$', '', text)
        return text
