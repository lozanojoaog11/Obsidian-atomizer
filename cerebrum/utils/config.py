"""Configuration management."""

import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration loader and manager."""

    @staticmethod
    def load(config_path: Path = None) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if config_path is None:
            # Try to find .cerebrum/config.yaml
            current = Path.cwd()
            config_path = current / '.cerebrum' / 'config.yaml'

            if not config_path.exists():
                # Use default config
                return Config.default_config()

        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    @staticmethod
    def default_config() -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'llm': {
                'provider': 'ollama',
                'model': 'llama3.2:latest',
                'temperature': 0.3,
            },
            'embeddings': {
                'model': 'nomic-embed-text',
                'cache': '.cerebrum/embeddings.db',
            },
            'vault': {
                'inbox': '00-Inbox',
                'permanent': '03-Permanent',
                'literature': '02-Literature',
                'mocs': '04-MOCs',
                'meta': '99-Meta',
            },
            'taxonomy': {
                'domains': ['knowledge', 'research'],
                'tags': ['note', 'concept'],
                'stopwords': ['a', 'o', 'e', 'de', 'em', 'para', 'com'],
            },
            'linking': {
                'similarity_threshold': 0.75,
                'max_suggestions': 5,
                'auto_apply': False,
            },
            'reviews': {
                'seedling_interval': '7d',
                'budding_interval': '14d',
                'evergreen_interval': '30d',
            },
        }

    @staticmethod
    def create_default(config_path: Path):
        """Create default config file."""
        config = Config.default_config()
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
