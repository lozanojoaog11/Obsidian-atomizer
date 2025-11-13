"""LLM Service: Local Ollama with Gemini fallback.

Priority:
1. Ollama (local) - llama3.2 or similar
2. Gemini (fallback) - if Ollama unavailable

Simple, reliable, works.
"""

import os
from typing import Optional, Dict, Any
import requests
import json


class LLMService:
    """Unified LLM service supporting Ollama and Gemini."""

    def __init__(
        self,
        provider: str = "ollama",
        model: Optional[str] = None,
        ollama_host: str = "http://localhost:11434",
        gemini_api_key: Optional[str] = None
    ):
        self.provider = provider
        self.ollama_host = ollama_host
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")

        # Set default models
        if model:
            self.model = model
        elif provider == "ollama":
            self.model = "llama3.2"  # Or llama2, mistral, etc.
        elif provider == "gemini":
            self.model = "gemini-1.5-flash"

        # Test provider
        if provider == "ollama":
            self._test_ollama()
        elif provider == "gemini" and not self.gemini_api_key:
            raise ValueError("Gemini API key required. Set GEMINI_API_KEY env var.")

    def _test_ollama(self):
        """Test if Ollama is available."""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=2)
            if response.status_code != 200:
                raise Exception("Ollama not responding")
        except Exception as e:
            raise Exception(
                f"Ollama not available at {self.ollama_host}. "
                f"Start with: ollama serve\n"
                f"Install model with: ollama pull {self.model}\n"
                f"Error: {str(e)}"
            )

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate text from prompt."""

        if self.provider == "ollama":
            return self._generate_ollama(prompt, max_tokens, temperature, **kwargs)
        elif self.provider == "gemini":
            return self._generate_gemini(prompt, max_tokens, temperature, **kwargs)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _generate_ollama(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> str:
        """Generate using Ollama."""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }

        try:
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json=payload,
                timeout=120
            )

            if response.status_code != 200:
                raise Exception(f"Ollama error: {response.text}")

            result = response.json()
            return result.get("response", "")

        except Exception as e:
            raise Exception(f"Ollama generation failed: {str(e)}")

    def _generate_gemini(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        **kwargs
    ) -> str:
        """Generate using Gemini."""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            }
        }

        try:
            response = requests.post(
                f"{url}?key={self.gemini_api_key}",
                headers=headers,
                json=payload,
                timeout=120
            )

            if response.status_code != 200:
                raise Exception(f"Gemini error: {response.text}")

            result = response.json()

            # Extract text from response
            candidates = result.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    return parts[0].get("text", "")

            return ""

        except Exception as e:
            raise Exception(f"Gemini generation failed: {str(e)}")

    def embed(self, texts: list) -> list:
        """Generate embeddings (Ollama only for now)."""

        if self.provider != "ollama":
            raise NotImplementedError("Embeddings only supported for Ollama")

        embeddings = []

        for text in texts:
            payload = {
                "model": self.model,
                "prompt": text
            }

            try:
                response = requests.post(
                    f"{self.ollama_host}/api/embeddings",
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    embeddings.append(result.get("embedding", []))
                else:
                    # Fallback: empty embedding
                    embeddings.append([0.0] * 768)

            except Exception:
                # Fallback: empty embedding
                embeddings.append([0.0] * 768)

        return embeddings

    @classmethod
    def create_default(cls) -> 'LLMService':
        """Create default LLM service (tries Ollama first, falls back to Gemini)."""

        # Try Ollama first
        try:
            return cls(provider="ollama")
        except Exception:
            pass

        # Fall back to Gemini
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            return cls(provider="gemini", gemini_api_key=gemini_key)

        # No LLM available
        raise Exception(
            "No LLM available. Either:\n"
            "1. Start Ollama: ollama serve && ollama pull llama3.2\n"
            "2. Set GEMINI_API_KEY environment variable"
        )
