"""
Gemini API client for AI-powered text analysis.
"""

import google.generativeai as genai
from config import settings


class GeminiClient:
    """Client for interacting with Google's Gemini API."""

    def __init__(self):
        """Initialize the Gemini client with API key from settings."""
        genai.configure(api_key=settings.gemini_api_key)
        self._model = genai.GenerativeModel(settings.gemini_model)

    @property
    def model(self):
        """Get the configured Gemini model."""
        return self._model

    def generate(self, prompt: str) -> str:
        """
        Generate content using Gemini.

        Args:
            prompt: The prompt to send to Gemini.

        Returns:
            The generated text response.

        Raises:
            Exception: If generation fails.
        """
        response = self._model.generate_content(prompt)
        return response.text.strip()


# Singleton instance for reuse
gemini_client = GeminiClient()
