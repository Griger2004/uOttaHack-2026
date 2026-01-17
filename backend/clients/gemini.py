"""
Gemini API client for AI-powered text analysis.
Updated for Google Gen AI SDK (v1.0+).
"""

import os
from google import genai
from google.genai import types
from config import settings


class GeminiClient:
    """Client for interacting with Google's Gemini API."""

    def __init__(self):
        """Initialize the Gemini client with API key from settings."""
        # Initialize the new Client
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def generate(self, prompt: str) -> str:
        """
        Generate content using Gemini.
        """
        try:
            # New SDK call format
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.0,  # Keep it deterministic
                    safety_settings=[  # Disable safety filters to prevent crashes on news topics
                        types.SafetySetting(
                            category="HARM_CATEGORY_DANGEROUS_CONTENT",
                            threshold="BLOCK_NONE",
                        ),
                        types.SafetySetting(
                            category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"
                        ),
                        types.SafetySetting(
                            category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"
                        ),
                        types.SafetySetting(
                            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            threshold="BLOCK_NONE",
                        ),
                    ],
                ),
            )
            return response.text.strip()
        except Exception as e:
            print(f"🔥 GEMINI ERROR: {e}")
            # Return a safe fallback so the server doesn't 500 crash
            return "Error: Unable to generate response."


# Singleton instance for reuse
gemini_client = GeminiClient()
