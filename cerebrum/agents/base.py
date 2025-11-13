"""Base agent class for all Cerebrum agents."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List
import time


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.start_time = None
        self.elapsed_time = 0

    def start_timer(self):
        """Start performance timer."""
        self.start_time = time.time()

    def stop_timer(self):
        """Stop performance timer."""
        if self.start_time:
            self.elapsed_time = time.time() - self.start_time

    @abstractmethod
    def process(self, *args, **kwargs):
        """Main processing method - must be implemented by subclasses."""
        pass

    def log(self, message: str, level: str = "info"):
        """Simple logging."""
        print(f"[{level.upper()}] {message}")
