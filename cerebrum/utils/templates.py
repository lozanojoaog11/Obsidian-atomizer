"""Template engine for note generation."""

from typing import Dict, Any
from pathlib import Path


class TemplateEngine:
    """Simple template engine."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.templates_dir = Path('.cerebrum/templates')

    def load_template(self, name: str) -> str:
        """Load template by name."""
        template_path = self.templates_dir / f"{name}.md"

        if template_path.exists():
            return template_path.read_text(encoding='utf-8')

        # Return default template
        return self.default_template()

    def default_template(self) -> str:
        """Default note template."""
        return """# {title}

> [!abstract] Definition
> {definition}

## Context

{context}

## Connections

{connections}

## Applications

{applications}
"""

    def render(self, template: str, variables: Dict[str, str]) -> str:
        """Render template with variables."""
        for key, value in variables.items():
            template = template.replace(f"{{{key}}}", str(value))
        return template
