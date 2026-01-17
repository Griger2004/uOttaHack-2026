"""
Yellowcake API client for web scraping.
"""

from typing import Optional
import requests
from config import settings


class YellowcakeClient:
    """Client for scraping web content via Yellowcake API."""

    def __init__(self):
        """Initialize the Yellowcake client."""
        self.endpoint = settings.yellowcake_endpoint
        self.api_key = settings.yellowcake_api_key
        self.timeout = settings.request_timeout

    def scrape(self, url: str) -> Optional[str]:
        """
        Scrape a URL and extract the main content.

        Args:
            url: The URL to scrape.

        Returns:
            The extracted text content, or None if scraping fails.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "url": url,
            "extract_content": True,
        }

        try:
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()

            # Extract main content - check common response field names
            content = (
                data.get("content")
                or data.get("text")
                or data.get("body")
            )

            return content

        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error scraping {url}: {e}")
            return None


# Singleton instance for reuse
yellowcake_client = YellowcakeClient()
