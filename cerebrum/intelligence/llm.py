"""
LLM Service - Wrapper for local LLM (Ollama) or remote APIs.
"""

from typing import Dict, Any, Optional


class LLMService:
    """Service for LLM interactions."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get('provider', 'ollama')
        self.model = config.get('model', 'llama3.2:latest')

        if self.provider == 'ollama':
            self._init_ollama()
        elif self.provider == 'gemini':
            self._init_gemini()

    def _init_ollama(self):
        """Initialize Ollama client."""
        try:
            import ollama
            self.client = ollama
        except ImportError:
            raise ImportError(
                "Ollama not installed. Install with: pip install ollama"
            )

    def _init_gemini(self):
        """Initialize Gemini client."""
        try:
            from google import genai
            api_key = self.config.get('api_key')
            if not api_key:
                raise ValueError("Gemini API key not found in config")
            self.client = genai.Client(api_key=api_key)
        except ImportError:
            raise ImportError(
                "Google GenAI not installed. Install with: pip install google-genai"
            )

    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        json_mode: bool = False
    ) -> str:
        """
        Generate text using the LLM.

        Args:
            prompt: The prompt to send
            temperature: Sampling temperature (0.0 - 1.0)
            json_mode: Whether to request JSON output

        Returns:
            Generated text
        """
        if self.provider == 'ollama':
            return self._generate_ollama(prompt, temperature, json_mode)
        elif self.provider == 'gemini':
            return self._generate_gemini(prompt, temperature, json_mode)

    def _generate_ollama(
        self,
        prompt: str,
        temperature: float,
        json_mode: bool
    ) -> str:
        """Generate using Ollama."""
        try:
            options = {'temperature': temperature}

            if json_mode:
                # Request JSON format in the prompt
                prompt = f"{prompt}\n\nRespond with valid JSON only."

            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options=options
            )

            return response['response']

        except Exception as e:
            # Fallback to simple response
            return self._fallback_response(prompt)

    def _generate_gemini(
        self,
        prompt: str,
        temperature: float,
        json_mode: bool
    ) -> str:
        """Generate using Gemini."""
        try:
            config = {
                'temperature': temperature,
            }

            if json_mode:
                config['response_mime_type'] = 'application/json'

            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt,
                config=config
            )

            return response.text

        except Exception as e:
            return self._fallback_response(prompt)

    def _fallback_response(self, prompt: str) -> str:
        """Fallback when LLM is not available."""
        return """# Concept Title

> [!abstract] Definition
> This is a placeholder note. LLM service not available.

## Context

Please configure your LLM service (Ollama or Gemini) in .cerebrum/config.yaml

## Connections

- Related concepts will appear here

## Next Steps

1. Install Ollama: https://ollama.ai
2. Or configure Gemini API key
"""
