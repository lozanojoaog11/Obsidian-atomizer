"""Markdown parsing utilities."""

import frontmatter
from pathlib import Path
from typing import Dict, Any, Optional


class MarkdownParser:
    """Parser for markdown files with frontmatter."""

    def parse(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse markdown file and extract frontmatter + content.

        Returns:
            {
                'metadata': {...},
                'content': '...',
                'title': '...'
            }
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        # Extract title from content or frontmatter
        title = post.metadata.get('title')
        if not title:
            # Try to get from first heading
            for line in post.content.split('\n'):
                if line.startswith('#'):
                    title = line.lstrip('#').strip()
                    break

        return {
            'metadata': post.metadata,
            'content': post.content,
            'title': title or file_path.stem
        }

    def extract_links(self, content: str) -> list[str]:
        """Extract wikilinks from content."""
        import re
        pattern = r'\[\[([^\]]+)\]\]'
        return re.findall(pattern, content)
